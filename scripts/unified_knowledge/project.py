"""Path-based user commands over the existing study, review and retrieval workflow."""
import argparse
import json
import shutil
from pathlib import Path
import sqlite3
import sys

from . import study
from .store import Store, atomic_write, canonical, digest, read_json, require

ROOT = Path(__file__).resolve().parents[2]
COMMANDS = {"start","check","modules","features","route","learn","review","wiki","ask"}


def settings(file):
    file = file.expanduser().resolve()
    require(file.is_file(),"将包内 paths.example.json 复制到 local/paths.json 并填写路径，或用 --paths 指定配置文件。")
    spec = read_json(file)
    known = {"source","design","manual","home","index_db","run_id","graph_storage","output","module_prefixes","repository_roots","product","revision"}
    require(isinstance(spec,dict) and not set(spec)-known,"paths.json 含未知字段："+str(sorted(set(spec)-known) if isinstance(spec,dict) else spec))
    def resolve(value):
        return (file.parent/Path(value).expanduser()).resolve()
    require(spec.get("source"),"paths.json 需要 source 源码目录")
    for key in ("source","design","manual","home","index_db","output"):
        if spec.get(key):
            spec[key]=str(resolve(spec[key]))
    spec.setdefault("home",str(resolve("workspace")))
    spec["repository_roots"]={k:str(resolve(v)) for k,v in spec.get("repository_roots",{}).items()}
    return spec


def check(spec):
    from .ecs import index_path
    from .graph_mount import inspect_input
    require(Path(spec["source"]).is_dir(),"源码目录不存在："+spec["source"])
    home=Path(spec["home"])
    for path in [spec["source"],*spec["repository_roots"].values(),*[spec[k] for k in ("manual","design") if spec.get(k)]]:
        root=Path(path)
        require(root.exists(),"材料路径不存在："+path)
        require(not root.is_relative_to(home) and not home.is_relative_to(root),"学习工作区与输入材料目录必须分开："+path)
    graph=None
    if spec.get("index_db"):
        db=index_path(spec["index_db"],home)
        storage=spec.get("graph_storage","reference")
        require(storage in {"copy","auto","reference"},"graph_storage 取 reference、copy 或 auto")
        linked = storage=="reference" or (storage=="auto" and db.stat().st_size>=256*1024**2)
        graph=inspect_input(db,spec.get("run_id"),check_indexes=linked)
        graph["storage"]="reference" if linked else "copy"
    else:
        require(not spec.get("run_id"),"填写 run_id 时请同时配置 index_db")
    return {"mode":"ecs" if graph else "source_only","home":str(home),"graph":graph,
            "python":sys.executable,"sqlite":sqlite3.sqlite_version,"git":shutil.which("git"),
            "database":str(home/"knowledge.sqlite3"),"wiki":str(home/"wiki/index.html")}


def start(spec, refresh):
    from init_internal_project import create
    info = check(spec)
    graph = info["graph"] or {}
    home = Path(spec["home"])
    signature=digest(["checkout-catalog/v2",spec,graph.get("run_id"),str(ROOT),sys.executable])
    if not refresh and (home/"knowledge.sqlite3").is_file():
        with Store(home,readonly=True,graph_override=spec.get("index_db")) as store:
            bound=store.get_meta("project_entry",{})
            if bound.get("signature")==signature and store.get_meta("study_head")==bound.get("plan_id") and Path(bound["mcp"]).is_file():
                return {**bound,**info,"action":"继续已冻结的学习快照。材料更新时用 start --refresh。"}
    args=argparse.Namespace(source=Path(spec["source"]),home=home,output=home/"setup/project.json",
         index_db=spec.get("index_db"),run_id=graph.get("run_id"),graph_storage=graph.get("storage"),
         product=spec.get("product","GaussDB"),revision=spec.get("revision","content-addressed"),
         design=Path(spec["design"]) if spec.get("design") else None,manual=Path(spec["manual"]) if spec.get("manual") else None,
         compile_db=None,repository_roots=spec["repository_roots"],module_prefix=spec.get("module_prefixes",[]),
         role="researcher",workspace_setup=True,source_only=not graph)
    result=create(args)
    with Store(home) as store:
        plan=study.current(store)
        mcp=home/"researcher.mcp.json"
        atomic_write(mcp,Path(result["mcp"]).read_bytes())
        bound={"signature":signature,"plan_id":plan["id"],"plan":result["study_plan"],"run":plan["run"],
               "modules":len(plan["modules"]),"candidates":len(plan.get("candidates",[])),"mcp":str(mcp),"source_snapshot":plan["snapshot"]}
        with store.transaction():
            store.set_meta("project_entry",bound)
    return {**info,**bound,"graph":result.get("graph"),"action":"打开 plan，运行 features，选择 ID 后用 learn --candidate 建单。"}


