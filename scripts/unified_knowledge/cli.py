"""Unified CLI for source indexing, research, knowledge, task context and releases."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__, study, team
from .changes import analyze_change
from .indexer import build_index, query_graph
from .knowledge import knowledge_graph, propose, review, review_context
from .materials import ingest
from .planner import (create_task_evidence, finish_research, lease, next_tasks, plan, read_for_task,
                      review_task, stage_research_unit, submit, task_context, task_status)
from .releases import activate, doctor, publish, status, verify
from .retrieval import explain_path, get_context, import_vectors, knowledge_delta, request_refresh, search
from .store import Store, canonical, read_json


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--home", required=True, type=Path)
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command", required=True)
    q = sub.add_parser("doctor"); q.add_argument("--repair-git", action="store_true"); q.add_argument("--verify-blobs", action="store_true")
    q = sub.add_parser("ingest"); q.add_argument("--config", required=True, type=Path)
    q = sub.add_parser("pipeline"); q.add_argument("--config", required=True, type=Path); q.add_argument("--profile"); q.add_argument("--timeout", type=int, default=120); q.add_argument("--ctags", type=Path)
    q = sub.add_parser("index"); q.add_argument("--snapshot", required=True); q.add_argument("--profile"); q.add_argument("--timeout", type=int, default=120); q.add_argument("--resume", action="store_true"); q.add_argument("--ctags", type=Path)
    for cmd in ("pipeline", "index"):
        item = sub.choices[cmd]
        item.add_argument("--mode", choices=("inventory", "selected", "full"))
        item.add_argument("--tu", action="append", help="Repository-relative translation unit; repeatable")
        item.add_argument("--jobs", type=int, default=2)
    q = sub.add_parser("navigate"); q.add_argument("--symbol", required=True); q.add_argument("--repository")
    q.add_argument("--direction", choices=("forward","reverse"), default="forward"); q.add_argument("--limit", type=int, default=20)
    q = sub.add_parser("integrate"); q.add_argument("--run", action="append", default=[]); q.add_argument("--profile")
    q = sub.add_parser("guide"); q.add_argument("--module")
    q = sub.add_parser("focus")
    q.add_argument("--module"); q.add_argument("--candidate"); q.add_argument("--tu", action="append", default=[])
    q.add_argument("--limit", type=int, default=12); q.add_argument("--jobs", type=int, default=2)
    q.add_argument("--extend"); q.add_argument("--question"); q.add_argument("--profile"); q.add_argument("--symbol")
    q = sub.add_parser("team"); actions = q.add_subparsers(dest="action", required=True)
    a = actions.add_parser("assign"); a.add_argument("--module", required=True); a.add_argument("--worker", required=True)
    a.add_argument("--out", type=Path); a.add_argument("--kit", type=Path); a.add_argument("--include-asset", action="append", default=[])
    a.add_argument("--replace", action="store_true"); a.add_argument("--reference", action="append", default=[])
    a = actions.add_parser("open"); source = a.add_mutually_exclusive_group(required=True)
    source.add_argument("--order", type=Path); source.add_argument("--kit", type=Path)
    a = actions.add_parser("export"); a.add_argument("--order", type=Path)
    a.add_argument("--task", required=True); a.add_argument("--out", required=True, type=Path)
    a = actions.add_parser("receive"); a.add_argument("--input", required=True, type=Path); a.add_argument("--jobs", type=int, default=2)
    a = actions.add_parser("propose"); a.add_argument("--task", required=True)
    q = sub.add_parser("plan"); q.add_argument("--run"); q.add_argument("--targets", nargs="*"); q.add_argument("--question"); q.add_argument("--max-symbols", type=int, default=12)
    q.add_argument("--granularity", choices=("auto","module"), default="auto"); q.add_argument("--preview",action="store_true")
    q = sub.add_parser("anchor"); q.add_argument("--snapshot", required=True); q.add_argument("--asset", required=True); q.add_argument("--start", required=True, type=int); q.add_argument("--end", required=True, type=int)
    q = sub.add_parser("evidence"); q.add_argument("--id", required=True); q.add_argument("--expected-hash"); q.add_argument("--max-chars", type=int, default=30000)
    q = sub.add_parser("status"); q.add_argument("--run")
    q = sub.add_parser("graph"); q.add_argument("--run", required=True); q.add_argument("--targets", nargs="+", required=True); q.add_argument("--direction", default="both"); q.add_argument("--depth", type=int, default=1); q.add_argument("--limit", type=int, default=100)
    q.add_argument("--kind", action="append"); q.add_argument("--walk", choices=("dfs", "bfs"))
    for name in ("context", "find", "explain", "request-refresh"):
        q = sub.add_parser(name); q.add_argument("--input", required=True, type=Path)
    q = sub.add_parser("knowledge-graph"); q.add_argument("--revision")
    q = sub.add_parser("knowledge-delta"); q.add_argument("--base", required=True); q.add_argument("--target", required=True)
    q = sub.add_parser("vectors"); q.add_argument("--revision", required=True); q.add_argument("--space", required=True); q.add_argument("--input", required=True, type=Path)
    q = sub.add_parser("change"); q.add_argument("--base-run", required=True); q.add_argument("--target-run", required=True); q.add_argument("--revision"); q.add_argument("--diff-file", type=Path); q.add_argument("--no-enqueue", action="store_true")
    q = sub.add_parser("publish"); q.add_argument("--output", required=True, type=Path); q.add_argument("--revision"); q.add_argument("--allow-partial", action="store_true")
    q = sub.add_parser("verify"); q.add_argument("--output", required=True, type=Path); q.add_argument("--require-current", action="store_true")
    q = sub.add_parser("activate"); q.add_argument("--output", required=True, type=Path)
    q = sub.add_parser("serve"); q.add_argument("--transport", choices=("stdio", "http"), default="stdio"); q.add_argument("--host", default="127.0.0.1"); q.add_argument("--port", type=int, default=8791); q.add_argument("--role", choices=("query", "researcher", "reviewer"), default="query")
    q = sub.add_parser("knowledge"); actions = q.add_subparsers(dest="action", required=True)
    a = actions.add_parser("propose"); a.add_argument("--input", required=True, type=Path)
    a = actions.add_parser("review-context"); a.add_argument("--id", required=True); a.add_argument("--reviewer", required=True); a.add_argument("--max-chars", type=int, default=100000)
    a = actions.add_parser("review"); a.add_argument("--id", required=True); a.add_argument("--input", required=True, type=Path)
    q = sub.add_parser("task"); actions = q.add_subparsers(dest="action", required=True)
    a = actions.add_parser("next"); a.add_argument("--run", required=True); a.add_argument("--limit", type=int, default=20)
    for name in ("context", "status"):
        a = actions.add_parser(name); a.add_argument("--id", required=True)
    for name in ("claim", "renew", "release", "checkpoint", "read", "submit"):
        a = actions.add_parser(name); a.add_argument("--id", required=True); a.add_argument("--worker", required=True)
        if name != "claim":
            a.add_argument("--token", required=True)
        if name in ("claim", "renew"):
            a.add_argument("--seconds", type=int, default=1800)
        if name in ("checkpoint", "submit"):
            a.add_argument("--input", required=True, type=Path)
        if name == "read":
            a.add_argument("--evidence", required=True); a.add_argument("--max-chars", type=int, default=100000)
    a = actions.add_parser("review"); a.add_argument("--id", required=True); a.add_argument("--input", required=True, type=Path)
    a = actions.add_parser("propose"); a.add_argument("--id", required=True)
    for action in ("anchor", "stage", "finish"):
        a = actions.add_parser(action)
        a.add_argument("--id", required=True); a.add_argument("--worker", required=True); a.add_argument("--token", required=True)
        if action == "anchor":
            a.add_argument("--asset", required=True); a.add_argument("--start", required=True, type=int); a.add_argument("--end", required=True, type=int)
        else:
            a.add_argument("--input", required=True, type=Path)
            if action == "stage":
                a.add_argument("--previous-hash")
            else:
                a.add_argument("--drafts-digest", required=True)
    q = sub.add_parser("worker"); actions = q.add_subparsers(dest="action", required=True)
    for name in ("prepare-codewiki", "run-codewiki", "structured", "receive-structured", "propose"):
        a = actions.add_parser(name); a.add_argument("--task", required=True); a.add_argument("--worker", required=True)
        if name != "propose":
            a.add_argument("--token", required=True)
        if name == "prepare-codewiki":
            a.add_argument("--config", required=True, type=Path)
        if name == "run-codewiki":
            a.add_argument("--rounds", type=int, default=2); a.add_argument("--timeout", type=int, default=3600)
        if name in {"structured", "receive-structured"}:
            a.add_argument("--attempt-name", default="structured")
    return p


def dispatch(store, args):
    command = args.command
    if command == "doctor":
        return doctor(store, repair_git=args.repair_git, verify_blobs=args.verify_blobs)
    if command == "ingest":
        value = ingest(store, read_json(args.config))
        return {"id": value["id"], "assets": len(value["assets"]), "profiles": [p["id"] for p in value["profiles"]], "database_execution": "not_run"}
    if command in {"pipeline", "index"}:
        mode = args.mode or ("selected" if args.tu else "inventory")
        if (mode == "selected") != bool(args.tu):
            raise ValueError("Use --tu for selected mode only")
        config = read_json(args.config) if command == "pipeline" else {}
        if config.get("ecs_index"):
            from .ecs import connect
            if args.tu or mode != "inventory":
                raise ValueError("Use the ECS run as supplied; focus selects its existing symbols")
            return connect(store, config, requested_profile=args.profile)
        if getattr(args,"snapshot",None) and store.record("snapshots",args.snapshot).get("source_index"):
            raise ValueError("This snapshot uses an imported ECS index; use guide or focus")
        if mode == "inventory":
            return study.inventory(store, config, args.profile, getattr(args, "snapshot", None))
        snapshot = ingest(store, config) if command == "pipeline" else store.record("snapshots", args.snapshot)
        profiles = [args.profile] if args.profile else [p["id"] for p in snapshot["profiles"] if p["id"] != "unknown"]
        batches = []
        for profile in profiles or ["unknown"]:
            run = build_index(store, snapshot["id"], profile, timeout=args.timeout,
                              resume=command == "pipeline" or args.resume, ctags=args.ctags, files=args.tu, jobs=args.jobs)
            if command == "index":
                return run
            course = plan(store, run["id"])
            batches.append({"index": run, "plan": course, "next_tasks": next_tasks(store, run["id"], limit=5)})
        return {"snapshot": snapshot["id"], "batches": batches, "status": "awaiting_actual_research_and_review",
                "automatic_semantic_completion": False, "database_execution": "not_run"}
    if command == "navigate":
        from .navigation import navigate
        p = study.current(store)
        if p.get("source_index") or p.get("reuse_index") or p.get("source_only"):
            return study.ecs_neighbors(store, p, args.symbol, args.direction, args.limit)
        return navigate(store, p["snapshot"], args.symbol, args.direction, args.limit, args.repository)
    if command == "integrate":
        plan_value = study.current(store)
        if plan_value.get("source_index") or plan_value.get("reuse_index"):
            r = store.record("runs",plan_value["run"])
            if args.run or (args.profile and args.profile != r["profile"]):
                raise ValueError("This plan uses one bound ECS run")
            return {"id":r["id"],"profile":r["profile"],"source_index":r.get("source_index"),"coverage":r["coverage"],
                    "status":r["status"],"frontend_invocations":0}
        from .assembly import integrate
        r = integrate(store, args.run, args.profile)
        return {k: r[k] for k in ("id", "profile", "inputs", "status", "coverage", "frontend_invocations")}
    if command == "guide":
        result = study.guide(store)
        if args.module:
            result["module_details"] = study.module_guide(store, args.module)
        return result
    if command == "focus":
        return study.focus(store, args.module, files=args.tu, limit=args.limit, jobs=args.jobs, extend=args.extend,
                           question=args.question, profile=args.profile, symbol=args.symbol, candidate_id=args.candidate)
    if command == "team":
        if args.action == "assign":
            if not args.out and not args.kit:
                raise ValueError("Specify --kit or --out")
            if args.kit:
                if args.kit.suffix.lower() != ".zip":
                    raise ValueError("Use a .zip filename for the module kit")
                plan_value = study.current(store)
                for key in args.include_asset:
                    store.asset(plan_value["snapshot"], key)
            order = args.out or args.kit.with_suffix(".order.json")
            result = team.assign(store, args.module, args.worker, order, args.replace, args.reference)
            if args.kit:
                from .workkit import pack
                result["kit"] = pack(store, order, args.kit, args.include_asset)
            return result
        if args.action == "open":
            return team.open_order(store, args.order)
        if args.action == "export":
            return team.export_result(store, args.order or store.home/"order.json", args.task, args.out)
        if args.action == "receive":
            return team.receive(store, args.input, args.jobs)
        return team.propose_task(store, args.task)
    if command == "plan":
        if args.preview:
            if args.targets or args.question:
                raise ValueError("--preview describes the whole-run queue; omit --targets and --question")
            from .course import preview, queue_runs
            return preview(store,args.run,args.granularity) if args.run else queue_runs(store)
        if not args.run:
            raise ValueError("Select the learning run with plan --preview, then pass --run")
        return plan(store, args.run, targets=args.targets, question=args.question, max_symbols=args.max_symbols, granularity=args.granularity)
    if command == "anchor":
        with store.transaction():
            return store.anchor(args.snapshot, args.asset, args.start, args.end)
    if command == "evidence":
        return store.read_evidence(args.id, expected_hash=args.expected_hash, max_chars=args.max_chars)
    if command == "status":
        return status(store, run=args.run)
    if command == "graph":
        from .planner import resolve_targets
        nodes, missing = resolve_targets(store, args.run, args.targets)
        return {**query_graph(store, args.run, nodes, direction=args.direction, depth=args.depth, limit=args.limit,
                              kinds=args.kind, walk=args.walk), "unresolved_targets": missing}
    if command in {"context", "find", "explain", "request-refresh"}:
        return {"context": get_context, "find": search, "explain": explain_path, "request-refresh": request_refresh}[command](store, read_json(args.input))
    if command == "knowledge-graph":
        return knowledge_graph(store, args.revision)
    if command == "knowledge-delta":
        return knowledge_delta(store, args.base, args.target)
    if command == "vectors":
        return import_vectors(store, args.revision, args.space, read_json(args.input))
    if command == "change":
        base, target = store.record("runs", args.base_run), store.record("runs", args.target_run)
        return analyze_change(store, base["snapshot"], target["snapshot"], base_run=args.base_run, target_run=args.target_run,
                              revision=args.revision, enqueue=not args.no_enqueue,
                              diff_text=args.diff_file.read_text(encoding="utf-8") if args.diff_file else None)
    if command == "publish":
        return publish(store, args.output, revision=args.revision, allow_partial=args.allow_partial)
    if command == "verify":
        return verify(args.output, current_store=store, require_current=args.require_current)
    if command == "activate":
        return activate(store, args.output)
    if command == "knowledge":
        if args.action == "propose":
            return propose(store, read_json(args.input))
        if args.action == "review-context":
            return review_context(store, args.id, args.reviewer, max_chars=args.max_chars)
        return review(store, args.id, read_json(args.input))
    if command == "task":
        action = args.action
        if action == "next":
            return next_tasks(store, args.run, args.limit)
        if action == "context":
            return task_context(store, args.id)
        if action == "status":
            return task_status(store, args.id)
        if action == "anchor":
            return create_task_evidence(store, args.id, args.worker, args.token, args.asset, args.start, args.end)
        if action == "stage":
            return stage_research_unit(store, args.id, args.worker, args.token, read_json(args.input), args.previous_hash)
        if action == "finish":
            return finish_research(store, args.id, args.worker, args.token, read_json(args.input), args.drafts_digest)
        if action == "propose":
            return team.propose_task(store, args.id)
        if action == "review":
            return review_task(store, args.id, read_json(args.input))
        if action == "read":
            return read_for_task(store, args.id, args.worker, args.token, args.evidence, max_chars=args.max_chars)
        if action == "submit":
            return submit(store, args.id, args.worker, args.token, read_json(args.input))
        return lease(store, args.id, args.worker, seconds=getattr(args, "seconds", 1800), action=action,
                     token=getattr(args, "token", None), checkpoint=read_json(args.input) if getattr(args, "input", None) else None)
    if command == "worker":
        from . import worker
        if args.action == "prepare-codewiki":
            return worker.prepare_codewiki(store, args.task, args.worker, args.token, read_json(args.config))
        if args.action == "run-codewiki":
            return worker.run_codewiki(store, args.task, args.worker, args.token, rounds=args.rounds, timeout=args.timeout)
        if args.action == "structured":
            return worker.run_structured(store, args.task, args.worker, args.token, attempt_name=args.attempt_name)
        if args.action == "receive-structured":
            return worker.receive_structured(store, args.task, args.worker, args.token, attempt_name=args.attempt_name)
        return worker.propose_structured(store, args.task, args.worker)
    raise ValueError("Unknown unified command")


def main(argv=None):
    args = parser().parse_args(argv)
    if args.command == "serve":
        from .service import http_server, stdio
        if args.transport == "stdio":
            stdio(args.home, args.role)
        else:
            server = http_server(args.home, host=args.host, port=args.port, role=args.role)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
        return 0
    try:
        if args.command == "plan" and not (args.home/"knowledge.sqlite3").is_file():
            raise ValueError("Select the existing Windows learning workspace containing knowledge.sqlite3")
        if args.command == "team" and args.action == "open" and args.kit:
            from .workkit import open_kit
            print(json.dumps(open_kit(args.home,args.kit),ensure_ascii=False,indent=2))
            return 0
        if args.command == "index" and (Path(__file__).resolve().parents[2] / "ECS-EDITION").is_file():
            raise ValueError("Use the completed ECS run via init_internal_project.py --paths or pipeline --config")
        if args.command == "pipeline":
            config = read_json(args.config)
            if (Path(__file__).resolve().parents[2] / "ECS-EDITION").is_file() and not config.get("ecs_index"):
                raise ValueError("This edition consumes an ECS knowledge.sqlite3 and run_id")
            if config.get("ecs_index"):
                from .ecs import index_path
                index_path(config["ecs_index"]["database"], args.home)
        query_commands = {"navigate", "context", "find", "explain", "status", "evidence", "graph", "knowledge-graph", "knowledge-delta", "verify"}
        readonly = args.command in query_commands or (args.command == "plan" and args.preview) or (args.command == "doctor" and (args.home/"release.json").is_file() and not args.repair_git)
        with Store(args.home, readonly=readonly) as store:
            result = dispatch(store, args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"error": type(error).__name__, "message": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
