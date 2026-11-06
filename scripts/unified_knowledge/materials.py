"""Whole-tree inventory, frozen material extraction and build-context capture."""
from __future__ import annotations

from html.parser import HTMLParser
import fnmatch
import io
import json
import os
from pathlib import Path
import re
import shlex
import stat
import subprocess
import xml.etree.ElementTree as ET
import zipfile

from .store import canonical, digest, identity, now, require

CPP = {".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx", ".inc"}
OMIT_DIRS = {".git", ".svn", ".codewiki", ".codegraph", ".serena", ".claude", ".codex", "__pycache__", "node_modules", ".venv"}
TEXT_DOCS = {".md", ".markdown", ".txt", ".html", ".htm", ".docx", ".pdf"}


def linked(path):
    value = path.lstat()
    return stat.S_ISLNK(value.st_mode) or bool(getattr(value, "st_file_attributes", 0) & 0x400)


def walk(root):
    """Yield every accepted file or explicit link/directory exclusion."""
    root = Path(root)
    if root.is_file():
        yield root, None
        return
    errors = []
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=errors.append):
        dirs.sort()
        for name in list(dirs):
            entry = Path(directory) / name
            if name in OMIT_DIRS or linked(entry):
                dirs.remove(name)
                yield entry, "linked_directory" if linked(entry) else "tool_metadata_directory"
        for name in sorted(files):
            p = Path(directory) / name
            yield p, "linked_file" if linked(p) else None
    for error in errors:
        yield Path(error.filename), "walk_error:" + type(error).__name__


class TextHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden += 1
        if not self.hidden and tag in {"p", "br", "div", "tr", "li", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, text):
        if not self.hidden:
            self.parts.append(text)


def extract(raw, suffix):
    if suffix in {".md", ".markdown", ".txt"}:
        return raw.decode("utf-8-sig"), "native-text", "requires_semantic_review"
    if suffix in {".html", ".htm"}:
        p = TextHTML()
        p.feed(raw.decode("utf-8-sig"))
        return "".join(p.parts), "html-text", "layout_requires_original_review"
    if suffix == ".docx":
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            info = z.getinfo("word/document.xml")
            require(info.file_size <= 64 * 1024 * 1024, "DOCX XML too large")
            root = ET.fromstring(z.read(info))
        ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        rows = ["".join(t.text or "" for t in p.iter(ns + "t")) for p in root.iter(ns + "p")]
        return "\n".join(rows), "docx-xml", "tables_require_original_review"
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            raise ValueError("PDF extraction needs pypdf; original material remains frozen") from None
        pages = [p.extract_text() or "" for p in PdfReader(io.BytesIO(raw)).pages]
        require(any(p.strip() for p in pages), "No extractable PDF text; offline OCR adapter required")
        return "\n".join("# Page %d\n%s" % (i + 1, t) for i, t in enumerate(pages)), "pypdf", "layout_requires_original_review"
    raise ValueError("Unsupported document format: " + suffix)


def git_identity(root):
    result = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True,
                            encoding="utf-8", errors="replace", timeout=15)
    return result.stdout.strip() if result.returncode == 0 else None


def _compile_entry(entry, root):
    require(isinstance(entry, dict) and isinstance(entry.get("file"), str), "Invalid compile command")
    directory = Path(entry.get("directory", root)).resolve()
    file = Path(entry["file"])
    file = (directory / file).resolve() if not file.is_absolute() else file.resolve()
    require(file.is_relative_to(root), "Compilation unit leaves repository")
    arguments = entry.get("arguments")
    if arguments is None:
        command = entry.get("command")
        require(isinstance(command, str), "Compile entry needs arguments or command")
        # Split only; these strings are never passed to a shell.
        arguments = shlex.split(command, posix=os.name != "nt")
        if os.name == "nt":
            arguments = [a[1:-1] if len(a) >= 2 and a.startswith('"') and a.endswith('"') else a for a in arguments]
    require(isinstance(arguments, list) and all(isinstance(a, str) for a in arguments), "Invalid compiler arguments")
    return {"file": file.relative_to(root).as_posix(), "directory": str(directory), "arguments": arguments}