def review_step(store, args):
    from . import knowledge, planner, team
    task=planner.task_status(store,args.task)
    require(task["snapshot"]==store.get_meta("snapshot_head"),"任务属于另一源码快照")
    require(task["status"] in {"submitted","accepted"} and task.get("result"),"任务尚未提交")
    done=store.db.execute("SELECT id FROM proposals p WHERE status='accepted' AND EXISTS "
                         "(SELECT 1 FROM json_each(p.data,'$.research_tasks') WHERE value=?) LIMIT 1",(args.task,)).fetchone()
    if done:
        return {"status":"knowledge_accepted","proposal":done[0],"next":"运行 wiki 导出阅读版"}
    result=task["result"]
    mode="self_reviewed" if args.reviewer==result["worker"] else "independent_review"
    decision={"reviewer":args.reviewer,"mode":mode,"verdict":"accept","notes":args.notes}
    if args.accept or args.return_for_research:
        require(args.notes and args.notes.strip(),"请填写实际审阅意见 --notes")
    if args.return_for_research:
        require(task["status"]=="submitted","只有待审的研究任务可以退回给成员")
        result=planner.review_task(store,args.task,{**decision,"verdict":"reject","result_digest":args.return_for_research})
        return {"status":result["status"],"task":args.task,"next":"成员重新领取此任务，核对退回原因，修正并提交。"}

    if task["status"]=="submitted":
        if not args.accept:
            refs=sorted({r for u in result.get("claims",[]) for r in u.get("source_refs",[])} |
                        {r for c in result.get("coverage",[]) for r in c.get("evidence_refs",[])})
            return {"stage":"research","task":args.task,"digest":digest(result),"result":result,
                    "evidence":[store.read_evidence(ref,max_chars=6000) for ref in refs],
                    "next":"核对研究内容与源码，认可后以 --accept 此 digest --notes 审阅意见 重跑 review。"}
        planner.review_task(store,args.task,{**decision,"result_digest":args.accept})
        # The following prompt is a separate knowledge decision, bound to the exact proposed units.
        args.accept=None
    proposal=team.propose_task(store,args.task)
    if not args.accept:
        ctx=knowledge.review_context(store,proposal["id"],args.reviewer,max_chars=1000000)
        return {"stage":"knowledge","task":args.task,"proposal":proposal["id"],"digest":ctx["proposal_digest"],
                "units":proposal["units"],"evidence":ctx["evidence"],"truncated":ctx["truncated"],
                "next":"审阅知识提案和引用，认可后用此提案的新 digest 执行同一 review 命令。"}
    rev=knowledge.review(store,proposal["id"],{**decision,"proposal_digest":args.accept})
    return {"status":"knowledge_accepted","revision":rev["id"],"next":"运行 wiki 打开已审知识，或用 ask 查询证据。"}


