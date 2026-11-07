"""Versioned, data-only product conventions; never execute code found in a repository."""
from fnmatch import fnmatchcase
from pathlib import Path, PurePosixPath
import re

from .store import digest, read_json, require

ROOT = Path(__file__).resolve().parents[2] / "adapters" / "products"
TOPICS = ("errors", "memory", "compatibility", "guc")


def load(spec=None, *, _stack=()):
    """Resolve a built-in name, JSON path or embedded adapter to an immutable value."""
    if isinstance(spec, dict):
        raw = dict(spec)
    else:
        name = str(spec or "postgres-family")
        path = ROOT / (name + ".json") if re.fullmatch(r"[a-z][a-z0-9-]*", name) else Path(name)
        raw = read_json(path)
    require(isinstance(raw, dict), "Product adapter must be an object")
    require(raw.get("schema") == "source-product-adapter/v1", "Unsupported product adapter schema")
    require(isinstance(raw.get("id"), str) and raw["id"] and raw.get("version"), "Adapter identity/version required")
    require(raw["id"] not in _stack and len(_stack) < 8, "Cyclic product adapter inheritance")
    base = load(raw["extends"], _stack=(*_stack, raw["id"])) if raw.get("extends") else {}
    value = {**base, **{k: v for k, v in raw.items() if k not in {"extends", "digest"}}}
    for name in ("module_markers", "expand_dirs", "test_directories"):
        require(isinstance(value.get(name, []), list) and all(isinstance(x, str) for x in value.get(name, [])), "Invalid adapter " + name)
    rules = value.get("module_rules", [])
    require(isinstance(rules, list), "module_rules must be a list")
    for rule in rules:
        require(isinstance(rule, dict) and isinstance(rule.get("id"), str) and "/" in rule["id"], "Module ID must include repository prefix")
        require(isinstance(rule.get("patterns"), list) and rule["patterns"] and all(isinstance(p, str) for p in rule["patterns"]), "Module patterns required")
    detectors = value.get("detectors", [])
    require(isinstance(detectors, list) and len(detectors) <= 100, "Invalid detector count")
    ids = set()
    for row in detectors:
        require(row.get("id") and row["id"] not in ids, "Duplicate detector identity")
        ids.add(row["id"])
        require(row.get("scope") in {"candidate", "signal"}, "Detector scope must be candidate or signal")
        require(row.get("topic") in {*TOPICS, "build", "feature"}, "Unknown detector topic")
        require(row["scope"] != "signal" or row["topic"] != "feature", "Feature detectors must produce candidates")
        require(isinstance(row.get("extensions"), list) and row["extensions"], "Detector extensions required")
        require(isinstance(row.get("kind"), str), "Detector kind required")
        require(isinstance(row.get("pattern"), str) and len(row["pattern"]) <= 2000, "Invalid detector pattern")
        try:
            expression = re.compile(row["pattern"])
        except re.error as exc:
            raise ValueError("Invalid detector regex: " + row["id"]) from exc
        require("name" in expression.groupindex, "Detector requires a named 'name' capture")
    value.pop("digest", None)
    value["digest"] = digest(value)
    return value


def module_for(adapter, repo, path):
    key = repo + "/" + path
    matches = {r["id"] for r in adapter.get("module_rules", []) if any(fnmatchcase(key, p) for p in r["patterns"])}
    require(len(matches) <= 1, "Ambiguous module ownership for " + key + ": " + str(sorted(matches)))
    if matches:
        owner = next(iter(matches))
        require(owner.split("/", 1)[0] == repo, "Module ownership cannot change repository identity")
        return owner
    dirs = list(PurePosixPath(path).parts[:-1])
    if not dirs:
        return repo + "/@root"
    start = next((dirs.index(m) + 1 for m in adapter.get("module_markers", []) if m in dirs), 0)
    end = min(len(dirs), start + 1)
    if end and dirs[end - 1] in adapter.get("expand_dirs", []):
        end = min(len(dirs), end + 1)
    return "/".join([repo, *dirs[:end]])


def expressions(adapter, scope):
    return [(r, re.compile(r["pattern"])) for r in adapter.get("detectors", []) if r["scope"] == scope]


def signals(store, snapshot, groups, adapter, *, per_topic=12, max_bytes=2_000_000):
    """Bounded evidence seeds, never conclusions about topic applicability or macro activation."""
    assets = {a["key"]: a for a in snapshot["assets"]}
    patterns = expressions(adapter, "signal")
    result, gaps = {}, []
    for module, keys in sorted(groups.items()):
        topics = {t: {"status": "unknown", "evidence": [], "sample_limited": False} for t in (*TOPICS, "build")}
        for key in sorted(keys):
            asset = assets[key]
            selected = [(r, exp) for r, exp in patterns if PurePosixPath(key).suffix.lower() in r["extensions"]]
            if not selected or asset["status"] != "frozen":
                continue
            if asset.get("bytes", 0) > max_bytes:
                gaps.append({"asset": key, "reason": "signal_scan_size_budget"})
                continue
            text = store.blob(asset["sha"]).decode("utf-8", errors="replace")
            for rule, expression in selected:
                topic = topics[rule["topic"]]
                if len(topic["evidence"]) >= per_topic:
                    topic["sample_limited"] = True
                    continue
                for found in expression.finditer(text):
                    if len(topic["evidence"]) >= per_topic:
                        topic["sample_limited"] = True
                        break
                    line = text.count("\n", 0, found.start()) + 1
                    topic["evidence"].append({"asset": key, "start": line, "end": line, "detector": rule["id"], "name": found.group("name")})
        for topic in topics.values():
            topic["reason"] = "Lexical leads require source verification" if topic["evidence"] else "No sampled lead; absence has not been established"
        result[module] = topics
    return result, gaps
