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
COMMANDS = {"start","check","modules","features","route","learn","review","wiki","ask","plan-tasks","planning-feedback","curriculum","inputs","graph-job",
            "plan","progress","next","advance","run","coverage","verify-uses","accept-coverage"}


def query_config(home, researcher_config):
    value=read_json(Path(researcher_config))
    for server in value["mcpServers"].values():
        args=server["args"]
        args[args.index("--role")+1]="query"
    target=Path(home)/"query.mcp.json"
    if not target.is_file() or read_json(target)!=value:
        atomic_write(target,json.dumps(value,ensure_ascii=False,indent=2)+"\n")
    return str(target)


def research_prompt(task, actor, question):
    return (
        f"以 {actor} 身份研究任务 {task}，问题：{question}。只使用当前 gaussdb_knowledge MCP 工作区。"
        "先 claim_task（建议seconds=14400），读取task_context、冻结方法、已审复用知识、文档和历史结果。"
        "保留返回的token；到期前renew_task续租，checkpoint_task记录进展，必要时release_task。"
        "重新认领后的证据必须在新租约实际回读，不能把旧回执当作新读取。"
        "query_graph的run使用task_context.run，不能用source_index.run_id；get_context的source_snapshot/build_profile/index_run"
        "分别来自任务snapshot/profile/run。lookup_symbols核对真实符号ID，不猜ID或用另一个函数/类型代替。"
        "通过create_task_evidence建立准确区间，并用read_task_evidence完整读取；截断则分段。"
        "优先用search_source在冻结材料检索状态名、字段和文字（支持asset_patterns），再read_source读命中上下文；搜索命中本身不算阅读。"
        "沿入口、状态生产/消费、跨模块契约、宏条件、正常/错误清理、资源寿命、缓存及必要并发/恢复边界研究。"
        "目录或关键词未命中不证明功能/测试不存在；图的候选边不证明运行路径。"
        "每次stage_research_unit提交一个unit。共同字段为id/kind/title/body/conditions/counterexamples/source_refs/symbol_refs/knowledge_refs；"
        "kind只能为module/responsibility/feature/mechanism/claim/contract/flow/test_obligation/requirement/observation/decision。"
        "claim需statement；contract需producers/consumers（真实symbol-instance ID）、requires/ensures/invariants。"
        "knowledge_refs是对象数组，如[{\"relation\":\"DEPENDS_ON\",\"target\":\"claim:example\"}]。"
        "test_obligation的expected_from是单个对象，如{\"kind\":\"contract\",\"ref\":\"contract:example\"}，execution_status=not_run。"
        "flow.steps用call/data_stage/state_transition/async_message区分，不把数据阶段伪装成调用。"
        "责任树和特性树分别使用level=1..4与parent，先提交上级；不要写_binding/review/content_hash等保留字段。"
        "source_refs只能引用本租约真正完整读过的证据。全部完成后，用finish_research提交coverage与最新drafts_digest；"
        "如果task_context含whole_learning，必须遵守该覆盖协议：module_assets分页盘点、read_source逐段读取，"
        "用stage_progress登记资产/候选归属、机制提案、跨模块契约和缺口，并在finish_research同时带最新progress_digest。"
        "模块盘点可以只提交真实规划progress；不能在没读全文件或没形成知识时标记studied。"
        "coverage逐问题包含question/status(answered/open/not_applicable)/explanation/evidence_refs。"
        "存在whole_learning时，新机制和依赖只在stage_progress.proposals/gaps登记；不要再调用planning_feedback另建一份。"
        "只有旧工作区没有whole_learning才用planning_feedback。不逐函数或调用边扩张任务，不重跑全仓索引。"
        "finish_research成功即停止工具调用；租约已经结束，不要继续stage/submit/planning_feedback。"
        "最后返回任务ID、提交状态和缺口，停在待审；不得自行接受研究或知识。"
        "当前为源码研究，不运行数据库、SQL、产品编译或故障注入；未证实的外部实现与构建条件明确保留。"
    )


