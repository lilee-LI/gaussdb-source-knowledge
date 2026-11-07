"""Exercise real Linux capture, macro-selected native calls and coordinator replay."""

import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import sqlite3
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def verify(output):
    output.mkdir(parents=True, exist_ok=False)
    src = output / "source"
    shutil.copytree(ROOT / "assets/ecs-fixture/source", src)
    subprocess.run(["git", "init", "-q"], cwd=src, check=True)
    subprocess.run(["git", "add", "."], cwd=src, check=True)
    (src / "include/build-config.h").write_text(
        "#define SELECT_COMPUTE 1\n", encoding="utf-8"
    )
    (src / "include/generated.h").symlink_to("build-config.h")
    (src / "executor/consumer.cpp").write_text(
        '#include "api.h"\n#include "generated.h"\nint cg_fallback(int x) { return x; }\n'
        "int cg_consume(int x) {\n#if SELECT_COMPUTE && ENABLE_FEATURE\n return cg_compute(x);\n"
        "#else\n return cg_fallback(x);\n#endif\n}\n",
        encoding="utf-8",
    )
    (src / "Makefile").write_text(
        "all: a.o b.o\na.o: optimizer/producer.cpp\n\t$(CXX) @opts.rsp -c $< -o $@\n"
        "b.o: executor/consumer.cpp\n\t$(CXX) @opts.rsp -c $< -o $@\n",
        encoding="utf-8",
    )
    (src / "opts.rsp").write_text("-Iinclude -DENABLE_FEATURE=1\n", encoding="utf-8")

    def run(script, *args, ok=True):
        cmd = ["sh", str(ROOT / script), *map(str, args)]
        r = subprocess.run(cmd, capture_output=True, encoding="utf-8", timeout=420)
        if ok and r.returncode:
            raise RuntimeError(r.stderr[-1500:])
        if not ok:
            assert r.returncode != 0
            return r.stderr
        return json.loads(r.stdout)

    comp = output / "compile_commands.json"
    run(
        "ecs.sh",
        "capture",
        "--source",
        src,
        "--output",
        comp,
        "--",
        "make",
        "-j2",
        "-B",
    )
    rows = json.loads(comp.read_bytes())
    assert len(rows) == 2 and all("-DENABLE_FEATURE=1" in r["arguments"] for r in rows)
    common = [
        "build",
        "--frontend", "clang",
        "--source",
        src,
        "--compile-db",
        comp,
        "--work",
        output / "work",
        "--jobs",
        "2",
    ]
    delivery = output / "handoff"
    r = run("ecs.sh", *common, "--output", delivery)
    assert r["status"] == "ready" and r["coverage"]["parsed_tus"] == 2
    assert r["coverage"]["call_binding"]["linked_definitions"] == 1
    again = run("ecs.sh", *common, "--output", output / "replay")
    assert r["run_id"] == again["run_id"]
    assert "new --output" in run("ecs.sh", *common, "--output", delivery, ok=False)
    # Stop the real controller after its first committed TU. The OS releases the work lock.
    resume_args = [
        "build",
        "--frontend", "clang",
        "--source",
        src,
        "--compile-db",
        comp,
        "--work",
        output / "interrupted",
        "--jobs",
        "1",
        "--output",
        output / "resumed",
    ]
    with subprocess.Popen(
        ["sh", str(ROOT / "ecs.sh"), *map(str, resume_args)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    ) as process:
        for log in process.stderr:
            if "[1/2] parsed" in log:
                os.killpg(process.pid, signal.SIGKILL)
                break
        assert process.wait(timeout=15) < 0
    with sqlite3.connect(output / "interrupted/knowledge.sqlite3") as db:
        completed = db.execute("SELECT run,context,data FROM native_tus").fetchall()
    assert len(completed) == 1
    resumed = run("ecs.sh", *resume_args)
    assert (
        resumed["run_id"] == completed[0][0] and resumed["coverage"]["parsed_tus"] == 2
    )
    with sqlite3.connect(output / "interrupted/knowledge.sqlite3") as db:
        assert (
            db.execute(
                "SELECT data FROM native_tus WHERE run=? AND context=?",
                completed[0][:2],
            ).fetchone()[0]
            == completed[0][2]
        )
    with sqlite3.connect(delivery / "knowledge.sqlite3") as db:
        assert not db.execute("SELECT 1 FROM tu_cache").fetchone()
        assert not db.execute("SELECT 1 FROM tasks").fetchone()
        callees = db.execute(
            "SELECT s.name FROM relations r JOIN symbols s ON s.id=r.target AND s.run=r.run "
            "WHERE r.kind='CALLS'"
        ).fetchall()
        assert callees == [("cg_compute",)]
    checkout = output / "coordinator-source"
    shutil.copytree(
        src,
        checkout,
        ignore=shutil.ignore_patterns(".git", "*.o", "generated.h", "build-config.h"),
    )
    (checkout / "include/generated.h").write_text("build-config.h", encoding="utf-8")
    cfg = output / "paths.json"
    home = output / "learning"
    cfg.write_text(
        json.dumps(
            {
                "source": str(checkout),
                "index_db": str(delivery / "knowledge.sqlite3"),
                "home": str(home),
                "run_id": r["run_id"],
            }
        ),
        encoding="utf-8",
    )
    run("kb.sh", "check", "--paths", cfg)
    plan = run("kb.sh", "start", "--paths", cfg)
    for symbol, direction, peer in (
        ("cg_consume", "forward", "cg_compute"),
        ("cg_compute", "reverse", "cg_consume"),
    ):
        graph = run(
            "kb.sh",
            "--home",
            home,
            "navigate",
            "--symbol",
            symbol,
            "--direction",
            direction,
        )
        assert any(n["name"] == peer for n in graph["nodes"])
        assert any(
            e["resolution"] == "resolved" and e["kind"] == "CALLS"
            for e in graph["relations"]
        )
    (src / "include/generated.h").write_text(
        "#define SELECT_COMPUTE 0\n", encoding="utf-8"
    )
    changed = run("ecs.sh", *common, "--output", output / "changed")
    assert changed["run_id"] != r["run_id"]
    with sqlite3.connect(output / "changed/knowledge.sqlite3") as db:
        assert db.execute(
            "SELECT s.name FROM relations r JOIN symbols s ON s.id=r.target AND s.run=r.run "
            "WHERE r.kind='CALLS'"
        ).fetchall() == [("cg_fallback",)]
    (src / "executor/consumer.cpp").write_text(
        '#include "absent.h"\n', encoding="utf-8"
    )
    failed = output / "failed"
    run("ecs.sh", *common, "--output", failed, ok=False)
    assert not failed.exists()
    partial = run("ecs.sh", *common, "--output", output / "partial", "--allow-partial")
    assert partial["status"] == "partial" and partial["coverage"]["parsed_tus"] == 1
    return {
        "result": "passed",
        "capture_entries": len(rows),
        "parsed_tus": 2,
        "cross_file_call": "cg_consume -> cg_compute",
        "macro_change": "cg_consume -> cg_fallback",
        "repeat_run_reused": True,
        "interrupted_run_resumed": True,
        "missing_header_blocked": True,
        "generated_header_replayed": True,
        "coordinator_plan_modules": plan["modules"],
        "output": str(output),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    print(json.dumps(verify(p.parse_args().output.resolve()), indent=2))
