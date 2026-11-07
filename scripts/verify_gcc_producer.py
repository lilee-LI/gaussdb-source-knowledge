"""Real GCC regression: C/C++, overloads, static binding, macros, dispatch and cache."""
import argparse
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--cc",default="gcc")
    p.add_argument("--cxx",default="g++")
    args = p.parse_args()
    target = args.output.resolve()
    if target.exists():
        raise ValueError("Use a new verification output directory")
    source = target/"source"
    source.mkdir(parents=True)
    (source/"shared.h").write_text("""#ifdef __cplusplus
struct Base { virtual int virt(int) = 0; };
int overloaded(int); int overloaded(double); int target(int);
#define WRAP(x) target(x)
extern "C" {
#endif
int c_target(int);
#ifdef __cplusplus
}
#endif
""",encoding="utf-8")
    (source/"first.cpp").write_text("""#include "shared.h"
static int local(int x) { return x + 1; }
int target(int x) { return local(x); }
int overloaded(int x) { return x; }
int overloaded(double x) { return int(x); }
int caller(Base* b, int (*callback)(int), int x) {
    return overloaded(x) + overloaded(1.5) + WRAP(x) + b->virt(x) + callback(x) + c_target(x);
}
int unicode_line(int x) { /* 汉字 */ return target(x); }
""",encoding="utf-8")
    (source/"second.cpp").write_text('#include "shared.h"\nstatic int local(int x) { return x + 2; }\nint consumer(int x) { return target(x) + local(x); }\n',encoding="utf-8")
    (source/"third.c").write_text('int c_target(int x) { return x + 3; }\n',encoding="utf-8")
    for folder,name,absolute in (("parser-a","generated_a",False),("parser-b","generated_b",True)):
        parser = source/folder
        parser.mkdir()
        body = 'int '+name+'(int x) { return target(x); }\n'
        (parser/"grammar.y").write_text(body,encoding="utf-8")
        label = str(parser/"grammar.y") if absolute else "grammar.y"
        (parser/"grammar.cpp").write_text('#include "../shared.h"\n#line '+('2153' if absolute else '1')+' '+json.dumps(label)+'\n'+body,encoding="utf-8")
    entries = [{"file":str(source/name),"directory":str(source),
                "arguments":[args.cc if name.endswith(".c") else args.cxx,"-std=c11" if name.endswith(".c") else "-std=c++14",
                             "-I"+str(source),"-c",name,"-o",name+".o"]}
               for name in ("first.cpp","second.cpp","third.c","parser-a/grammar.cpp","parser-b/grammar.cpp")]
    compile_db = target/"compile_commands.json"
    compile_db.write_text(json.dumps(entries),encoding="utf-8")
    common = ["sh",str(ROOT/"ecs.sh"),"build","--source",str(source),"--compile-db",str(compile_db),
              "--cc",args.cc,"--cxx",args.cxx,"--work",str(target/"work"),"--jobs","2","--frontend","gcc"]
    def run(name,*extra,success=True):
        result = subprocess.run([*common,"--output",str(target/name),*extra],capture_output=True,text=True,encoding="utf-8")
        (target/(name+".log")).write_text(result.stderr,encoding="utf-8")
        if success:
            assert result.returncode==0,result.stderr[-3000:]
            return json.loads(result.stdout)
        assert result.returncode!=0,"Missing include was incorrectly accepted"
    first = run("handoff")
    assert first["coverage"]["parsed_tus"]==5 and first["coverage"]["partial_tus"]==0
    with sqlite3.connect(target/"handoff/knowledge.sqlite3") as db:
        nodes = {r[0]:json.loads(r[1]) for r in db.execute("SELECT id,data FROM symbols")}
        edges = [json.loads(r[0]) for r in db.execute("SELECT data FROM relations")]
        def named(a,b):
            return [e for e in edges if nodes.get(e["source"],{}).get("name")==a and nodes.get(e["target"],{}).get("name")==b]
        assert len({v["usr"] for v in nodes.values() if v["name"]=="overloaded"})==2
        assert all(e["resolution"]=="resolved" for e in named("caller","overloaded"))
        assert any(e.get("target_binding")=="linked_definitions" and e["resolution"]=="resolved" for e in named("consumer","target"))
        assert any(e.get("target_binding")=="linked_definitions" for e in named("caller","c_target"))
        assert len([n for n in nodes.values() if n["name"]=="local"])==2
        assert any(e["dispatch"]=="virtual" and e["resolution"]=="candidate" for e in edges)
        assert any(e["dispatch"]=="indirect" and e["resolution"]=="candidate" for e in edges)
        macro = named("caller","target")
        assert macro and macro[0]["spelling_location"]["asset"]!="server/first.cpp" and macro[0]["asset"]=="server/first.cpp"
        utf = named("unicode_line","target")
        assert utf and (source/"first.cpp").read_bytes()[utf[0]["offset"]:utf[0]["offset"]+1]==b"("
        for folder,name in (("parser-a","generated_a"),("parser-b","generated_b")):
            mapped = named(name,"target")
            assert mapped and mapped[0]["asset"]=="server/"+folder+"/grammar.cpp" and mapped[0]["start"]==3
            assert mapped[0]["expansion_location"]["presumed_location"]["line"]==(2153 if folder=="parser-b" else 1)
    repeated = run("repeat")
    assert repeated["run_id"]==first["run_id"],"Unchanged input failed to reuse its native run"
    file = source/"first.cpp"
    stamp = 1600000000
    expected_time = time.strftime("%a %b %e %H:%M:%S %Y",time.localtime(stamp))
    file.write_text(file.read_text(encoding="utf-8")+
        'static_assert(__builtin_strcmp(__FILE__, '+json.dumps(str(file))+') == 0, "source path");\n'+
        'static_assert(__builtin_strcmp(__TIMESTAMP__, '+json.dumps(expected_time)+') == 0, "source timestamp");\n',encoding="utf-8")
    os.utime(file,(stamp,stamp))
    paths = run("paths-and-time")
    assert paths["coverage"]["parsed_tus"]==5,"Frozen inputs changed builtin source macros"
    (source/"shared.h").unlink()
    run("missing",success=False)
    partial = run("partial","--allow-partial")
    assert partial["coverage"]["parsed_tus"]==1 and partial["coverage"]["partial_tus"]+partial["coverage"]["failed_tus"]==4
    report = {"status":"passed","initial":first,"repeat_run":repeated["run_id"],
              "checks":["C and C++","overload ABI identity","cross-TU definition","cross-language linkage","static isolation",
                        "virtual and indirect candidates","macro spelling and expansion","UTF-8 byte location","repeat reuse",
                        "__FILE__ and __TIMESTAMP__ preservation","relative and absolute #line sources","missing header gate"]}
    (target/"verification.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({"status":"passed","checks":report["checks"]}),flush=True)


if __name__=="__main__":
    main()
