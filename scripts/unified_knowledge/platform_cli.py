"""Platform commands over the existing workspace and reviewed knowledge engine."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys

from .store import Store, atomic_write, canonical, read_json, require


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, required=True)
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("manifest")
    commands.add_parser("releases")
    prepare = commands.add_parser("prepare")
    prepare.add_argument("--provider", type=Path)
    prepare.add_argument("--revision")
    sync = commands.add_parser("sync")
    sync.add_argument("--release", required=True)
    sync.add_argument("--max-documents", type=int, default=100)
    activate = commands.add_parser("activate")
    activate.add_argument("--release", required=True)
    activate.add_argument("--expected-active")
    query = commands.add_parser("query")
    query.add_argument("--question", required=True)
    query.add_argument("--release")
    query.add_argument("--target", action="append", default=[])
    query.add_argument("--max-bytes", type=int, default=60000)
    query.add_argument("--limit", type=int, default=20)
    evaluate = commands.add_parser("evaluate")
    evaluate.add_argument("--dataset", type=Path, required=True)
    evaluate.add_argument("--release")
    evaluate.add_argument("--split", choices=["development","acceptance"], default="acceptance")
    evaluate.add_argument("--output", type=Path, required=True)
    serve = commands.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument("--token-env")
    serve.add_argument("--allow-release", action="append")
    args = parser.parse_args(argv)
    try:
        if args.action == "serve":
            import uvicorn
            from .gateway import create_app
            require(args.host in {"127.0.0.1","::1","localhost"} or args.token_env, "Non-loopback serving requires --token-env or a loopback reverse proxy")
            uvicorn.run(create_app(args.home, token_env=args.token_env, allowed_releases=args.allow_release), host=args.host, port=args.port, log_level="info")
            return 0
        from . import publication
        readonly = args.action in {"manifest","releases","query","evaluate"}
        with Store(args.home, readonly=readonly) as store:
            if args.action == "manifest":
                from .study import current
                from .query_api import source_manifest
                result = source_manifest(store, current(store))
            elif args.action == "releases":
                result = publication.catalog(store)
            elif args.action == "prepare":
                result = publication.prepare(store, provider=read_json(args.provider) if args.provider else None, revision=args.revision)
            elif args.action == "sync":
                result = publication.sync(store, args.release, max_documents=args.max_documents)
            elif args.action == "activate":
                result = publication.activate(store, args.release, expected_active=args.expected_active)
            elif args.action == "query":
                from .retrieval_pipeline import context
                result = context(store, args.question, release_id=args.release, targets=args.target, max_bytes=args.max_bytes, limit=args.limit)
            elif args.action == "evaluate":
                from .evaluation import evaluate
                result = evaluate(store, read_json(args.dataset), release_id=args.release, split=args.split)
                atomic_write(args.output, canonical(result) + "\n")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, sqlite3.Error) as exc:
        print(json.dumps({"error":str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
