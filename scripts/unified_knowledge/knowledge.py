"""Reviewed Wiki and typed contracts, version dependencies and Git-backed commits."""
from __future__ import annotations

from collections import defaultdict
import json
import os
from pathlib import Path
import subprocess

from .store import atomic_write, canonical, digest, identity, now, require


KINDS = {"module", "responsibility", "feature", "mechanism", "claim", "contract", "flow",
         "test_obligation", "requirement", "observation", "decision"}
EDGES = {"DEPENDS_ON", "PRODUCES", "CONSUMES", "IMPLEMENTS", "REQUIRES_TEST", "REFINES",
         "CONTRADICTS", "VERIFIED_BY", "CITES"}


def content_hash(unit):
    return digest({k: v for k, v in unit.items() if k not in {"_binding", "review", "content_hash", "version"}})


def symbol_dependency(store, run, symbol):
    rows = store.lookup_symbols(run,symbol,names=False,limit=1)
    require(rows, "Unknown source symbol: " + symbol)
    value = json.loads(rows[0]["data"])
    evidence = store.record("anchors", value["evidence"])
    outgoing = [json.loads(r[0]) for r in store.db.execute("SELECT data FROM relations WHERE run=? AND source=? ORDER BY id", (run, value["id"]))]
    proof = {"logical": value["logical"], "name": value["name"], "kind": value["kind"], "type": value.get("type"),
             "resolution": value["resolution"], "quote": evidence["quote_sha256"],
             "outgoing": sorted((e["kind"], e.get("target_logical", e["target"]), e["resolution"]) for e in outgoing)}
    if value.get("type_observations"):
        proof["type_observations"] = value["type_observations"]
    return {"type": "symbol", "ref": value["logical"], "fingerprint": digest(proof)}


def dependency_value(store, snapshot, run, dependency):
    kind, ref = dependency["type"], dependency["ref"]
    if kind == "asset":
        item = store.asset(snapshot, ref)
        if item["status"] == "frozen":
            store.blob(item["sha"])
            if item.get("text_sha"):
                store.blob(item["text_sha"])
        return digest({k: item.get(k) for k in ("status", "sha", "text_sha", "document_status", "declared_revision")})
    if kind == "symbol":
        return symbol_dependency(store, run, ref)["fingerprint"]
    if kind == "scope":
        rows = [(r[0], r[1], r[2]) for r in store.db.execute("SELECT key,sha,status FROM assets WHERE snapshot=? ORDER BY key", (snapshot,))
                if r[0].startswith(ref)]
        return digest(rows)
    if kind == "profile":
        return store.profile(snapshot, ref)["digest"]
    raise ValueError("Unsupported knowledge dependency: " + kind)


class UnitMap(dict):
    """Lazy revision-bound object lookup; never loads a whole Wiki per question."""
    def __init__(self, store, revision, initial=None):
        super().__init__(initial or {})
        self.store, self.revision = store, revision
        self.dependency_cache = {}

    def get(self, key, default=None):
        if key not in self:
            self.update(self.store.units(self.revision, ids=[key]))
        return super().get(key, default)

    def __missing__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value


def freshness(store, unit, snapshot, run, units, visited=None):
    # An explicit stack also handles deep cross-module knowledge dependencies.
    visited = set() if visited is None else set(visited)
    reasons = []
    profile = store.record("runs", run)["profile"]
    method_digest = store.record("snapshots", snapshot).get("methods_digest")
    cache = getattr(units, "dependency_cache", {})
    stack = [unit]
    while stack:
        current = stack.pop()
        if current["id"] in visited:
            continue
        visited.add(current["id"])
        binding = current.get("_binding", {})
        if not binding:
            reasons.append({"code": "knowledge_binding_missing", "id": current["id"]})
        if binding and binding.get("profile") != profile:
            reasons.append({"code": "profile_mismatch", "id": current["id"], "expected": binding.get("profile")})
        if binding and binding.get("methods_digest") != method_digest:
            reasons.append({"code": "method_version_changed", "id": current["id"]})
        for dep in binding.get("dependencies", []):
            key = (snapshot, run, dep["type"], dep["ref"])
            try:
                if key not in cache:
                    cache[key] = dependency_value(store, snapshot, run, dep)
                if cache[key] != dep["fingerprint"]:
                    reasons.append({"code": "dependency_changed", "id": current["id"], **dep})
            except (ValueError, OSError):
                reasons.append({"code": "dependency_missing", "id": current["id"], **dep})
        for link in binding.get("knowledge_dependencies", []):
            target = units.get(link["ref"])
            if not target or content_hash(target) != link["fingerprint"]:
                reasons.append({"code": "knowledge_dependency_changed", "id": current["id"], "ref": link["ref"]})
            else:
                stack.append(target)
    return reasons


