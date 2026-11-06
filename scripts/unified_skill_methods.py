"""Prepare frozen specialist methods and check topic extensions; never accept knowledge."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "unified-skill/v1"
EXTENSION = "unified-topic-extensions/v1"
DEPTHS = ("reference", "mechanism", "survey")
EVIDENCE = re.compile(r"^evidence:[0-9a-f]{32}$")


def require(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def registry():
    return read(ROOT / "adapters/unified-skill-profiles.json")


def asset(path):
    result = (ROOT / path).resolve()
    require(result.is_relative_to(ROOT) and result.is_file(), "Method missing or outside project: " + path)
    return result


def decisions(request, profiles):
    require(isinstance(request, dict) and request.get("protocol") == PROTOCOL, "Current Skill protocol required")
    require(isinstance(request.get("scope"), str) and request["scope"].strip(), "Concrete research scope required")
    supplied = request.get("topic_decisions", {})
    core = request.get("core_checks", {})
    require(isinstance(supplied, dict) and not set(supplied) - set(profiles["topics"]), "Unknown topic")
    require(isinstance(core, dict) and not set(core) - set(profiles["core_checks"]), "Unknown kernel check")
    result = {}
    for group, names, values in (("topics", profiles["topics"], supplied), ("core_checks", profiles["core_checks"], core)):
        result[group] = {}
        for name in names:
            value = values.get(name, {"need": "unknown", "question": "核对本范围是否涉及 " + name,
                                      "reason": "尚未判断；保持未知，不能推定不涉及"})
            require(isinstance(value, dict) and value.get("need") in {"required", "not_involved", "unknown"}, "Invalid need: " + name)
            require(isinstance(value.get("reason"), str) and value["reason"].strip(), "Decision reason required: " + name)
            if value["need"] != "not_involved":
                require(isinstance(value.get("question"), str) and value["question"].strip(), "Research question required: " + name)
            if group == "topics" and value["need"] == "required":
                require(value.get("depth") in DEPTHS, "Explicit topic depth required: " + name)
            result[group][name] = copy.deepcopy(value)
    return result


def prepare(request, config=None):
    profiles = registry()
    chosen = decisions(request, profiles)
    paths = set(profiles["common_methods"])
    for name, decision in chosen["topics"].items():
        if decision["need"] == "required":
            paths.update(profiles["topics"][name]["methods"][decision["depth"]])
    planned = []
    for path in sorted(paths):
        full = asset(path)
        method_id = "unified-method-" + hashlib.sha256(path.encode("utf-8")).hexdigest()[:16]
        planned.append({"id": method_id, "path": str(full), "revision": sha(full)})
    merged = copy.deepcopy(config or {})
    existing = merged.get("methods", [])
    require(isinstance(existing, list) and all(isinstance(m, dict) and m.get("id") and m.get("path") for m in existing), "Invalid existing methods")
    require(len({m["id"] for m in existing}) == len(existing), "Duplicate existing method IDs")
    ids = {m["id"]: str(Path(m["path"]).resolve()) for m in existing}
    existing_paths = set(ids.values())
    for item in planned:
        require(item["id"] not in ids or ids[item["id"]] == item["path"], "Method ID collision")
        if item["path"] not in existing_paths:
            existing.append(item)
            existing_paths.add(item["path"])
    merged["methods"] = existing
    return {"protocol": PROTOCOL, "scope": request["scope"], **chosen, "method_manifest": planned,
            "validator_sha256": sha(Path(__file__)),
            "config": merged, "status": "method_preparation_only", "semantic_approval": "not_granted",
            "actual_material_freeze": "performed_by_unified_ingest"}


def _refs(value, allowed_evidence, allowed_knowledge, allowed_links, location):
    if isinstance(value, dict):
        for key, item in value.items():
            require(key not in {"evidence_id", "evidence_ids", "source_ref", "source_ref_ids", "evidence_ref"},
                    "Normalize legacy evidence fields to evidence_refs/source_refs: " + location)
            if key in {"source_refs", "evidence_refs"}:
                require(isinstance(item, list) and all(isinstance(r, str) and EVIDENCE.fullmatch(r) for r in item), "Evidence ID list required: " + location)
                require(set(item) <= allowed_evidence, "Hidden evidence dependency: " + location)
            elif key == "knowledge_refs":
                require(isinstance(item, list), "Knowledge reference list required: " + location)
                for link in item:
                    if isinstance(link, dict):
                        require((link.get("target"), link.get("relation")) in allowed_links, "Hidden typed knowledge dependency: " + location)
                    else:
                        require(isinstance(link, str) and link in allowed_knowledge, "Hidden knowledge dependency: " + location)
            _refs(item, allowed_evidence, allowed_knowledge, allowed_links, location + "." + key)
    elif isinstance(value, list):
        for item in value:
            _refs(item, allowed_evidence, allowed_knowledge, allowed_links, location)
    elif isinstance(value, str):
        for ref in re.findall(r"evidence:[A-Za-z0-9_-]+", value):
            require(EVIDENCE.fullmatch(ref) and ref in allowed_evidence, "Hidden or incomplete evidence reference in text: " + location)


def check(value, request=None, method_plan=None):
    profiles = registry()
    if method_plan is not None:
        require(method_plan.get("protocol") == PROTOCOL and method_plan.get("validator_sha256") == sha(Path(__file__)), "Method validator changed; replan before current-contract review")
        require(all(Path(item["path"]).is_file() and sha(item["path"]) == item["revision"] for item in method_plan["method_manifest"]), "Methods changed since preparation; current review needs a new plan")
        if request is not None:
            require(method_plan["scope"] == request.get("scope") and method_plan["topics"] == decisions(request, profiles)["topics"], "Method plan does not match topic request")
    units = value.get("units") if isinstance(value, dict) else None
    require(isinstance(units, list) and units, "Proposal units required")
    kinds = set(read(ROOT/"contracts/unified-knowledge-proposal-v1.schema.json")["$defs"]["unit"]["properties"]["kind"]["enum"])
    ids, seen = set(), {}
    checked = []
    for unit in units:
        require(isinstance(unit, dict) and isinstance(unit.get("id"), str) and unit["id"].strip(), "Unit ID required")
        require(unit["id"] not in ids, "Duplicate unit ID")
        ids.add(unit["id"])
        require(unit.get("kind") in kinds and unit.get("title") and isinstance(unit.get("body"), str) and unit["body"].strip(), "Invalid unified unit kind/title/body")
        require(not any(k.startswith("_") for k in unit), "Reserved knowledge metadata")
        require(unit.get("runtime_verified", False) is False, "Source-only runtime verification cannot be asserted")
        for field in ("runtime_validation", "database_execution", "execution_status"):
            require(unit.get(field, "not_run") == "not_run", "Source-only execution status required")
        evidence = unit.get("source_refs", [])
        links = unit.get("knowledge_refs", [])
        require(isinstance(evidence, list) and all(isinstance(r, str) and EVIDENCE.fullmatch(r) for r in evidence), "Evidence ID list required")
        require(isinstance(links, list) and all(isinstance(r, dict) and isinstance(r.get("target"), str) and r.get("relation") for r in links), "Typed knowledge_refs required")
        link_pairs = {(r["target"], r["relation"]) for r in links}
        targets = {r["target"] for r in links}
        extensions = unit.get("topic_extensions", {})
        require(isinstance(extensions, dict) and not set(extensions) - set(profiles["topics"]), "Unknown topic extension")
        for name, extension in extensions.items():
            require(isinstance(extension, dict) and extension.get("contract") == EXTENSION, "Topic extension contract required")
            require(not set(extension) - {"contract", "depth", "scope", "coverage", "details"}, "Unknown topic extension field")
            depth = extension.get("depth")
            require(depth in DEPTHS and isinstance(extension.get("scope"), str) and extension["scope"].strip(), "Topic depth/scope required")
            coverage, details = extension.get("coverage"), extension.get("details")
            require(isinstance(coverage, list) and isinstance(details, dict), "Structured topic coverage/details required")
            require(all(isinstance(item, (dict, list)) for item in details.values()), "Professional details must stay structured")
            rows = {}
            for row in coverage:
                require(isinstance(row, dict) and row.get("check") in profiles["topics"][name]["sections"] + ["scope_inventory"], "Unknown topic check")
                key = row["check"]
                require(key not in rows, "Duplicate topic check")
                rows[key] = row
                require(row.get("status") in {"answered", "open", "not_applicable"} and isinstance(row.get("explanation"), str) and row["explanation"].strip(), "Topic status/explanation required")
                if row["status"] == "answered":
                    require(row.get("evidence_refs") or row.get("knowledge_refs"), "Answered topic needs explicit evidence or knowledge")
                    require(isinstance(details.get(key), (dict, list)) and details[key], "Professional structured details required: " + key)
                if row["status"] == "open":
                    require(isinstance(row.get("next_step"), str) and row["next_step"].strip(), "Open topic needs a concrete next_step")
            required = profiles["topics"][name]["required_sections"][depth]
            require(set(required) <= set(rows), "Missing required topic checks: " + name)
            _refs(extension, set(evidence), targets, link_pairs, unit["id"] + "." + name)
            seen[name] = max(seen.get(name, 0), DEPTHS.index(depth) + 1)
            checked.append({"unit": unit["id"], "topic": name, "depth": depth,
                            "open_checks": [r["check"] for r in coverage if r["status"] == "open"]})
    if request is not None:
        selection = decisions(request, profiles)["topics"]
        for name, decision in selection.items():
            if decision["need"] == "required":
                require(seen.get(name, 0) >= DEPTHS.index(decision["depth"]) + 1, "Required topic/depth not delivered: " + name)
    return {"status": "topic_contract_valid", "checked": checked, "units": len(units),
            "semantic_approval": "not_granted", "evidence_existence_and_reads": "checked_by_unified_engine",
            "open_questions_remain": any(item["open_checks"] for item in checked)}


def audit():
    profiles = registry()
    require(profiles["protocol"] == PROTOCOL and len(profiles["topics"]) == 8, "Eight current profiles required")
    paths = {"SKILL.md", "skills/source-repository-learning/SKILL.md", *profiles["common_methods"]}
    skill_paths = {"SKILL.md", "skills/source-repository-learning/SKILL.md"}
    for item in profiles["topics"].values():
        skill_paths.add(item["skill"])
        require(set(item["methods"]) == set(DEPTHS) and set(item["required_sections"]) == set(DEPTHS), "Depth definitions missing")
        for values in item["methods"].values():
            paths.update(values)
    hashes = {}
    for name in sorted(paths):
        path = asset(name)
        hashes[name] = sha(path)
        if name in skill_paths:
            text = path.read_text(encoding="utf-8-sig")
            require(PROTOCOL in text, "Skill still lacks current protocol: " + name)
            require('本入口遵循用户“客户包全部可读且无源码”' not in text, "Old customer rule still active")
            require('通过根工程 `scripts/dbknowledge.py --project PROJECT study ...`' not in text, "Old default study route still active")
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8-sig")):
            if re.match(r"^[a-zA-Z]+:", target) or target.startswith("#"):
                continue
            require((path.parent/target.split("#",1)[0]).exists(), "Broken method link: " + name + " -> " + target)
    archive = ROOT/"references/legacy-skills-20261104"
    historical = read(archive/"MANIFEST.json") if (archive/"MANIFEST.json").is_file() else {}
    require(all(sha(archive/name) == item["sha256"] for name,item in historical.items()), "Historical Skill bytes changed")
    cases = read(ROOT/"assets/unified-skill-evaluation-cases.json")
    require(len({case["id"] for case in cases["cases"]}) == len(cases["cases"]), "Duplicate evaluation IDs")
    require(all(case["execution_status"] == "not_run" for case in cases["cases"]), "Unexecuted evaluation mislabeled")
    return {"status": "skill_contract_audit_passed", "skill_files": len(skill_paths), "method_files": len(paths),
            "historical_skills_preserved": len(historical), "evaluation_recipes_not_run": len(cases["cases"]),
            "sha256": hashes, "semantic_approval": "not_granted"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument("--request", required=True, type=Path)
    plan_parser.add_argument("--config", type=Path)
    plan_parser.add_argument("--config-output", type=Path)
    check_parser = sub.add_parser("check")
    check_parser.add_argument("--input", required=True, type=Path)
    check_parser.add_argument("--request", type=Path)
    check_parser.add_argument("--method-plan", type=Path)
    sub.add_parser("audit")
    for command in (plan_parser, check_parser):
        command.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        for output in (getattr(args,"output",None),getattr(args,"config_output",None)):
            require(output is None or not output.exists(), "Use a new output file")
        if getattr(args,"output",None) and getattr(args,"config_output",None):
            require(args.output.resolve() != args.config_output.resolve(), "Plan and config need different output paths")
        if args.action == "plan":
            result = prepare(read(args.request), read(args.config) if args.config else None)
            if args.config_output:
                with args.config_output.open("x", encoding="utf-8") as handle:
                    handle.write(json.dumps(result["config"], ensure_ascii=False, indent=2)+"\n")
        elif args.action == "check":
            result = check(read(args.input), read(args.request) if args.request else None, read(args.method_plan) if args.method_plan else None)
        else:
            result = audit()
        text = json.dumps(result, ensure_ascii=False, indent=2)+"\n"
        if getattr(args,"output",None):
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(text)
        else:
            print(text,end="")
        return 0
    except (OSError,ValueError,KeyError,TypeError) as error:
        print(json.dumps({"error":type(error).__name__,"message":str(error)},ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
