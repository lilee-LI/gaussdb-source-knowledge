"""Configure source, documents and the optional build database, then open a lightweight study plan."""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

from unified_knowledge.store import Store, atomic_write, digest, read_json, require
from unified_knowledge.study import inventory
from unified_skill_methods import prepare


def create(args):
    root = Path(__file__).resolve().parents[1]
    source, home = args.source.expanduser().resolve(), args.home.expanduser().resolve()
    require(source.is_dir(), "Provide the local source directory")
    output = args.output.expanduser().resolve()
    repo = {"id": "server", "root": str(source), "exclude": [
        "*.o", "*.obj", "*.a", "*.lib", "*.pdb", "*.dll", "*.so", "*.so.*", "*.exe", "*.whl",
        "compile_commands.json", "*/compile_commands.json"]}
    index_db, run_id = getattr(args, "index_db", None), getattr(args, "run_id", None)
    require(index_db or not run_id, "填写 run_id 时必须同时提供 index_db")
    if index_db:
        from unified_knowledge.ecs import index_path
        index_db = index_path(index_db, home)
        require(not args.compile_db, "ECS already supplied the index; configure the run ID instead of a compilation database")
    config = {"product": args.product, "revision": args.revision, "repositories": [repo], "materials": [],
              "methods": [], "profiles": [], "ownership": [], "module_prefixes": getattr(args, "module_prefix", [])}
    if getattr(args, "product_adapter", None):
        from unified_knowledge.product_adapter import load
        config["product_adapter"] = load(args.product_adapter)
    if getattr(args,"learning_policy",None):
        config["learning_policy"]=args.learning_policy
    if index_db:
        from unified_knowledge.graph_mount import inspect_input
        run_id = inspect_input(index_db,run_id)["run_id"]
        config["ecs_index"] = {"database":str(index_db),"run_id":run_id}
        if getattr(args,"graph_storage",None):
            config["ecs_index"]["graph_storage"] = args.graph_storage
        for repo_id, path in getattr(args, "repository_roots", {}).items():
            config["repositories"].append({"id":repo_id,"root":str(Path(path).resolve())})
    for name, path in (("design", args.design), ("manual", args.manual)):
        if path:
            path = path.expanduser().resolve()
            require(path.exists(), "Material directory/file missing: " + name)
            config["materials"].append({"id": name, "path": str(path), "material_kind": name,
                                        "status": "unreviewed", "revision": "user-material-snapshot"})
    config['materials'].extend(getattr(args,'input_materials',[]))
    if args.compile_db:
        path = args.compile_db.expanduser().resolve()
        require(path.is_file(), "Compilation database missing: " + str(path))
        config["profiles"].append({"id": args.profile, "repository": "server",
                                   "compile_commands": str(path), "extra_arguments": []})
    methods = prepare({"protocol": "unified-skill/v1", "scope": "Whole-repository discovery; select specialist methods for each feature",
                       "topic_decisions": {}}, config)
    config = methods["config"]
    python = Path(sys.executable).absolute()
    mcp = {"mcpServers": {"gaussdb_knowledge": {"command": str(python),
           "args": ["-X", "utf8", str(root / "scripts/unified_kb.py"), "--home", str(home),
                    "serve", "--transport", "stdio", "--role", args.role]}}}
    if getattr(args,"workspace_setup",False):
        output = home/"setup"/digest([config,str(python),args.role])[:20]/"project.json"
    mcp_path = output.with_name(output.stem + ".mcp.json")
    method_path = output.with_name(output.stem + ".methods.json")
    artifacts = {output: config, mcp_path: mcp, method_path: methods}
    for path, data in artifacts.items():
        require(not path.exists() or read_json(path) == data, "Existing configuration differs; choose a new --output: " + str(path))
    with Store(home,graph_override=index_db) as store:
        if index_db:
            from unified_knowledge.ecs import connect
            result = connect(store, config)
        else:
            result = inventory(store, config, source_only=getattr(args,"source_only",False))
    for path, data in artifacts.items():
        if not path.exists():
            atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    guide = result["study_plan"]
    return {"project": str(output), "mcp": str(mcp_path), "methods": str(method_path), "home": str(home),
            "profile": guide["profile"], "study_plan": guide["plan_file"], "modules": len(guide["modules"]),
            "frontend_invocations": 0, "graph":result.get("graph"), "study_run":guide["study_run"], "source_index":guide.get("source_index"), "seconds": result["seconds"], "next": guide["next"]}


def main():
    import sys
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--paths", type=Path, help="JSON file containing local paths, index_db and run_id")
    for name in ("source","design","manual","index-db","compile-db","output","home"):
        p.add_argument("--" + name, type=Path)
    p.add_argument("--profile", default="target-build"); p.add_argument("--product", default="GaussDB")
    p.add_argument("--revision", default="content-addressed"); p.add_argument("--run-id")
    p.add_argument("--module-prefix", action="append", default=[])
    p.add_argument("--role", choices=("query","researcher","reviewer"), default="researcher")
    args = p.parse_args()
    try:
        if args.paths:
            spec = read_json(args.paths)
            allowed = {"source","design","manual","index_db","run_id","output","home","module_prefixes","repository_roots","graph_storage"}
            require(isinstance(spec, dict) and not set(spec) - allowed, "Unsupported keys in paths file")
            for name in ("source","design","manual","index_db","output","home"):
                if getattr(args, name) is None and spec.get(name):
                    setattr(args,name,(args.paths.resolve().parent / spec[name]).resolve())
            args.run_id = args.run_id or spec.get("run_id")
            args.graph_storage = spec.get("graph_storage")
            args.module_prefix = args.module_prefix or spec.get("module_prefixes", [])
            args.repository_roots = {k:(args.paths.resolve().parent / v).resolve() for k,v in spec.get("repository_roots", {}).items()}
        require(args.source, "Provide --source or a source path in --paths")
        args.home = args.home or Path("state/gaussdb")
        args.output = args.output or Path("local/gaussdb.json")
        if (Path(__file__).resolve().parents[1] / "ECS-EDITION").is_file():
            require(args.index_db, "请提供 ECS 的 index_db；仅有源码时使用 kb start。")
        print(json.dumps(create(args),ensure_ascii=False,indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as error:
        print(json.dumps({"error":str(error)},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