def _validate_unit(store, unit, proposal, available):
    require(isinstance(unit, dict) and isinstance(unit.get("id"), str) and unit["id"].strip(), "Knowledge id required")
    require(unit.get("kind") in KINDS and unit.get("title") and isinstance(unit.get("body"), str) and unit["body"].strip(),
            "Knowledge kind, title and substantive Markdown body required")
    require("runtime_verified" not in unit or unit["runtime_verified"] is False,
            "Source-only submission cannot assert runtime verification")
    for field in ("runtime_validation", "database_execution"):
        require(unit.get(field, "not_run") == "not_run", "Source-only knowledge cannot assert executed runtime status")
    for field in ("source_refs", "symbol_refs", "knowledge_refs", "conditions", "counterexamples"):
        require(isinstance(unit.get(field, []), list), "Expected a list: " + field)
    for ref in unit.get("source_refs", []):
        anchor = store.record("anchors", ref)
        current = store.asset(proposal["snapshot"], anchor["asset"])
        require(current["sha"] == anchor["asset_sha"], "Knowledge cites changed source material")
        store.read_evidence(ref)
    for ref in unit.get("symbol_refs", []):
        symbol_dependency(store, proposal["run"], ref)
    for link in unit.get("knowledge_refs", []):
        require(isinstance(link, dict) and link.get("relation") in EDGES and link.get("target") in available,
                "Unresolved or invalid semantic relation")
    if unit["kind"] in {"claim", "contract", "requirement"}:
        require(unit.get("source_refs"), "Claim, contract or requirement needs frozen evidence")
        require(unit.get("conditions"), "Explicit applicability conditions required")
        require(unit.get("counterexamples"), "Counterexample or bounded limitation required")
        require(any(store.asset(proposal["snapshot"], store.record("anchors", r)["asset"])["kind"] in {"source", "document"}
                    for r in unit["source_refs"]), "Method text alone cannot support a product behavior claim")
    if unit["kind"] == "claim":
        require(unit.get("statement"), "Claim statement required")
        if unit.get("assertion_kind") in {"absence", "exhaustive", "uniqueness"}:
            require(any(isinstance(d,dict) and d.get("type") == "scope" for d in unit.get("scope_dependencies", [])),
                    "Negative/exhaustive claim needs an explicit search-scope dependency")
    if unit["kind"] == "contract":
        for key in ("producers", "consumers", "requires", "ensures", "invariants"):
            require(isinstance(unit.get(key), list) and unit[key], "Contract missing " + key)
        for ref in unit["producers"] + unit["consumers"]:
            symbol_dependency(store, proposal["run"], ref)
    if unit["kind"] == "test_obligation":
        expected = unit.get("expected_from", {})
        require(isinstance(expected,dict) and isinstance(expected.get("ref"),str) and
                expected.get("kind") in {"requirement","claim","contract","source_prediction"},
                'expected_from must be one object, e.g. {"kind":"contract","ref":"contract:example"}')
        require(expected.get("ref") in available or expected.get("ref") in unit.get("source_refs", []), "Test oracle reference missing")
        if expected["kind"] != "source_prediction":
            require(expected["ref"] in available and available[expected["ref"]]["kind"] == expected["kind"],
                    "Test oracle type does not match its actual knowledge object")
        require(unit.get("execution_status", "not_run") == "not_run", "Only separate runtime receipts may attest execution")
    if unit["kind"] == "flow":
        require(isinstance(unit.get("steps"), list) and unit["steps"], "Flow needs explicitly typed steps")
        for step in unit["steps"]:
            require(isinstance(step,dict) and step.get("kind") in {"call", "data_stage", "state_transition", "async_message"},
                    "Flow step must distinguish calls, data stages and transitions")
            if step["kind"] == "call":
                require(step.get("symbol") and step.get("target"), "Call flow needs real source and target symbols")
                symbol_dependency(store, proposal["run"], step["symbol"])
                symbol_dependency(store, proposal["run"], step["target"])
    if unit["kind"] in {"feature", "responsibility"}:
        require(type(unit.get("level")) is int and 1 <= unit["level"] <= 4, "Tree level must be 1..4")
        parent = unit.get("parent")
        if unit["level"] > 1:
            require(parent in available and available[parent]["kind"] == unit["kind"]
                    and available[parent].get("level") == unit["level"] - 1, "Tree parent/level mismatch")
        else:
            require(not parent, "Level-one tree node cannot have a parent")
    require(unit.get("source_refs") or unit.get("knowledge_refs") or unit["kind"] in {"responsibility", "feature"},
            "Knowledge needs evidence or explicit knowledge dependencies")