def settings(file):
    file = file.expanduser().resolve()
    require(file.is_file(),"将包内 paths.example.json 复制到 local/paths.json 并填写路径，或用 --paths 指定配置文件。")
    spec = read_json(file)
    known = {"source","design","manual","features","compile_db","path_maps","curriculum","build_profile","home","index_db","run_id","graph_storage","output","module_prefixes","repository_roots","product","revision","product_adapter","learning_policy"}
    require(isinstance(spec,dict) and not set(spec)-known,"paths.json 含未知字段："+str(sorted(set(spec)-known) if isinstance(spec,dict) else spec))
    def resolve(value):
        return (file.parent/Path(value).expanduser()).resolve()
    require(spec.get("source"),"paths.json 需要 source 源码目录")
    for key in ("source","design","manual","home","index_db","output"):
        if spec.get(key):
            spec[key]=str(resolve(spec[key]))
    for key in ('features','compile_db'):
        if spec.get(key):
            if isinstance(spec[key],str):spec[key]=str(resolve(spec[key]))
            else:
                require(isinstance(spec[key],dict) and spec[key].get('path'),key+' needs a file path')
                spec[key]={**spec[key],'path':str(resolve(spec[key]['path']))}
    for mapping in spec.get('path_maps',[]):
        require(isinstance(mapping,dict) and mapping.get('from') and mapping.get('to'),'path_maps entries need from/to')
        mapping['to']=str(resolve(mapping['to']))
    spec.setdefault("home",str(resolve("workspace")))
    spec["repository_roots"]={k:str(resolve(v)) for k,v in spec.get("repository_roots",{}).items()}
    if spec.get("product_adapter"):
        from .product_adapter import load
        value = spec["product_adapter"]
        if isinstance(value, str) and ("/" in value or "\\" in value or value.endswith(".json")):
            value = str(resolve(value))
        spec["product_adapter"] = load(value)
    if isinstance(spec.get('learning_policy'),str) and (spec['learning_policy'].endswith('.json') or '/' in spec['learning_policy'] or '\\' in spec['learning_policy']):
        spec['learning_policy']=str(resolve(spec['learning_policy']))
    return spec


def check(spec):
    from .ecs import index_path
    from .graph_mount import inspect_input
    require(Path(spec["source"]).is_dir(),"源码目录不存在："+spec["source"])
    home=Path(spec["home"])
    extra=[spec[k]['path'] if isinstance(spec[k],dict) else spec[k] for k in ('features','compile_db') if spec.get(k)]
    for path in [spec["source"],*spec.get("repository_roots",{}).values(),*[spec[k] for k in ("manual","design") if spec.get(k)],*extra]:
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
            "compile_database":"provided_unparsed" if spec.get('compile_db') else 'not_provided',
            "historical_features":"provided" if spec.get('features') else 'not_provided',
            "python":sys.executable,"sqlite":sqlite3.sqlite_version,"git":shutil.which("git"),
            "database":str(home/"knowledge.sqlite3"),"wiki":str(home/"wiki/index.html")}