def execute(args):
    spec=settings(args.paths)
    if args.action=="check":
        return check(spec)
    if args.action=="start":
        return start(spec,args.refresh)
    home=Path(spec["home"])
    require((home/"knowledge.sqlite3").is_file(),"请先在本工作区执行 start")
    with Store(home,readonly=args.action in {"ask","modules","features"}) as store:
        plan=study.current(store)
        if args.action=="modules":
            return [{"module":k,"files":len(v["files"]),"candidate_documents":len(v["document_matches"]),
                     "graph_coverage":v.get("graph_coverage")} for k,v in sorted(plan["modules"].items())]
        if args.action=="features":
            from .catalog import listing
            return listing(store,plan,module=args.module,state=args.state,offset=args.offset,limit=args.limit)
        if args.action=="route":
            return study.route(store,args.candidate,args.module)
        if args.action=="learn":
            from .catalog import candidate
            lead=candidate(plan,args.candidate) if args.candidate else None
            require(lead or (args.module and args.question),"使用 --candidate，或提供 --module 和 --question")
            module=args.module
            module=module or lead["owner_module"]
            require(module,"该候选尚无责任模块，请用 --module 明确归属")
            if module not in plan["modules"]:
                names=[m for m in plan["modules"] if m.endswith("/"+module)]
                require(len(names)==1,"请从 modules 输出选择完整模块名。匹配项："+str(names[:12]))
                module=names[0]
            order=store.get_meta("assignment:"+plan["id"]+":"+module,{})
            actor=args.worker or order.get("worker") or "researcher"
            require(not order or order["worker"]==actor,"请用已分配的成员身份 "+str(order.get("worker")))
            mcp=home/("worker.mcp.json" if plan.get("worker_scope") else "researcher.mcp.json")
            require(mcp.is_file(),"请运行 start 生成此工作区的 MCP 配置")
            work=study.focus(store,module,files=args.file,question=args.question,symbol=args.symbol,candidate_id=args.candidate)
            question=work.get("question") or args.question
            task=work["task"]
            if work.get("reused"):
                status=store.db.execute("SELECT status FROM tasks WHERE id=?",(task,)).fetchone()[0]
                if status in {"accepted","submitted","leased"}:
                    return {**work,"status":status,"next":"查看 features 状态。进行中的任务由租约持有人继续，已提交任务进入 review。"}
            return {**work,"worker":actor,"mcp":str(mcp),"claude_command":'claude --mcp-config "'+str(mcp)+'"',
                    "prompt":f"以 {actor} 身份领取 {task}，研究问题 {question}。读取 task_context、历史结果和文档，按调用点及源码行核对条件和反例。用 read_task_evidence 读取引用，stage_research_unit 保存结论及测试依据，用 finish_research 提交后停下。"}
        if args.action=="review":
            return review_step(store,args)
        if args.action=="wiki":
            from .reader_wiki import export_wiki
            return export_wiki(store)
        if args.action=="ask":
            from .retrieval import get_context
            return get_context(store,{"task":args.role,"query":args.question,"targets":args.symbol,"source_snapshot":plan["snapshot"],
                                      "index_run":plan["run"],"build_profile":plan["profile"],"token_budget":args.budget})


def main(argv):
    p=argparse.ArgumentParser(description="GaussDB 源码知识工程：在 local/paths.json 填写材料和 ECS 路径。",
        epilog="首次使用：check → start → features → learn --candidate <ID>。多人使用 --home <工作区> team --help。")
    subs=p.add_subparsers(dest="action",required=True)
    for name in sorted(COMMANDS):
        a=subs.add_parser(name)
        a.add_argument("--paths",type=Path,default=ROOT/"local/paths.json")
        if name=="start":
            a.add_argument("--refresh",action="store_true")
        if name=="route":
            a.add_argument("--candidate",required=True); a.add_argument("--module",required=True)
        if name=="learn":
            a.add_argument("--module"); a.add_argument("--question"); a.add_argument("--candidate")
            a.add_argument("--symbol"); a.add_argument("--file",action="append",default=[]); a.add_argument("--worker")
        if name=="features":
            a.add_argument("--module"); a.add_argument("--state"); a.add_argument("--limit",type=int,default=30)
            a.add_argument("--offset",type=int,default=0)
        if name=="review":
            a.add_argument("--task",required=True); a.add_argument("--reviewer",required=True); a.add_argument("--notes")
            choice=a.add_mutually_exclusive_group(); choice.add_argument("--accept"); choice.add_argument("--return-for-research")
        if name=="ask":
            a.add_argument("--role",choices=("coding","test_generation","review","operations"),default="coding")
            a.add_argument("--question",required=True); a.add_argument("--symbol",action="append",default=[])
            a.add_argument("--budget",type=int,default=32768)
    try:
        print(json.dumps(execute(p.parse_args(argv)),ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,KeyError,TypeError,sqlite3.Error) as err:
        print(json.dumps({"error":str(err)},ensure_ascii=False),file=sys.stderr)
        return 1