def propose(store, value):
    require(isinstance(value, dict) and isinstance(value.get("units"), list) and value["units"], "Knowledge units required")
    require(value.get("author") and "expected_head" in value, "Author and optimistic expected_head required")
    index = store.record("runs", value["run"])
    require(index["snapshot"] == value["snapshot"] and index["profile"] == value["profile"], "Knowledge input binding mismatch")
    require(index["status"] in {"ready", "partial"}, "Knowledge requires a finished index")
    with store.transaction():
        require(value["expected_head"] == store.get_meta("knowledge_head"), "Knowledge head changed; rebase proposal")
        current = store.units(value["expected_head"])
        updates = {}
        for original in value["units"]:
            require(original["id"] not in updates, "Duplicate unit in proposal")
            require(not any(k.startswith("_") for k in original), "Reserved knowledge metadata")
            updates[original["id"]] = dict(original)
        available = {**current, **updates}
        for unit in updates.values():
            _validate_unit(store, unit, value, available)
        for tid in value.get("research_tasks", []):
            row = store.db.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
            require(row is not None and row["status"] == "accepted" and row["snapshot"] == value["snapshot"],
                    "Referenced research task must be accepted in this snapshot")
        require(value.get("research_tasks") or value.get("import_provenance"),
                "Knowledge needs accepted research or explicit import provenance")
        result = {**value, "units": list(updates.values()), "profile_digest": index["profile_digest"],
                  "schema": "knowledge-proposal/v1"}
        pid = identity("proposal", result)
        result["id"] = pid
        store.db.execute("INSERT OR IGNORE INTO proposals VALUES(?,?,'pending',?)", (pid, now(), canonical(result)))
        store.event("knowledge_propose", {"id": pid, "author": value["author"], "units": list(updates)})
    return result


def review_context(store, proposal_id, reviewer, *, max_chars=100000):
    require(reviewer and type(max_chars) is int and 1 <= max_chars <= 1000000, "Reviewer and valid read budget required")
    proposal = store.record("proposals", proposal_id)
    refs = sorted({ref for u in proposal["units"] for ref in u.get("source_refs", [])})
    evidence = []
    remaining = max_chars
    with store.transaction():
        for ref in refs:
            if remaining <= 0:
                break
            value = store.read_evidence(ref, max_chars=remaining)
            remaining -= value["returned_chars"]
            evidence.append(value)
            store.event("knowledge_review_read", {"proposal": proposal_id, "reviewer": reviewer, "evidence": ref,
                                                "proposal_digest": digest(proposal), "truncated": value["truncated"]})
    return {"proposal": proposal, "proposal_digest": digest(proposal), "evidence": evidence,
            "materials": [{"evidence": ref, "current_material": store.asset(proposal["snapshot"], store.record("anchors", ref)["asset"])}
                          for ref in refs],
            "truncated": len(evidence) < len(refs) or any(e["truncated"] for e in evidence),
            "review_template": {"reviewer": reviewer, "mode": "self_reviewed", "verdict": "accept_or_reject",
                                "proposal_digest": digest(proposal), "notes": "Actual evidence, conditions and consumer review required"}}


