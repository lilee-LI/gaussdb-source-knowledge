"""Build-profile-aware, resumable code facts with independent syntax accounting."""
from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid

from . import tu_cache
from .graph_facts import LegacyCalls, link_calls, traversal
from .materials import CPP
from .store import atomic_write, canonical, digest, identity, now, require


def tool_identity():
    versions = {}
    for package in ("libclang", "tree-sitter", "tree-sitter-cpp", "networkx"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "unavailable"
    versions["adapter"] = digest(Path(__file__).read_bytes())
    versions["clang_worker"] = digest(Path(__file__).with_name("clang_worker.py").read_bytes())
    versions["graph_adapter"] = digest(Path(__file__).with_name("graph_facts.py").read_bytes())
    versions["cache_policy"] = digest(Path(__file__).with_name("tu_cache.py").read_bytes())
    return versions


def materialize(store, snapshot):
    value = store.record("snapshots", snapshot)
    roots = {r["id"]: store.home / "checkouts" / snapshot.replace(":", "-") / r["id"]
             for r in value["materials"] if r["kind"] == "source"}
    for repo, root in roots.items():
        root.mkdir(parents=True, exist_ok=True)
    for row in store.db.execute("SELECT data FROM assets WHERE snapshot=? AND kind='source' AND status='frozen'", (snapshot,)):
        item = json.loads(row[0])
        root = roots[item["repo"]]
        p = (root / item["path"]).resolve()
        require(p.is_relative_to(root), "Snapshot asset path escapes checkout")
        if p.exists():
            require(p.is_file() and digest(p.read_bytes()) == item["sha"], "Frozen analysis checkout was modified")
        else:
            atomic_write(p, store.blob(item["sha"]))
    return roots


def frozen_view(store, snapshot, roots):
    """Make Clang resolve repository files from frozen blobs without copying the tree."""
    entries = {repo: {"type": "directory", "name": str(root), "contents": []} for repo, root in roots.items()}
    directories = {(repo, ()): value for repo, value in entries.items()}
    for row in store.db.execute("SELECT repo,path,sha FROM assets WHERE snapshot=? AND kind='source' AND status='frozen' ORDER BY key", (snapshot,)):
        repo, parts = row["repo"], Path(row["path"]).parts
        require(parts and not Path(row["path"]).is_absolute() and ".." not in parts, "Invalid frozen source location")
        parent = directories[repo, ()]
        for i, component in enumerate(parts[:-1]):
            key = (repo, parts[:i + 1])
            if key not in directories:
                directories[key] = {"type": "directory", "name": component, "contents": []}
                parent["contents"].append(directories[key])
            parent = directories[key]
        parent["contents"].append({"type": "file", "name": parts[-1], "external-contents": str(store.blob_path(row["sha"]))})
    overlay = next(iter(roots.values())).parent / "overlay.json"
    raw = canonical({"version": 0, "use-external-names": False, "roots": list(entries.values())})
    atomic_write(overlay, raw)
    return overlay


def compiler_arguments(entry, profile, originals, roots):
    raw = list(entry["arguments"]) + list(profile.get("extra_arguments", []))
    if raw and Path(raw[0]).stem.lower() in {"ccache", "sccache", "distcc"}:
        raw.pop(0)
    driver = Path(raw[0]).name.lower() if raw else ""
    if raw and not raw[0].startswith("-"):
        raw.pop(0)
    elif raw and Path(raw[0]).name.lower() in {"clang.exe", "clang++.exe", "gcc.exe", "g++.exe", "cl.exe"}:
        raw.pop(0)
    result, skipped, i = [], [], 0
    path_options = {"-I", "-isystem", "-iquote", "-include", "-imacros", "-isysroot", "--sysroot"}
    pair_outputs = {"-o", "-MF", "-MT", "-MQ", "-MJ", "--serialize-diagnostics", "-L", "-l", "-Xlinker"}

    def remap(value):
        p = Path(value)
        if not p.is_absolute():
            p = Path(entry["directory"]) / p
        p = p.resolve()
        for repo, original in originals.items():
            if p.is_relative_to(original):
                return str(roots[repo] / p.relative_to(original))
        return str(p)

    while i < len(raw):
        arg = raw[i]
        if any(arg.startswith(option) and len(arg) > len(option) for option in ("-MF", "-MT", "-MQ", "-MJ")):
            i += 1
            continue
        if arg in pair_outputs:
            i += 2
            continue
        if arg == "-pipe" or arg.startswith(("-Wl,", "-L")) or (arg.startswith("-l") and not arg.startswith(("-load", "-lazy"))):
            i += 1
            continue
        if arg in {"-c", "-S", "-E", "-emit-llvm", "-MD", "-MMD", "-MP", "-MG"}:
            i += 1
            continue
        if arg in {"-D", "-U"}:
            require(i + 1 < len(raw), "Missing macro option value")
            result.append(arg + raw[i + 1])
            i += 2
            continue
        if arg in path_options:
            require(i + 1 < len(raw), "Missing include/path option value")
            result.extend([arg, remap(raw[i + 1])])
            i += 2
            continue
        if any(arg.startswith(name) and len(arg) > len(name) for name in ("-isystem", "-iquote")):
            name = "-isystem" if arg.startswith("-isystem") else "-iquote"
            result.extend([name, remap(arg[len(name):])])
        elif arg.startswith("-I") and len(arg) > 2:
            result.append("-I" + remap(arg[2:]))
        elif arg.startswith("--sysroot="):
            result.append("--sysroot=" + remap(arg.split("=", 1)[1]))
        elif arg.startswith(("-Xclang", "-fplugin", "-load", "@")) or arg in {"-cc1", "-mllvm"}:
            raise ValueError("Unsupported compiler plugin/response/internal flag: " + arg)
        elif arg.startswith(("-D", "-U", "-std=", "-f", "-m", "-W", "-O", "-g", "-pthread", "--target=", "-target", "-x")):
            result.append(arg)
            if arg in {"-x", "-target"}:
                require(i + 1 < len(raw), "Missing frontend option value")
                result.append(raw[i + 1])
                i += 1
        elif arg.startswith("-"):
            skipped.append(arg)
        else:
            try:
                source = (Path(entry["directory"]) / arg).resolve()
                if source.name != Path(entry["file"]).name:
                    skipped.append(arg)
            except OSError:
                skipped.append(arg)
        i += 1
    require(not skipped, "Unrecognized frontend flags need explicit adaptation: " + repr(skipped))
    if Path(entry["file"]).suffix == ".c" and "++" in driver and "-x" not in result and not any(
            s.startswith("-x") for s in result):
        result[:0] = ["-x", "c++"]
    return result


def syntax_candidates(raw, asset):
    text = raw.decode("utf-8", errors="replace")
    symbols, diagnostics = [], []
    try:
        from tree_sitter import Language, Parser
        import tree_sitter_cpp
        tree = Parser(Language(tree_sitter_cpp.language())).parse(raw)
        stack = [tree.root_node]
        while stack:
            node = stack.pop()
            if node.type == "function_definition":
                declarator = node.child_by_field_name("declarator")
                if declarator:
                    todo = [declarator]
                    name = None
                    while todo:
                        item = todo.pop()
                        if item.type in {"identifier", "field_identifier", "operator_name", "destructor_name"}:
                            name = raw[item.start_byte:item.end_byte].decode("utf-8", errors="replace")
                            break
                        todo.extend(reversed(item.named_children))
                    if name:
                        symbols.append({"name": name, "start": node.start_point.row + 1, "end": node.end_point.row + 1,
                                        "asset": asset, "kind": "candidate_function", "resolution": "candidate",
                                        "logical": identity("syntax", [asset, name, node.start_point.row + 1]),
                                        "definition": True, "frontend_selected": False})
            stack.extend(reversed(node.named_children))
        if tree.root_node.has_error:
            diagnostics.append({"mode": "tree_sitter", "asset": asset, "code": "syntax_errors_present"})
    except ImportError:
        diagnostics.append({"mode": "lexical", "asset": asset, "code": "tree_sitter_unavailable"})
        for match in re.finditer(r"(?m)^[\w:*&<>~ \t]+\b([A-Za-z_]\w*)\s*\([^;{}]*\)\s*\{", text):
            start = text[:match.start()].count("\n") + 1
            symbols.append({"name": match.group(1), "start": start, "end": start, "asset": asset,
                            "kind": "candidate_function", "resolution": "candidate", "definition": True,
                            "frontend_selected": False, "logical": identity("syntax", [asset, start])})
    # Raw branches remain visible even when no selected profile parses them.
    macros = [{"name": m.group(1), "line": text[:m.start()].count("\n") + 1}
              for m in re.finditer(r"(?m)^\s*#\s*define\s+([A-Za-z_]\w*)", text)]
    guards = [{"line": i, "condition": line.strip()} for i, line in enumerate(text.splitlines(), 1)
              if re.match(r"^\s*#\s*(if|ifdef|ifndef|elif|else|endif)\b", line)]
    return symbols, diagnostics, macros, guards


def syntax_calls(raw, symbols):
    """Tree-sitter call sites are navigation candidates, including unselected branches."""
    from tree_sitter import Language, Parser
    import tree_sitter_cpp
    if not symbols:
        return []
    by_name = {}
    for symbol in symbols:
        by_name.setdefault(symbol["name"], []).append(symbol)
    result = []
    stack = [Parser(Language(tree_sitter_cpp.language())).parse(raw).root_node]
    while stack:
        node = stack.pop()
        if node.type == "call_expression":
            site = node.child_by_field_name("function")
            if site:
                name = raw[site.start_byte:site.end_byte].decode("utf-8", errors="replace")
                line = node.start_point.row + 1
                owners = [s for s in symbols if s["start"] <= line <= s["end"]]
                if owners:
                    owner = min(owners, key=lambda s: s["end"] - s["start"])
                    choices = by_name.get(name, [])
                    target = choices[0]["logical"] if len(choices) == 1 else identity("syntax-call", [owner["asset"], node.start_byte, name])
                    result.append({"source": owner["logical"], "target": target, "asset": owner["asset"],
                                   "kind": "CALLS", "resolution": "candidate", "name": name, "offset": node.start_byte,
                                   "start": line, "end": node.end_point.row + 1, "parser": "tree-sitter"})
        stack.extend(node.named_children)
    return result


def parse_one(job, timeout):
    """Only subprocess work runs in parallel; the controller owns all SQLite writes."""
    incoming, outgoing, request = job
    started = time.monotonic()
    try:
        atomic_write(incoming, canonical(request))
        proc = subprocess.run([sys.executable, "-X", "utf8", "-m", "unified_knowledge.clang_worker",
                               str(incoming), str(outgoing)], cwd=Path(__file__).resolve().parents[1],
                              capture_output=True, timeout=timeout)
        require(proc.returncode == 0 and outgoing.is_file(), "Clang worker exited without a result")
        payload = json.loads(outgoing.read_text(encoding="utf-8"))
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        payload = {"symbols": [], "relations": [], "includes": [], "status": "failed",
                   "diagnostics": [], "error": str(error)}
    return payload, round(time.monotonic() - started, 4)


def _persist_payload(store, run, snapshot, profile, payload, context):
    ids = {}
    for item in payload["symbols"]:
        item = dict(item)
        item["id"] = identity("symbol-instance", [snapshot, profile, item["logical"]])
        ids[item["logical"]] = item["id"]
        item.update(snapshot=snapshot, profile=profile, contexts=[context])
        asset = store.asset(snapshot, item["asset"])
        count = len(store.source_lines(asset["sha"]))
        item["end"] = min(item["end"], count)
        item["evidence"] = store.anchor(snapshot, item["asset"], item["start"], item["end"])["id"]
        previous = store.db.execute("SELECT data FROM symbols WHERE run=? AND id=?", (run, item["id"])).fetchone()
        if previous:
            old = json.loads(previous[0])
            item["contexts"] = sorted(set(old.get("contexts", []) + [context]))
            if old.get("definition") and not item.get("definition"):
                old["contexts"] = item["contexts"]
                item = old
        store.db.execute("INSERT OR REPLACE INTO symbols VALUES(?,?,?,?,?,?,?)",
                         (run, item["id"], item["logical"], item["name"], item["asset"], item["kind"], canonical(item)))
    for edge in payload["relations"]:
        edge = dict(edge)
        if not edge.get("asset"):
            continue
        try:
            asset = store.asset(snapshot, edge["asset"])
        except ValueError:
            continue
        size = len(store.source_lines(asset["sha"]))
        if not 1 <= edge["start"] <= size:
            continue
        edge["evidence"] = store.anchor(snapshot, edge["asset"], edge["start"], min(size, max(edge["start"], edge["end"])))["id"]
        edge["source_logical"], edge["target_logical"] = edge["source"], edge["target"]
        edge["source"] = ids.get(edge["source"], identity("symbol-instance", [snapshot, profile, edge["source"]]))
        edge["target"] = ids.get(edge["target"], identity("symbol-instance", [snapshot, profile, edge["target"]]))
        edge.update(context=context, snapshot=snapshot, profile=profile)
        eid = identity("relation", edge)
        edge["id"] = eid
        store.db.execute("INSERT OR IGNORE INTO relations VALUES(?,?,?,?,?,?,?)",
                         (run, eid, edge["source"], edge["target"], edge["kind"], edge["resolution"], canonical(edge)))


def build_index(store, snapshot, profile="unknown", *, timeout=120, resume=False, ctags=None, files=None, jobs=1):
    require(type(jobs) is int and 1 <= jobs <= 8, "jobs must be from 1 to 8")
    selected = None if files is None else sorted(set(files))
    require(selected is None or selected, "Select at least one file")
    require(type(timeout) is int and timeout > 0, "Invalid frontend timeout")
    binding = store.profile(snapshot, profile)
    tools = tool_identity()
    if ctags:
        binary = Path(ctags).resolve()
        require(binary.is_file(), "Ctags executable missing")
        proc = subprocess.run([str(binary), "--options=NONE", "--version"], capture_output=True, timeout=15)
        require(proc.returncode == 0, "Ctags executable failed")
        tools["ctags"] = {"sha256": digest(binary.read_bytes()), "version": proc.stdout.decode("utf-8", errors="replace").splitlines()[0]}
    else:
        tools["ctags"] = "not_configured"
    commands = binding["commands"]
    if selected is not None:
        if profile != "unknown":
            missing = set(selected) - {c["file"] for c in commands}
            require(not missing, "No compile command for: " + ", ".join(sorted(missing)))
        commands = [entry for entry in commands if entry["file"] in selected]
    scope_key = identity("index-scope", [snapshot, binding["digest"], tools, selected, tu_cache.environment()])
    rid = store.get_meta("current:" + scope_key, scope_key)
    # A snapshot fixes repository inputs; separately supplied system headers can change.
    previous = store.db.execute("SELECT data FROM runs WHERE id=?", (rid,)).fetchone()
    if previous:
        prior_run = json.loads(previous[0])
        if prior_run["status"] != "building" and any(
                t["status"] == "parsed" and not tu_cache.valid(store, snapshot, t)
                for t in prior_run.get("tu_results", [])):
            rid = identity("index", [scope_key, uuid.uuid4().hex])
    old = store.db.execute("SELECT data FROM runs WHERE id=?", (rid,)).fetchone()
    old_value = json.loads(old[0]) if old else None
    retry_contexts = {r["context"] for r in (old_value or {}).get("tu_results", []) if r["status"] != "parsed"}
    if old_value and (old_value["status"] == "ready" or
                      (old_value["status"] == "partial" and (not resume or not retry_contexts))):
        return old_value
    require(not old_value or old_value["status"] != "building" or resume, "Interrupted index requires --resume")
    snap = store.record("snapshots", snapshot)
    roots = {r["id"]: store.home / "vfs" / snapshot.replace(":", "-") / r["id"]
             for r in snap["materials"] if r["kind"] == "source"}
    overlay = frozen_view(store, snapshot, roots) if commands else None
    ctags_roots = materialize(store, snapshot) if ctags else {}
    originals = {r["id"]: Path(r["root"]) for r in snap["materials"] if r["kind"] == "source"}
    lease = uuid.uuid4().hex
    with store.transaction():
        prior = store.get_meta("index_lease:" + rid)
        require(not prior or prior["expires"] < time.time(), "Index run has an active lease")
        store.set_meta("index_lease:" + rid, {"token": lease, "expires": time.time() + timeout + 60})
        run = json.loads(old[0]) if old else {
            "id": rid, "snapshot": snapshot, "profile": profile, "profile_digest": binding["digest"],
            "created": now(), "status": "building", "tools": tools, "completed_tus": [],
            "syntax_complete": False, "diagnostics": [], "tu_results": [], "cache_hits": 0,
            "database_execution": "not_run", "mode": "selected" if selected is not None else "full",
            "selected_files": selected, "jobs": jobs, "frontend_invocations": 0}
        store.set_meta("current:" + scope_key, rid)
        if retry_contexts:
            run["status"] = "building"
            run["syntax_complete"] = False
            run["completed_tus"] = [t for t in run["completed_tus"] if t not in retry_contexts]
            run["tu_results"] = [t for t in run["tu_results"] if t["context"] not in retry_contexts]
            for context in retry_contexts:
                store.db.execute("DELETE FROM relations WHERE run=? AND json_extract(data,'$.context')=?", (rid, context))
            for row in store.db.execute("SELECT id,data FROM symbols WHERE run=?", (rid,)).fetchall():
                item = json.loads(row["data"])
                contexts = [c for c in item.get("contexts", []) if c not in retry_contexts]
                if contexts:
                    item["contexts"] = contexts
                    store.db.execute("UPDATE symbols SET data=? WHERE run=? AND id=?", (canonical(item), rid, item["id"]))
                else:
                    store.db.execute("DELETE FROM symbols WHERE run=? AND id=?", (rid, item["id"]))
        store.db.execute("INSERT OR REPLACE INTO runs VALUES(?,?,?,?,?,?)",
                         (rid, snapshot, profile, run["created"], "building", canonical(run)))
    try:
        if not run["syntax_complete"]:
            for row in store.db.execute("SELECT data FROM assets WHERE snapshot=? AND kind='source' AND status='frozen'", (snapshot,)).fetchall():
                item = json.loads(row[0])
                if selected is not None and item["path"] not in selected:
                    continue
                if Path(item["path"]).suffix.lower() not in CPP:
                    continue
                symbols, diagnostics, macros, guards = syntax_candidates(store.blob(item["sha"]), item["key"])
                with store.transaction():
                    _persist_payload(store, rid, snapshot, profile, {"symbols": symbols, "relations": syntax_calls(store.blob(item["sha"]), symbols) if profile == "unknown" and selected else []}, "raw_syntax")
                    run["diagnostics"].extend(diagnostics)
                    store.set_meta("raw_structure:" + snapshot + ":" + item["key"], {"macros": macros, "guards": guards})
            run["syntax_complete"] = True
        if ctags and not run.get("ctags_complete"):
            files = []
            for row in store.db.execute("SELECT data FROM assets WHERE snapshot=? AND kind='source' AND status='frozen'", (snapshot,)):
                item = json.loads(row[0])
                if Path(item["path"]).suffix.lower() in CPP and (selected is None or item["path"] in selected):
                    files.append(str(ctags_roots[item["repo"]] / item["path"]))
            candidates, errors = [], []
            for start in range(0, len(files), 256):
                process = subprocess.run([str(binary), "--options=NONE", "--output-format=json", "--fields=+neK",
                    "--language-force=C++", "--kinds-C++=f", "--extras=-q", "--sort=no", "-f", "-", "-L", "-"],
                    input="\n".join(files[start:start+256])+"\n", capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
                if process.returncode:
                    errors.append({"code": "ctags_batch_failed", "batch": start, "stderr": process.stderr[-2000:]})
                    continue
                for line in process.stdout.splitlines():
                    value = json.loads(line)
                    if value.get("_type") != "tag":
                        continue
                    path = Path(value["path"]).resolve()
                    asset = next((repo+"/"+path.relative_to(root).as_posix() for repo, root in ctags_roots.items() if path.is_relative_to(root)), None)
                    if asset:
                        candidates.append({"name": value["name"], "asset": asset, "start": value["line"],
                                           "end": value.get("end", value["line"])})
            with store.transaction():
                store.set_meta("ctags:" + rid, {"candidates": candidates, "errors": errors})
                run["ctags_complete"] = True
                run["diagnostics"].extend(errors)
        filenames = [r[0] for r in store.db.execute("SELECT key FROM assets WHERE snapshot=? AND kind='source' ORDER BY key", (snapshot,))]
        work = store.home / "index-work" / rid.replace(":", "-")
        completed = set(run["completed_tus"])
        remaining = [(n, e) for n, e in enumerate(commands)
                     if identity("tu", [binding["repository"], e]) not in completed]
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            for start in range(0, len(remaining), jobs):
                batch = []
                for number, entry in remaining[start:start + jobs]:
                    context = identity("tu", [binding["repository"], entry])
                    source_key = binding["repository"] + "/" + entry["file"]
                    key, cached, pending, normalized = None, None, None, []
                    try:
                        source = store.asset(snapshot, source_key)
                        require(source["status"] == "frozen", "Compilation unit not frozen: " + source_key)
                        normalized = compiler_arguments(entry, binding, originals, originals)
                        key = tu_cache.parse_key(binding["repository"], entry, normalized, binding, tools, source["sha"])
                        row = store.db.execute("SELECT data FROM tu_cache WHERE key=?", (key,)).fetchone()
                        if row:
                            value = json.loads(row[0])
                            if tu_cache.valid(store, snapshot, value):
                                cached = value
                                run["cache_hits"] += 1
                        if cached is None:
                            args = compiler_arguments(entry, binding, originals, roots)
                            request = {"file": str(roots[binding["repository"]] / entry["file"]),
                                       "arguments": [*args, "-ivfsoverlay", str(overlay)],
                                       "roots": {k: str(v) for k, v in roots.items()},
                                       "home": str(store.home), "snapshot": snapshot, "unit_file": source_key}
                            job = (work / (str(number) + ".request.json"), work / (str(number) + ".result.json"), request)
                            pending = pool.submit(parse_one, job, timeout)
                            run["frontend_invocations"] += 1
                    except (ValueError, OSError) as error:
                        cached = {"symbols": [], "relations": [], "includes": [], "status": "failed",
                                  "diagnostics": [], "error": str(error)}
                    batch.append((context, source_key, key, normalized, cached, pending))
                for context, source_key, key, normalized, payload, pending in batch:
                    seconds = 0.0
                    if pending:
                        payload, seconds = pending.result()
                        if payload["status"] == "parsed":
                            payload["lookup_guard"] = tu_cache.guard(store, snapshot, source_key, normalized, originals, payload["includes"])
                    with store.transaction():
                        require(store.get_meta("index_lease:" + rid)["token"] == lease, "Index lease lost")
                        _persist_payload(store, rid, snapshot, profile, payload, context)
                        if pending and payload["status"] == "parsed" and payload.get("lookup_guard") is not None:
                            store.db.execute("INSERT OR REPLACE INTO tu_cache VALUES(?,?)", (key, canonical(payload)))
                        run["completed_tus"].append(context)
                        run["tu_results"].append({"context": context, "asset": source_key, "status": payload["status"],
                            "cache_key": key, "seconds": seconds, "error": payload.get("error"),
                            "diagnostics": payload.get("diagnostics", []), "includes": payload.get("includes", []),
                            "lookup_guard": payload.get("lookup_guard")})
                        store.set_meta("index_lease:" + rid, {"token": lease, "expires": time.time() + timeout + 60})
                        store.db.execute("UPDATE runs SET data=? WHERE id=?", (canonical(run), rid))
        counts = Counter(r["status"] for r in run["tu_results"])
        run["status"] = "ready" if commands and counts["parsed"] == len(binding["commands"]) else "partial"
        run["coverage"] = {"assets": len(filenames), "translation_units": len(commands), "available_tus": len(binding["commands"]),
                           "deferred_tus": len(binding["commands"]) - len(commands),
                           "parsed_tus": counts["parsed"], "partial_tus": counts["partial"], "failed_tus": counts["failed"],
                           "unknown_profile": profile == "unknown", "semantic_completeness": "not_certified"}
        with store.transaction():
            # Remove duplicate syntax candidates only where a real frontend definition overlaps them.
            candidates = store.db.execute("SELECT id,asset,data FROM symbols WHERE run=? AND kind='candidate_function'", (rid,)).fetchall()
            for candidate in candidates:
                value = json.loads(candidate["data"])
                actual = store.db.execute("SELECT data FROM symbols WHERE run=? AND asset=? AND kind<>'candidate_function'",
                                          (rid, candidate["asset"])).fetchall()
                if any((a := json.loads(r[0])).get("definition") and a["name"] == value["name"]
                       and a["start"] <= value["end"] and value["start"] <= a["end"] for r in actual):
                    store.db.execute("DELETE FROM symbols WHERE run=? AND id=?", (rid, candidate["id"]))
            run["coverage"]["symbols"] = store.db.execute("SELECT count(*) FROM symbols WHERE run=?", (rid,)).fetchone()[0]
            run["coverage"]["relations"] = store.db.execute("SELECT count(*) FROM relations WHERE run=?", (rid,)).fetchone()[0]
            audit = store.get_meta("ctags:" + rid, {"candidates": [], "errors": []})
            missing = []
            for item in audit["candidates"]:
                actual = [json.loads(r[0]) for r in store.db.execute("SELECT data FROM symbols WHERE run=? AND asset=? AND name=?",
                                                                    (rid, item["asset"], item["name"]))]
                if not any(a.get("definition") and a["start"] <= item["end"] and item["start"] <= a["end"] for a in actual):
                    missing.append(item)
            # A primary-parser omission must not also disappear from the graph
            # and research curriculum. Retain it explicitly as an unconfirmed
            # independent candidate, while keeping the gap visible.
            for item in missing:
                candidate = {**item, "kind": "candidate_function", "resolution": "candidate", "definition": True,
                             "frontend_selected": False, "parser": "ctags_fallback",
                             "logical": identity("ctags-candidate", [item["asset"], item["name"], item["start"]])}
                _persist_payload(store, rid, snapshot, profile, {"symbols": [candidate], "relations": []}, "independent_ctags")
            run["coverage"]["ctags"] = {"configured": bool(ctags), "candidates": len(audit["candidates"]),
                                        "unmatched": missing, "retained_as_candidates": len(missing),
                                        "errors": audit["errors"], "semantic_completeness": "not_certified"}
            run["coverage"]["symbols"] = store.db.execute("SELECT count(*) FROM symbols WHERE run=?", (rid,)).fetchone()[0]
            if missing or audit["errors"]:
                run["status"] = "partial"
            run["coverage"]["call_binding"] = link_calls(store, rid)
            if binding.get("unavailable_commands"):
                run["status"] = "partial"
                run["coverage"]["invalid_commands"] = len(binding["unavailable_commands"])
            run["facts_digest"] = digest({
                "symbols": [[r[0], digest(json.loads(r[1]))] for r in store.db.execute("SELECT id,data FROM symbols WHERE run=? ORDER BY id", (rid,))],
                "relations": [[r[0], digest(json.loads(r[1]))] for r in store.db.execute("SELECT id,data FROM relations WHERE run=? ORDER BY id", (rid,))],
                "profile": binding["digest"], "tu_results": run["tu_results"]})
            store.db.execute("UPDATE runs SET status=?,data=? WHERE id=?", (run["status"], canonical(run), rid))
            store.set_meta("index_head:" + snapshot + ":" + profile, rid)
            store.set_meta("index_lease:" + rid, None)
            store.event("index", {"id": rid, "status": run["status"], "coverage": run["coverage"]})
        return run
    except BaseException:
        with store.transaction():
            prior = store.get_meta("index_lease:" + rid)
            if prior and prior["token"] == lease:
                store.set_meta("index_lease:" + rid, None)
        raise


def query_graph(store, run, targets, *, direction="both", kinds=None, depth=1, limit=100, walk=None):
    require(walk in {None, "bfs", "dfs"}, "Invalid graph walk")
    targets = list(targets)
    require(direction in {"both", "forward", "reverse"}, "Invalid graph direction")
    require(type(depth) is int and 0 <= depth <= 8 and type(limit) is int and 1 <= limit <= 5000, "Invalid graph bounds")
    record = store.record("runs", run)
    require(record["status"] in {"ready", "partial"}, "Index run is not queryable")
    legacy = LegacyCalls(store,run) if record.get("graph_storage")=="reference" and "call_binding" not in record["coverage"] else None
    frontier, seen, nodes, edges = set(targets), set(), {}, {}
    truncated = False
    for level in range(depth + 1):
        following = set()
        for key in sorted(frontier):
            if key in seen:
                continue
            if len(seen) >= limit:
                truncated = True
                break
            seen.add(key)
            row = store.db.execute("SELECT data FROM symbols WHERE run=? AND id=?", (run, key)).fetchone()
            if row:
                nodes[key] = json.loads(row[0])
            if level == depth:
                continue
            columns = ("source", "target") if direction == "both" else (("source",) if direction == "forward" else ("target",))
            for column in columns:
                keys = [key]
                if legacy and column=="target" and nodes.get(key,{}).get("definition") and (not kinds or "CALLS" in kinds):
                    decls = legacy.matches(nodes[key],False,limit+1)
                    truncated |= len(decls)>limit
                    keys.extend(d["id"] for d in decls[:limit])
                for endpoint in keys:
                    selected = ["CALLS"] if endpoint!=key else kinds
                    for edge_row in store.db.execute("SELECT data FROM relations WHERE run=? AND " + column + "=? " +
                            (" AND kind IN (" + ",".join("?" for _ in selected) + ")" if selected else "") +
                            " ORDER BY id LIMIT ?", (run, endpoint, *(selected or []), limit + 1)):
                        edge = json.loads(edge_row[0])
                        if legacy:
                            edge = legacy.rewrite(edge)
                        if endpoint!=key and edge["target"]!=key:
                            continue
                        if edge["id"] in edges:
                            continue
                        if len(edges) >= limit:
                            truncated = True
                            break
                        edges[edge["id"]] = edge
                        following.add(edge["target"] if column == "source" else edge["source"])
                    if len(edges) >= limit and len(keys)>1:
                        truncated = True
                        break
        frontier = following - seen
    return {"run": run, "snapshot": record["snapshot"], "profile": record["profile"],
            "nodes": list(nodes.values()), "relations": list(edges.values()), "truncated": truncated,
            "index_status": record["status"],
            "walk": traversal(edges.values(), targets, direction, walk, depth) if walk else None}