def start(spec, refresh):
    from init_internal_project import create
    info = check(spec)
    graph = info["graph"] or {}
    home = Path(spec["home"])
    from . import whole
    from .inputs import prepare
    manifest=prepare(spec,home/'setup/inputs')
    learning=whole.policy(spec.get('learning_policy'),spec.get('product_adapter') if isinstance(spec.get('product_adapter'),dict) else None)
    learning=whole.policy({**learning,'curriculum_protocol':'module-feature/v2.4'})
    signature=digest(["module-curriculum/v2.4",spec,manifest['digest'],learning['digest'],graph.get("run_id"),str(ROOT),sys.executable])
    if not refresh and (home/"knowledge.sqlite3").is_file():
        with Store(home,readonly=True,graph_override=spec.get("index_db")) as store:
            bound=store.get_meta("project_entry",{})
            if bound.get("signature")==signature and store.get_meta("study_head")==bound.get("plan_id") and Path(bound["mcp"]).is_file():
                return {**bound,**info,"query_mcp":query_config(home,bound["mcp"]),"action":"继续已冻结的学习快照。材料更新时用 start --refresh。"}
    args=argparse.Namespace(source=Path(spec["source"]),home=home,output=home/"setup/project.json",
         index_db=spec.get("index_db"),run_id=graph.get("run_id"),graph_storage=graph.get("storage"),
         product=spec.get("product","GaussDB"),revision=spec.get("revision","content-addressed"),
         design=Path(spec["design"]) if spec.get("design") else None,manual=Path(spec["manual"]) if spec.get("manual") else None,
         compile_db=Path(manifest['normalized_compile_db']) if manifest.get('normalized_compile_db') and not graph else None,
         profile=spec.get('build_profile','declared-build'),input_materials=manifest['materials'],
         repository_roots=spec.get("repository_roots",{}),module_prefix=spec.get("module_prefixes",[]),
         product_adapter=spec.get("product_adapter"),
         learning_policy=learning,
         role="researcher",workspace_setup=True,source_only=not graph)
    result=create(args)
    with Store(home) as store:
        plan=study.current(store)
        for kind in ('features','compile_db'):
            info_item=manifest['inputs'].get(kind)
            if info_item:
                repo='historical_features' if kind=='features' else 'compile_database'
                asset=store.asset(plan['snapshot'],repo+'/'+Path(info_item['path']).name)
                require(asset['sha']==info_item['sha256'],'Input changed during snapshot; run start --refresh with stable files')
        mcp=home/"researcher.mcp.json"
        atomic_write(mcp,Path(result["mcp"]).read_bytes())
        whole.ensure(store,learning)
        with store.transaction():store.set_meta('learning_inputs',manifest)
        from . import curriculum
        course=curriculum.ensure(store,manifest,spec.get('curriculum'))
        course_export=curriculum.export(store)
        exported=whole.export(store)
        bound={"signature":signature,"plan_id":plan["id"],"plan":result["study_plan"],"run":plan["run"],
               "modules":len(plan["modules"]),"candidates":len(plan.get("candidates",[])),"mcp":str(mcp),
               "query_mcp":query_config(home,mcp),"source_snapshot":plan["snapshot"],"whole_plan":exported,
               "curriculum":course_export,"input_manifest":manifest['manifest_path'],"input_summary":manifest['summary'],
               "learning_packages":len(course['packages']),"tu_parsing":"not_run_on_start"}
        with store.transaction():
            store.set_meta("project_entry",bound)
    return {**info,**bound,"graph":result.get("graph"),"action":"打开 curriculum.html 查看领域、模块、机制工作包和全部文件义务。在当前 Claude 使用 /gauss-knowledge，选模块后串行或原生 subagent 学习；审阅后继续。compile_db 仅登记构建上下文，产图使用 graph-job 提示的 ECS 工具。"}


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
    if not result.get('claims'):
        from . import whole
        require(result.get('progress'),'Planning-only task has no coverage report')
        return {'status':'planning_accepted','task':args.task,'advance':whole.advance(store),'plan':whole.export(store)}
    proposal=team.propose_task(store,args.task)
    if not args.accept:
        ctx=knowledge.review_context(store,proposal["id"],args.reviewer,max_chars=1000000)
        return {"stage":"knowledge","task":args.task,"proposal":proposal["id"],"digest":ctx["proposal_digest"],
                "units":proposal["units"],"evidence":ctx["evidence"],"truncated":ctx["truncated"],
                "next":"审阅知识提案和引用，认可后用此提案的新 digest 执行同一 review 命令。"}
    rev=knowledge.review(store,proposal["id"],{**decision,"proposal_digest":args.accept})
    from . import whole
    extra={'advance':whole.advance(store),'whole_plan':whole.export(store)} if whole.current(store,False) else {}
    return {"status":"knowledge_accepted","revision":rev["id"],**extra,"next":"运行 wiki 打开已审知识，next 继续下一项；coverage 查看验收缺口。"}


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
        if args.action=='curriculum':
            from . import curriculum
            return curriculum.export(store)
        if args.action=='inputs':return store.get_meta('learning_inputs',{})
        if args.action=='graph-job':
            from .graph_job import prepare
            return prepare(store,spec)
        if args.action in {'plan','progress','next','advance','run','coverage','verify-uses','accept-coverage'}:
            from . import whole
            if args.action=='plan':
                from . import curriculum
                baseline=whole.export(store);course=curriculum.export(store) if curriculum.current(store) else {}
                return {**baseline,**course,'curriculum':course,'whole':baseline}
            if args.action=='progress':return whole.status(store,args.module)
            if args.action=='next':return whole.next_task(store,args.worker,args.module)
            if args.action=='advance':return {**whole.advance(store,args.max_tasks),'export':whole.export(store)}
            if args.action=='run':
                from .continuation import run
                return run(store,worker=args.worker,module=args.module,steps=args.steps,timeout=args.timeout,budget=args.budget,executable=args.claude,resume_task=args.resume_task)
            if args.action=='coverage':return whole.audit(store,args.module)
            if args.action=='verify-uses':return whole.verify_uses(store,read_json(args.input))
            if args.action=='accept-coverage':return whole.accept(store,args.digest,args.reviewer,args.notes,args.module)
        if args.action == "plan-tasks":
            from .task_planning import construct
            return construct(store, modules=args.module, max_tasks=args.max_tasks, files_per_task=args.files_per_task, apply=args.apply)
        if args.action == "planning-feedback":
            from .task_planning import propose
            return propose(store, read_json(args.input))
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
            lead=candidate(plan,args.candidate,store) if args.candidate else None
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
            prompt=research_prompt(task,actor,question)
            prompt_file=home/"instructions"/(task.replace(":","-")+".md")
            atomic_write(prompt_file,prompt+"\n")
            return {**work,"worker":actor,"mcp":str(mcp),"claude_command":'claude --mcp-config "'+str(mcp)+'"',
                    "prompt_file":str(prompt_file),"prompt":prompt}
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
        if name in {'progress','next','run','coverage','accept-coverage'}:a.add_argument('--module')
        if name in {'next','run'}:a.add_argument('--worker',required=True)
        if name=='advance':a.add_argument('--max-tasks',type=int,default=8)
        if name=='run':
            a.add_argument('--steps',type=int,default=1);a.add_argument('--timeout',type=int,default=1800)
            a.add_argument('--budget',type=float,default=3);a.add_argument('--claude',type=Path)
            a.add_argument('--resume-task')
        if name=='verify-uses':a.add_argument('--input',required=True,type=Path)
        if name=='accept-coverage':
            a.add_argument('--digest',required=True);a.add_argument('--reviewer',required=True);a.add_argument('--notes',required=True)
        if name == "plan-tasks":
            a.add_argument("--module", action="append")
            a.add_argument("--max-tasks", type=int, default=20)
            a.add_argument("--files-per-task", type=int, default=12)
            a.add_argument("--apply", action="store_true")
        if name == "planning-feedback":
            a.add_argument("--input", type=Path, required=True)
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
