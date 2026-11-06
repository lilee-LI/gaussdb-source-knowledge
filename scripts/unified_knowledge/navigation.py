"""Use the installed CodeGraph CLI and its existing project index for navigation."""
import json
from pathlib import Path
import shutil
import subprocess

from .store import digest, require


def available(root):
    return bool(shutil.which("codegraph") and (Path(root) / ".codegraph/codegraph.db").is_file())


def _command():
    binary = shutil.which("codegraph")
    require(binary, "Install the optional CodeGraph CLI or use focus for scoped Tree-sitter/Clang navigation")
    path = Path(binary)
    if path.suffix.lower() in {".cmd", ".ps1", ".bat"}:
        node = shutil.which("node")
        shim = path.parent / "node_modules/@colbymchenry/codegraph/npm-shim.js"
        require(node and shim.is_file(), "CodeGraph npm launcher missing")
        return [node, str(shim)]
    return [binary]


def navigate(store, snapshot, symbol, direction="forward", limit=20, repository=None):
    require(isinstance(symbol, str) and symbol.strip() and not symbol.startswith("-"), "Supply a function name")
    require(direction in {"forward", "reverse"} and type(limit) is int and 1 <= limit <= 100, "Invalid navigation bounds")
    repos = [r for r in store.record("snapshots", snapshot)["materials"] if r["kind"] == "source"]
    repo = next((r for r in repos if r["id"] == repository), None) if repository else repos[0]
    require(repo, "Repository missing from snapshot")
    root = Path(repo["root"]).resolve()
    require(available(root), "An existing CodeGraph CLI/index is required for this navigation provider")
    action = "callees" if direction == "forward" else "callers"

    def run(op):
        proc = subprocess.run([*_command(), op, symbol, "--path", str(root), "--json", "--limit", str(limit)],
                              capture_output=True, encoding="utf-8", errors="replace", timeout=60)
        require(proc.returncode == 0, "CodeGraph query failed: " + proc.stderr[-600:])
        try:
            return json.loads(proc.stdout)
        except ValueError:
            raise ValueError("CodeGraph did not return structured navigation results") from None

    def location(node):
        rel = node.get("filePath", "")
        path = (root / rel).resolve()
        if not rel or not path.is_relative_to(root):
            return {"name": node.get("name"), "status": "outside_snapshot"}
        key = repo["id"] + "/" + path.relative_to(root).as_posix()
        item = store.db.execute("SELECT sha,status FROM assets WHERE snapshot=? AND key=?", (snapshot, key)).fetchone()
        line = node.get("startLine")
        verified = (item and item["status"] == "frozen" and path.is_file() and digest(path.read_bytes()) == item["sha"]
                    and type(line) is int and 1 <= line <= len(store.source_lines(item["sha"])))
        return {"name": node.get("name"), "asset": key, "line": line, "sha": item["sha"] if verified else None,
                "status": "candidate" if verified else "stale_or_unbound"}

    matches = [location(item["node"]) for item in run("query") if item.get("node", {}).get("name") == symbol]
    neighbors = [location(node) for node in run(action).get(action, [])]
    return {"provider": "@colbymchenry/codegraph", "snapshot": snapshot, "symbol": symbol,
            "direction": direction, "matches": matches, "neighbors": neighbors, "resolution": "candidate",
            "next": "按文件与行号读取冻结证据，需要构建语义时再选择相关 TU。"}