def _git_commit(store, files, parent, message):
    """A private bare Git mirror; application/project Git configuration is untouched."""
    git_dir = store.home / "wiki.git"
    if not git_dir.exists():
        result = subprocess.run(["git", "init", "--bare", "--quiet", str(git_dir)], capture_output=True, timeout=30)
        require(result.returncode == 0, "Git initialization failed")
    env = dict(os.environ, GIT_AUTHOR_NAME="Knowledge Engineering", GIT_AUTHOR_EMAIL="knowledge@localhost",
               GIT_COMMITTER_NAME="Knowledge Engineering", GIT_COMMITTER_EMAIL="knowledge@localhost")
    def git(args, raw=None):
        p = subprocess.run(["git", "--git-dir", str(git_dir), *args], input=raw, capture_output=True, timeout=30, env=env)
        require(p.returncode == 0, "Git mirror operation failed: " + p.stderr.decode("utf-8", errors="replace")[-500:])
        return p.stdout.decode("ascii").strip()
    tree = {}
    for path, raw in sorted(files.items()):
        parts = path.split("/")
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = git(["hash-object", "-w", "--stdin"], raw)
    def write_tree(node):
        lines = []
        for name, item in sorted(node.items()):
            if isinstance(item, dict):
                lines.append("040000 tree " + write_tree(item) + "\t" + name)
            else:
                lines.append("100644 blob " + item + "\t" + name)
        return git(["mktree"], ("\n".join(lines) + "\n").encode("utf-8"))
    tree_id = write_tree(tree)
    return git(["commit-tree", tree_id, *(["-p", parent] if parent else []), "-m", message])