def ingest(store, config, *, imported=None):
    require(isinstance(config, dict), "Snapshot configuration must be an object")
    repos = config.get("repositories", [])
    require(isinstance(repos, list) and repos, "At least one source repository is required")
    supplied = []
    ids = set()
    methods = [{"id": "__engine_research_contract", "path": str(Path(__file__).with_name("research_contract.md")),
                "revision": "unified-research/v1"},
               {"id": "__codewiki_enhanced_rules", "path": str(Path(__file__).resolve().parents[2] / "integrations/codewiki/enhanced-learning.md"),
                "revision": "content-addressed"}, *config.get("methods", [])]
    for kind, entries in (("source", repos), ("document", config.get("materials", [])), ("method", methods)):
        for row in entries:
            key = row.get("id")
            require(isinstance(key, str) and re.fullmatch(r"[A-Za-z0-9_.-]+", key) and key not in ids,
                    "Unique material/repository id required")
            ids.add(key)
            root = Path(row.get("root", row.get("path", ""))).expanduser().resolve()
            require(root.exists() and not linked(root), "Material path missing or linked")
            require(not store.home.is_relative_to(root) and not root.is_relative_to(store.home),
                    "Workspace must be separate from all source/material roots")
            if kind == "source":
                require(root.is_dir(), "Repository root must be a directory")
            supplied.append({**row, "id": key, "root": str(root), "kind": kind})
    rows, documents = [], []
    for entry in supplied:
        root = Path(entry["root"])
        binding_source = imported is not None and entry["kind"] == "source"
        upstream = imported.source_assets(entry["id"]) if binding_source else {}
        before = []
        for p, excluded in walk(root):
            relative = p.relative_to(root).as_posix() if root.is_dir() else p.name
            local_link = None
            if entry.get("native_sources") and excluded == "linked_file":
                try:
                    target = p.resolve(strict=True)
                    if target.is_relative_to(root) and target.is_file():
                        local_link = {"link_target":target.relative_to(root).as_posix(),"link_text":os.readlink(p)}
                        excluded = None
                except (OSError,RuntimeError):
                    pass
            if entry.get("native_sources") and (excluded or not (
                    p.suffix.lower() in CPP | {".inl",".ipp",".tpp",".tcc",".in",".def",".y",".l",".s",".asm",".cu",".cuh"}
                    or (not p.suffix and "include" in relative.split("/")[:-1])
                    or relative in entry.get("additional_files", []))):
                continue
            known = upstream.pop(relative, None)
            if known and known.get("link_target"):
                # Git for Windows can check out a symlink as a file containing its target.
                # Resolve only a source-proven link and verify the target by the upstream content hash.
                placeholder = not excluded and p.is_file() and p.stat().st_size < 4096 and p.read_bytes() == os.fsencode(known["link_text"])
                if excluded == "linked_file" or placeholder:
                    local_target = (root / known["link_target"]).resolve()
                    require(local_target.is_relative_to(root),"ECS symlink target escapes checkout")
                    if excluded == "linked_file" and p.is_symlink():
                        require(os.readlink(p) == known["link_text"] or p.resolve() == local_target,
                                "Source symlink differs from ECS: "+relative)
                    rows.append(imported.bind_asset(store,known,local_target if local_target.is_file() else None))
                    continue
            if not excluded and entry.get("include") and not any(fnmatch.fnmatchcase(relative, rule) for rule in entry["include"]):
                excluded = "declared_scope_exclusion"
            if not excluded and any(fnmatch.fnmatchcase(relative, rule) for rule in entry.get("exclude", [])):
                excluded = "declared_scope_exclusion"
            if not excluded and (p.name.startswith(".env") or p.suffix.lower() in {".pem", ".key"} or p.name in {"id_rsa", "id_ed25519"}):
                excluded = "key_or_credential_material"
            record = {"key": entry["id"] + "/" + relative, "repo": entry["id"], "path": relative,
                      "kind": entry["kind"], "sha": None, "status": "excluded" if excluded else "pending",
                      "reason": excluded}
            if excluded and excluded.startswith("walk_error:"):
                record["status"] = "failed"
            if binding_source:
                record["inventory_origin"] = "checkout_only" if known is None else "checkout_and_ecs"
            if local_link:
                record.update(local_link)
            if excluded:
                rows.append(record)
                continue
            if known and known["status"] == "frozen":
                rows.append(imported.bind_asset(store, known, p))
                continue
            try:
                raw = p.read_bytes()
                sha = store.put_blob(raw)
                record.update(sha=sha, status="frozen", bytes=len(raw))
                before.append((p, sha))
                if entry["kind"] == "document":
                    require(p.suffix.lower() in TEXT_DOCS, "Unsupported material format")
                    text, parser, quality = extract(raw, p.suffix.lower())
                    require(bool(text.strip()), "Extracted material is empty")
                    text = text.replace("\r\n", "\n").replace("\r", "\n")
                    text_sha = store.put_blob(text.encode("utf-8"))
                    record.update(text_sha=text_sha, extraction=parser, extraction_quality=quality,
                                  material_kind=entry.get("material_kind", "manual"),
                                  document_status=entry.get("status", "unreviewed"),
                                  declared_revision=entry.get("revision", "unknown"))
                    lines = text.splitlines()
                    starts = [i for i, line in enumerate(lines) if re.match(r"^#{1,6}\s+\S", line)]
                    if not starts or starts[0] != 0:
                        starts.insert(0, 0)
                    for n, start in enumerate(starts):
                        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
                        if start < end:
                            documents.append({"asset": record["key"], "start": start + 1, "end": end,
                                              "text_sha": text_sha, "kind": record["material_kind"],
                                              "title": lines[start].lstrip("# ").strip(),
                                              "document_status": record["document_status"]})
            except (OSError, ValueError, UnicodeError, zipfile.BadZipFile, ET.ParseError) as error:
                record.update(status="frozen" if record["sha"] else "failed", extraction_error=str(error))
            rows.append(record)
        for relative, asset in sorted(upstream.items()):
            target = (root / relative).resolve()
            require(target.is_relative_to(root), "Invalid source path in ECS snapshot")
            rows.append(imported.bind_asset(store, asset, None))
        # Detect an input modified while this material was being captured.
        require(all(p.is_file() and digest(p.read_bytes()) == sha for p, sha in before),
                "Material changed during snapshot; retry from a stable checkout")
    if imported:
        extra, inherited_assets, blocks = imported.inherited_documents(store, ids)
        supplied.extend(extra)
        rows.extend(inherited_assets)
        documents.extend(blocks)
    normalized_profiles = []
    for profile in ([] if imported else config.get("profiles", [])):
        require(isinstance(profile.get("id"), str) and 1 <= len(profile["id"]) <= 96 and profile["id"] != "unknown", "Explicit profile id required")
        require(not any(p["id"] == profile["id"] for p in normalized_profiles), "Duplicate build profile id")
        repo = next((r for r in supplied if r["id"] == profile.get("repository") and r["kind"] == "source"), None)
        require(repo is not None, "Profile repository missing")
        commands = profile.get("commands", [])
        if profile.get("compile_commands"):
            raw = Path(profile["compile_commands"]).read_bytes()
            command_sha = store.put_blob(raw)
            try:
                commands = json.loads(raw.decode("utf-8-sig"))
            except (ValueError, UnicodeError) as error:
                commands = [{"error": str(error)}]
        else:
            command_sha = digest(commands)
        normalized, unavailable = [], []
        if not isinstance(commands, list):
            unavailable.append({"reason": "Compile database must be an array"})
            commands = []
        for entry in commands:
            try:
                normalized.append(_compile_entry(entry, Path(repo["root"])))
            except (ValueError, OSError, TypeError) as error:
                unavailable.append({"file": entry.get("file") if isinstance(entry, dict) else None, "reason": str(error)})
        unique = {canonical(e): e for e in normalized}
        item = {"id": profile["id"], "repository": repo["id"],
                "commands": list(unique.values()), "duplicate_commands": len(normalized) - len(unique),
                "compile_database_sha": command_sha, "unavailable_commands": unavailable, "extra_arguments": profile.get("extra_arguments", []),
                "toolchain": profile.get("toolchain", "unknown")}
        require(isinstance(item["extra_arguments"], list) and all(isinstance(a, str) for a in item["extra_arguments"]),
                "Profile extra_arguments must be strings")
        item["digest"] = digest(item)
        normalized_profiles.append(item)
    # An unknown profile is an explicit lexical-only path, never a wildcard build.
    normalized_profiles.append({"id": "unknown", "repository": None, "commands": [], "extra_arguments": [],
                                "toolchain": "unknown", "digest": digest({"profile": "unknown"})})
    declaration = [{**r, "git_head": git_identity(Path(r["root"])) if r["kind"] == "source" and not imported else None}
                   for r in supplied]
    content = {"materials": declaration, "assets": sorted(rows, key=lambda r: r["key"]),
               "profiles": normalized_profiles, "product": config.get("product", "unbound"),
               "revision": config.get("revision", "content-addressed"),
               "ownership": config.get("ownership", []), "execution_profile": "source_only",
               "methods_digest": digest(sorted((r["key"], r["sha"], r["status"]) for r in rows if r["kind"] == "method"))}
    if imported:
        content["source_index"] = imported.origin
        content["profiles"] = normalized_profiles = imported.snapshot["profiles"]
        heads = {r["id"]: r.get("git_head") for r in imported.snapshot["materials"] if r["kind"] == "source"}
        for r in declaration:
            if r["kind"] == "source":
                r["git_head"] = heads[r["id"]]
                checkout_root = Path(r["root"])
                r["checkout_head"] = git_identity(checkout_root) if (checkout_root/".git").exists() else None
                if r["git_head"] and r["checkout_head"]:
                    require(r["git_head"] == r["checkout_head"],"Checkout commit differs from the ECS source snapshot")
    sid = identity("snapshot", content)
    snapshot = {**content, "id": sid, "created": now(), "database_execution": "not_run"}
    with store.transaction():
        existing = store.db.execute("SELECT 1 FROM snapshots WHERE id=?", (sid,)).fetchone()
        if existing:
            if not imported:
                store.set_meta("snapshot_head", sid)
            return store.record("snapshots", sid)
        store.db.execute("INSERT INTO snapshots VALUES(?,?,?)", (sid, snapshot["created"], canonical(snapshot)))
        for row in rows:
            store.db.execute("INSERT INTO assets VALUES(?,?,?,?,?,?,?,?)",
                             (sid, row["key"], row["repo"], row["path"], row["sha"], row["kind"], row["status"], canonical(row)))
        for row in normalized_profiles:
            store.db.execute("INSERT INTO profiles VALUES(?,?,?,?)", (sid, row["id"], row["digest"], canonical(row)))
        for block in documents:
            anchor = store.anchor(sid, block["asset"], block["start"], block["end"], text_sha=block["text_sha"])
            block.update(id=identity("document", [sid, anchor["id"]]), snapshot=sid, anchor=anchor["id"])
            store.db.execute("INSERT INTO documents VALUES(?,?,?,?,?)",
                             (sid, block["id"], block["kind"], block["asset"], canonical(block)))
        if not imported:
            store.set_meta("snapshot_head", sid)
        store.event("snapshot", {"id": sid, "assets": len(rows), "documents": len(documents)})
    return snapshot
