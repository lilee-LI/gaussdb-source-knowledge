"""Discover research leads in frozen inputs. Only an explicit selection creates a research task."""

from bisect import bisect_right
from collections import defaultdict
from pathlib import PurePosixPath
import json
import re
import unicodedata

from .store import identity, require
from . import product_adapter

PRIORITY = {"design": 0, "manual": 1, "registration": 2, "grammar": 3, "test": 4}
GENERIC = {
    "overview",
    "introduction",
    "introduction and overview",
    "设计",
    "概述",
    "简介",
    "背景",
    "目的",
    "测试",
    "功能描述",
    "design",
    "manual",
}


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def discover(store, snapshot, groups, docs, aliases, adapter=None):
    adapter = adapter or product_adapter.load()
    detectors = product_adapter.expressions(adapter, "candidate")
    leads = {}
    registrations = defaultdict(set)
    module_terms = {
        m: {normalize(m.split("/")[-1]), *aliases.get(m.split("/")[-1].lower(), ())}
        for m in groups
    }
    assets = {
        a["key"]: a
        for a in snapshot["assets"]
        if a["kind"] == "source" and a["status"] == "frozen"
    }

    def add(key, title, kind, asset, line, end, module=None, doc=None):
        cid = identity("candidate", key)
        row = leads.setdefault(
            cid,
            {
                "id": cid,
                "title": title,
                "evidence": [],
                "modules": set(),
                "owner_module": None,
                "owner_basis": "needs_confirmation",
            },
        )
        ref = {"kind": kind, "asset": asset, "start": line, "end": end}
        if doc:
            ref["document"] = doc
        if ref not in row["evidence"]:
            row["evidence"].append(ref)
        if module:
            row["modules"].add(module)
            if row["owner_module"] is None:
                row["owner_module"] = module
                row["owner_basis"] = kind + "_hint"
        return cid

    for module in sorted(groups):
        for asset in sorted(groups[module]):
            if asset not in assets:
                continue
            path = PurePosixPath(asset)
            ext = path.suffix.lower()
            if ext == ".sql" and any(
                p.casefold() in adapter.get("test_directories", [])
                for p in path.parts
            ):
                add(["test", asset], path.stem, "test", asset, 1, 1, module)
                continue
            selected = [(rule, exp) for rule, exp in detectors if ext in rule["extensions"]]
            if not selected:
                continue
            raw = store.blob(assets[asset]["sha"]).decode("utf-8", errors="replace")
            matches = [(m, rule["kind"]) for rule, exp in selected for m in exp.finditer(raw)]
            if not matches:
                continue
            breaks = [m.start() for m in re.finditer("\n", raw)]
            for match, kind in matches:
                name = match.group("name")
                line = bisect_right(breaks, match.start("name")) + 1
                cid = add(
                    [kind, path.parts[0], normalize(name)],
                    name,
                    kind,
                    asset,
                    line,
                    line,
                    module,
                )
                registrations[normalize(name)].add(cid)

    for d in sorted(
        docs, key=lambda x: (PRIORITY.get(x["kind"], 9), x["asset"], x["start"])
    ):
        title = d["title"].strip()
        if not title:
            continue
        key = normalize(title)
        where = normalize(d["asset"] + " " + title)
        matches = sorted(
            m
            for m, terms in module_terms.items()
            if any(t and t in where for t in terms)
        )
        named = {
            cid
            for word in re.findall(r"[a-z_][a-z0-9_.]*", key)
            for cid in registrations.get(word, ())
        }
        if not named and registrations:
            lines = store.source_lines(d["text_sha"])
            for line in lines[d["start"] - 1 : d["end"]]:
                for word in re.findall(r"[a-z_][a-z0-9_]*", line.lower()):
                    if "_" in word:
                        named.update(registrations.get(word, ()))
                if len(named) > 1:
                    break
        # A section about several parameters stays a distinct lead. Short generic headings are file-local.
        if len(named) == 1:
            row = leads[named.pop()]
            ref = {
                "kind": d["kind"],
                "asset": d["asset"],
                "start": d["start"],
                "end": d["end"],
                "document": d["id"],
            }
            row["evidence"].append(ref)
            implementation = [
                m for m in matches if "include" not in PurePosixPath(m).parts
            ]
            if len(implementation) == 1:
                row["owner_module"] = implementation[0]
                row["owner_basis"] = "document_hint"
        else:
            context = (
                [d["asset"], d["start"]] if key in GENERIC or not matches else matches
            )
            cid = add(
                ["section", context, key],
                title,
                d["kind"],
                d["asset"],
                d["start"],
                d["end"],
                matches[0] if len(matches) == 1 else None,
                d["id"],
            )
            row = leads[cid]
        row["modules"].update(matches)
    for row in leads.values():
        row["modules"] = sorted(row["modules"])
        row["evidence"].sort(
            key=lambda e: (PRIORITY.get(e["kind"], 9), e["asset"], e["start"])
        )
        row["question"] = (
            f"{row['title']} 的入口、适用条件、跨模块消费者及测试边界是什么？"
        )
        row["design_gap"] = not any(e["kind"] == "design" for e in row["evidence"])
    return sorted(
        leads.values(),
        key=lambda r: (
            PRIORITY.get(r["evidence"][0]["kind"], 9),
            normalize(r["title"]),
            r["id"],
        ),
    )