def knowledge_files(units):
    files, inventory = {}, []
    for uid, unit in sorted(units.items()):
        stem = digest(uid)[:24]
        folder = unit["kind"] + "s"
        path = folder + "/" + stem + ".md"
        metadata = {k: unit[k] for k in ("id", "kind", "title", "conditions", "source_refs", "symbol_refs", "content_hash") if k in unit}
        body = "---\n" + json.dumps(metadata, ensure_ascii=False, indent=2) + "\n---\n\n# " + unit["title"] + "\n\n" + unit["body"].strip() + "\n"
        files[path] = body.encode("utf-8")
        files[folder + "/" + stem + ".yaml"] = (json.dumps(unit, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        inventory.append({"id": uid, "path": path, "kind": unit["kind"], "title": unit["title"]})
    files["index.json"] = (canonical(inventory) + "\n").encode("utf-8")
    files["README.md"] = ("# 统一源码知识库\n\n" + "\n".join("- [" + r["title"] + "](" + r["path"] + ")" for r in inventory) + "\n").encode("utf-8")
    return files


def review(store, proposal_id, decision):
    require(decision.get("reviewer") and decision.get("notes") and decision.get("mode") in {"self_reviewed", "independent_review"},
            "Actual review identity, mode and notes required")
    require(decision.get("verdict") in {"accept", "reject"}, "Review verdict required")
    with store.transaction():
        proposal = store.record("proposals", proposal_id)
        status = store.db.execute("SELECT status FROM proposals WHERE id=?", (proposal_id,)).fetchone()[0]
        require(status == "pending", "Proposal is not pending")
        require(decision.get("proposal_digest") == digest(proposal), "Proposal changed since review")
        require(proposal["expected_head"] == store.get_meta("knowledge_head"), "Knowledge head changed; rebase before accepting")
        if proposal.get("remote_order"):
            order = proposal["remote_order"]
            active = store.get_meta(store.get_meta(order))
            require(active and active["id"] == order and set(proposal['research_tasks'])<=set(active.get('received_tasks',[active.get('received_task')])) and
                    active["ticket"]["snapshot"] == store.get_meta("snapshot_head"), "Remote work order superseded")
        if decision["mode"] == "independent_review":
            require(decision["reviewer"] != proposal["author"], "Independent review requires another actor")
        if decision["verdict"] == "reject":
            store.db.execute("UPDATE proposals SET status='rejected' WHERE id=?", (proposal_id,))
            store.event("knowledge_review", {"proposal": proposal_id, **decision})
            return {"proposal": proposal_id, "status": "rejected"}
        expected = {ref for unit in proposal["units"] for ref in unit.get("source_refs", [])}
        reads = [json.loads(r[0]) for r in store.db.execute("SELECT data FROM events WHERE kind='knowledge_review_read'")]
        actual = {r["evidence"] for r in reads if r["proposal"] == proposal_id and r["reviewer"] == decision["reviewer"]
                  and r["proposal_digest"] == decision["proposal_digest"] and not r["truncated"]}
        require(expected <= actual, "Review must actually read all changed-unit evidence")
        current = store.units(proposal["expected_head"])
        merged = {**current, **{u["id"]: u for u in proposal["units"]}}
        for unit in proposal["units"]:
            _validate_unit(store, unit, proposal, merged)
        updates = {}
        for original in proposal["units"]:
            unit = dict(original)
            dependencies = {}
            for ref in unit.get("source_refs", []):
                anchor = store.record("anchors", ref)
                dep = {"type": "asset", "ref": anchor["asset"]}
                dependencies[("asset", dep["ref"])] = dep
            symbols = [ref for _,_,ref in symbol_links(unit)]
            for ref in symbols:
                dep = symbol_dependency(store, proposal["run"], ref)
                dependencies[("symbol", dep["ref"])] = {"type": "symbol", "ref": dep["ref"]}
            for dep in unit.get("scope_dependencies", []):
                require(dep.get("type") in {"asset", "symbol", "scope", "profile"}, "Invalid declared scope dependency")
                dependencies[(dep["type"], dep["ref"])] = {"type": dep["type"], "ref": dep["ref"]}
            dependencies[("profile", proposal["profile"])] = {"type": "profile", "ref": proposal["profile"]}
            for dep in dependencies.values():
                dep["fingerprint"] = dependency_value(store, proposal["snapshot"], proposal["run"], dep)
            knowledge_deps = [{"ref": link["target"], "fingerprint": content_hash(merged[link["target"]])}
                              for link in unit.get("knowledge_refs", []) if link["relation"] not in {"CONTRADICTS"}]
            unit["content_hash"] = content_hash(unit)
            unit["_binding"] = {"snapshot": proposal["snapshot"], "run": proposal["run"], "profile": proposal["profile"],
                                "dependencies": list(dependencies.values()), "knowledge_dependencies": knowledge_deps,
                                "methods_digest": store.record("snapshots", proposal["snapshot"]).get("methods_digest")}
            unit["review"] = {**decision, "proposal": proposal_id, "at": now(), "runtime_validation": "not_run"}
            updates[unit["id"]] = unit
        units = {**current, **updates}
        revision_id = identity("knowledge", [proposal["expected_head"], proposal_id, decision, {k: digest(v) for k, v in sorted(units.items())}])
        files = knowledge_files(units)
        previous_git = store.get_meta("git_head")
        commit = _git_commit(store, files, previous_git, revision_id)
        revision = {"id": revision_id, "parent": proposal["expected_head"], "snapshot": proposal["snapshot"],
                    "run": proposal["run"], "profile": proposal["profile"], "created": now(), "proposal": proposal_id,
                    "git_commit": commit, "review_mode": decision["mode"], "runtime_validation": "not_run",
                    "unit_hashes": {k: digest(v) for k, v in sorted(units.items())},
                    "files": {k: digest(v) for k, v in sorted(files.items())}}
        directory = store.home / "revisions" / revision_id.replace(":", "-")
        for path, raw in files.items():
            atomic_write(directory / path, raw)
        atomic_write(directory / "revision.json", canonical(revision))
        store.db.execute("INSERT INTO revisions VALUES(?,?,?,?,?,?,?)", (revision_id, proposal["expected_head"],
                         proposal["snapshot"], proposal["run"], proposal["profile"], revision["created"], canonical(revision)))
        for uid, unit in units.items():
            h = digest(unit)
            store.db.execute("INSERT OR IGNORE INTO unit_versions VALUES(?,?)", (h, canonical(unit)))
            store.db.execute("INSERT INTO revision_units VALUES(?,?,?)", (revision_id, uid, h))
            text = unit["title"] + "\n" + unit["body"] + "\n" + canonical(unit.get("conditions", []))
            if store.fts:
                store.db.execute("INSERT INTO search_fts VALUES(?,?,?)", (revision_id, uid, text))
            from .retrieval import embedding
            lexical_hash = content_hash(unit)
            if not store.db.execute("SELECT 1 FROM lexical_cache WHERE hash=?", (lexical_hash,)).fetchone():
                store.db.execute("INSERT INTO lexical_cache VALUES(?,?,?)", (lexical_hash, text, canonical(embedding(text))))
            for dep in unit["_binding"]["dependencies"]:
                store.db.execute("INSERT INTO unit_dependencies VALUES(?,?,?,?,?)",
                                 (revision_id, uid, dep["type"], dep["ref"], dep["fingerprint"]))
            for link in unit.get("knowledge_refs", []):
                store.db.execute("INSERT INTO semantic_edges VALUES(?,?,?,?)",
                                 (revision_id, uid, link["target"], link["relation"]))
            for anchor in unit.get("source_refs", []):
                store.db.execute("INSERT INTO alignments VALUES(?,?,?,?,?)",
                                 (revision_id, uid, None, anchor, canonical({"kind": "CITES", "content_hash": unit["content_hash"]})))
            for _,relation,symbol in symbol_links(unit):
                store.db.execute("INSERT INTO alignments VALUES(?,?,?,?,?)",
                                 (revision_id, uid, symbol, None, canonical({"kind": relation, "content_hash": unit["content_hash"]})))
        store.db.execute("UPDATE proposals SET status='accepted' WHERE id=?", (proposal_id,))
        store.set_meta("knowledge_head", revision_id)
        store.set_meta("git_head", commit)
        store.event("knowledge_review", {"proposal": proposal_id, "revision": revision_id, **decision})
    # The Git ref is a recoverable mirror of the committed SQLite manifest.
    # Interrupted ref updates are detectable and repaired explicitly by doctor.
    result = subprocess.run(["git", "--git-dir", str(store.home / "wiki.git"), "update-ref",
                             "refs/heads/knowledge", commit, previous_git or "0" * 40],
                            capture_output=True, timeout=30)
    if result.returncode:
        raise ValueError("Knowledge committed; Git mirror ref needs reconciliation with doctor --repair-git")
    return revision


def symbol_links(unit):
    """Typed compiler bindings; prose consumer labels are source facts only."""
    for field,relation in (('symbol_refs','IMPLEMENTS'),('producers','PRODUCES'),('consumers','CONSUMES')):
        for ref in unit.get(field,[]):
            if field=='symbol_refs' or unit['kind']=='contract' or isinstance(ref,str) and ref.startswith(('symbol-instance:','symbol:','syntax:')):
                yield field,relation,ref


def knowledge_graph(store, revision=None):
    units = store.units(revision)
    edges = [{"source": uid, "target": link["target"], "kind": link["relation"]}
             for uid, unit in units.items() for link in unit.get("knowledge_refs", [])]
    trees = {"responsibility": [], "feature": []}
    for uid, unit in units.items():
        if unit["kind"] in trees:
            trees[unit["kind"]].append({"id": uid, "parent": unit.get("parent"), "level": unit["level"],
                                       "title": unit["title"], "symbol_refs": unit.get("symbol_refs", [])})
    links = []
    for uid, unit in units.items():
        for _,kind,symbol in symbol_links(unit):
            links.append({"knowledge": uid, "symbol": symbol, "kind": kind,
                          "source_binding": {k: unit["_binding"][k] for k in ("snapshot", "run", "profile")}})
    return {"revision": revision or store.get_meta("knowledge_head"), "source_links": links,
            "nodes": [{"id": k, "kind": u["kind"], "title": u["title"]} for k, u in units.items()],
            "relations": edges, "trees": trees}