def all_candidates(store, plan):
    rows = [*plan.get("candidates", []), *store.get_meta("planning-candidates:" + plan["id"], [])]
    return list({r["id"]:r for r in rows}.values())


def entries(store, plan):
    tasks = defaultdict(list)
    for row in store.db.execute(
        "SELECT id,status,owner,json_extract(data,'$.bundle.candidate_id') cid,"
        "json_extract(data,'$.bundle.module') module FROM tasks "
        "WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? "
        "AND json_extract(data,'$.bundle.candidate_id') IS NOT NULL",
        (plan["snapshot"], plan["id"]),
    ):
        tasks[row["cid"]].append(dict(row))
    published = {
        tid
        for row in store.db.execute(
            "SELECT data FROM proposals WHERE status='accepted'"
        )
        for tid in json.loads(row[0]).get("research_tasks", [])
    }
    assignments = {
        m: store.get_meta("assignment:" + plan["id"] + ":" + m, {}).get("worker")
        for m in plan["modules"]
    }
    rank = {
        "published": 6,
        "accepted": 5,
        "submitted": 4,
        "leased": 3,
        "needs_research": 2,
        "queued": 1,
        "deferred": 0,
    }
    for base in all_candidates(store, plan):
        rows = tasks[base["id"]]
        chosen = max(
            rows,
            key=lambda t: rank.get(
                "published" if t["id"] in published else t["status"], 0
            ),
            default={},
        )
        module = chosen.get("module") or base["owner_module"]
        state = (
            "published" if chosen.get("id") in published else chosen.get("status")
        ) or ("available" if module else "needs_owner")
        yield {
            **base,
            "owner_module": module,
            "worker": chosen.get("owner") or assignments.get(module),
            "state": state,
            "task": chosen.get("id"),
        }


def listing(store, plan, *, module=None, state=None, limit=30, offset=0):
    require(1 <= limit <= 200 and offset >= 0, "页大小应为 1..200，起点不能为负")
    if module:
        require(module in plan["modules"], "未知模块：" + module)
    rows = [
        r
        for r in entries(store, plan)
        if (not module or module in r["modules"] or module == r["owner_module"])
        and (not state or r["state"] == state)
    ]
    return {
        "total": len(rows),
        "offset": offset,
        "next_offset": offset + limit if len(rows) > offset + limit else None,
        "items": rows[offset : offset + limit],
        "catalog_available": "candidates" in plan,
        "next": "learn --candidate <id>；待归属条目加 --module <模块>。旧计划用 start --refresh 更新。",
    }


def candidate(plan, cid, store=None):
    rows = all_candidates(store, plan) if store is not None else plan.get("candidates", [])
    row = next((r for r in rows if r["id"] == cid), None)
    require(row is not None, "当前计划中没有这一候选特性，运行 features 查看。")
    return row
