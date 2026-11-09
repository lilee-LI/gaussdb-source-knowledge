"""Read four-input learning declarations without executing build commands.

The original feature/CDB files become frozen materials.  The normalized CDB is
an inventory descriptor for the host: it is never a substitute for the original
database on the real compiler/ECS host.  Mapping is explicitly not compilation.
"""
from __future__ import annotations

from collections import defaultdict
import csv
import io
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import shlex
import stat
import unicodedata

from .store import atomic_write, digest, identity, require

SCHEMA = "learning-inputs/v1"
_ALIASES = {
    "name": ("name", "feature", "feature_name", "title", "特性名称", "特性名", "名称", "功能名称"),
    "external_id": ("external_id", "feature_id", "id", "特性编号", "编号"),
    "aliases": ("aliases", "alias", "别名"),
    "version": ("version", "revision", "版本"),
    "module_hint": ("module_hint", "module", "owner_module", "模块", "所属模块"),
    "description": ("description", "summary", "描述", "说明"),
    "parent": ("parent", "parent_id", "父级"),
}
_OMIT = {".git", ".svn", ".claude", ".codex", ".codegraph", ".codewiki", ".serena", ".venv", "node_modules", "__pycache__"}


def _normal(value):
    return " ".join(unicodedata.normalize("NFKC", str(value)).strip().casefold().split())


def _declaration(spec, key):
    value = spec.get(key)
    if not value:
        return None
    row = {"path": value} if isinstance(value, (str, Path)) else dict(value)
    require(row.get("path"), key + " requires a path")
    path = Path(row["path"]).expanduser().resolve()
    require(path.is_file(), key + " file does not exist: " + str(path))
    return {**row, "path": str(path)}


def _list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    return [x.strip() for x in re.split(r"[;|；]", str(value)) if x.strip()]


def _fields(row, declaration):
    require(isinstance(row, (str, dict)), "Each feature is a name or an object")
    if isinstance(row, str):
        return {"name": row}
    keys = {_normal(k): k for k in row}
    columns = declaration.get("columns", {})
    result = {}
    for field, choices in _ALIASES.items():
        column = columns.get(field)
        matched = column if column in row else next((keys[_normal(x)] for x in choices if _normal(x) in keys), None)
        if matched is not None:
            result[field] = row[matched]
    # Compatibility with a names-only export whose column is explicitly mapped.
    return result


def _feature_rows(raw, suffix, declaration):
    text = raw.decode("utf-8-sig")
    if suffix == ".json":
        value = json.loads(text)
        prefix = ""
        if isinstance(value, dict):
            require(isinstance(value.get("features"), list), "Feature JSON object needs a features array")
            value = value["features"]; prefix = "/features"
        require(isinstance(value, list), "Feature JSON must be an array")
        return [(r, None, i + 1, prefix + "/" + str(i)) for i, r in enumerate(value)]
    if suffix == ".csv":
        reader = csv.reader(io.StringIO(text))
        found = []
        for row in reader:
            if any(cell.strip() for cell in row):
                found.append((row, reader.line_num))
        if not found:
            return []
        header = found[0][0]
        known_names = {_normal(x) for x in _ALIASES["name"]}
        custom = declaration.get("columns", {}).get("name")
        has_header = any(_normal(x) in known_names or x == custom for x in header)
        if not has_header:
            require(all(len(row) == 1 for row, _ in found), "A multi-column feature CSV needs a name column")
            return [(row[0], line, n + 1, None) for n, (row, line) in enumerate(found)]
        require(len({_normal(x) for x in header}) == len(header), "Feature CSV contains duplicate columns")
        return [(dict(zip(header, row)), line, n + 1, None) for n, (row, line) in enumerate(found[1:])]
    require(suffix in {".md", ".markdown", ".txt"}, "Features support CSV, JSON, Markdown or UTF-8 TXT")
    rows = []
    table_header = None
    for line, value in enumerate(text.splitlines(), 1):
        value = value.strip()
        if not value or value.startswith("#") or value.startswith("<!--"):
            continue
        if value.startswith("|") and value.endswith("|"):
            cells = [x.strip() for x in value.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", x.replace(" ", "")) for x in cells):
                continue
            if table_header is None:
                table_header = cells
                require(any(_normal(x) in {_normal(y) for y in _ALIASES["name"]} for x in cells),
                        "Markdown feature table needs a name column")
                continue
            rows.append((dict(zip(table_header, cells)), line, len(rows) + 1, None))
        else:
            name = re.sub(r"^(?:[-*+]\s+|\d+[.)、]\s*)", "", value).strip()
            rows.append((name, line, len(rows) + 1, None))
    return rows


def _features(declaration, product):
    if not declaration:
        return [], [], None
    path = Path(declaration["path"]); raw = path.read_bytes()
    rows = _feature_rows(raw, path.suffix.lower(), declaration)
    records = []; issues = []; groups = defaultdict(list)
    for row, line, number, pointer in rows:
        fields = _fields(row, declaration)
        name = str(fields.get("name", "")).strip()
        require(name, "Feature name is empty at row " + str(number))
        external_value = fields.get("external_id")
        external = str(external_value).strip() if external_value is not None else ""
        fid = identity("feature", [product, "external" if external else "name", external or _normal(name)])
        record = {"id": fid, "name": name, "external_id": external or None,
                  "aliases": _list(fields.get("aliases")), "version": str(fields.get("version", declaration.get("version", "unknown")) or "unknown"),
                  "module_hint": fields.get("module_hint"), "description": str(fields.get("description", "") or ""),
                  "parent": fields.get("parent"), "source_path": str(path), "source_line": line,
                  "source_lines": [line] if line is not None else [], "source_row": number,
                  "source_pointer": pointer, "row_id": identity("feature-row", [str(path), number, pointer]),
                  "status": "not_located", "mapping": "requires_source_research"}
        groups[fid].append(record); records.append(record)
    for fid, same in groups.items():
        if len({_normal(r["name"]) for r in same}) > 1:
            for record in same:record["status"] = "ambiguous"
            issues.append({"kind": "ambiguous_feature_identity", "feature": fid,
                           "rows": [r["source_row"] for r in same], "names": sorted({r["name"] for r in same})})
        else:
            for record in same[1:]:
                record["status"] = "duplicate"; record["duplicate_of"] = same[0]["row_id"]
    info = {"path": str(path), "sha256": digest(raw), "format": path.suffix.lower(), "rows": len(records)}
    return records, issues, info


def _path(value):
    value = str(value).replace("\\", "/")
    return posixpath.normpath(value)


def _absolute(value):
    return value.startswith("/") or bool(re.match(r"^[A-Za-z]:/", value))


def _join(directory, file):
    return _path(file if _absolute(_path(file)) else posixpath.join(_path(directory), _path(file)))


def _source_index(source):
    by_name = defaultdict(list)
    def is_link(path):
        value = path.lstat()
        return stat.S_ISLNK(value.st_mode) or bool(getattr(value, "st_file_attributes", 0) & 0x400)
    for parent, dirs, names in os.walk(source, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in _OMIT and not is_link(Path(parent) / d))
        for name in names:
            p = Path(parent) / name
            if name not in _OMIT and not is_link(p) and p.is_file():
                by_name[name.casefold()].append(p.resolve())
    return by_name


def _mapped_file(reference, original_file, source, maps, index):
    attempts = []
    # A real host path is accepted only inside the declared source directory.
    for candidate in (reference, original_file):
        p = Path(candidate)
        if p.is_absolute():
            attempts.append((p.resolve(), "host_path"))
    normalized = _path(reference)
    for row in maps:
        require(isinstance(row, dict) and isinstance(row.get("from"), str) and row.get("to"), "path_maps uses from/to objects")
        before = _path(row["from"]).rstrip("/"); key = normalized
        compare, prefix = (key.casefold(), before.casefold()) if re.match(r"^[A-Za-z]:", before) else (key, before)
        if compare == prefix or compare.startswith(prefix + "/"):
            tail = key[len(before):].lstrip("/")
            attempts.append(((Path(row["to"]).expanduser().resolve() / tail).resolve(), "explicit_path_map"))
    if not _absolute(_path(original_file)):
        attempts.append(((source / _path(original_file)).resolve(), "source_relative"))
    for p, method in attempts:
        if p.is_relative_to(source) and p.is_file() and not p.is_symlink():
            return p, method, []
    basename = PurePosixPath(normalized).name.casefold()
    choices = index.get(basename, [])
    parts = PurePosixPath(normalized).parts
    scored = []
    for candidate in choices:
        relative = candidate.relative_to(source).parts
        count = 0
        for a, b in zip(reversed(parts), reversed(relative)):
            if (a.casefold() if os.name == "nt" else a) != (b.casefold() if os.name == "nt" else b):break
            count += 1
        if count:scored.append((count, candidate))
    best = max((n for n, _ in scored), default=0)
    winners = [p for n, p in scored if n == best]
    if len(winners) == 1:
        return winners[0], "unique_source_suffix", []
    return None, "ambiguous_source_suffix" if winners else "unlocated", [p.relative_to(source).as_posix() for p in winners[:20]]


def _arguments(entry, directory):
    args = entry.get("arguments")
    if args is not None:
        require(isinstance(args, list) and args and all(isinstance(x, str) for x in args), "arguments must be a nonempty string array")
        return list(args)
    command = entry.get("command")
    require(isinstance(command, str) and command.strip(), "compile command needs arguments or command")
    windows = bool(re.match(r"^[A-Za-z]:[/\\]", str(directory)))
    args = shlex.split(command, posix=not windows)
    if windows:
        args = [x[1:-1] if len(x) > 1 and x[0] == x[-1] == '"' else x for x in args]
    require(args, "compile command is empty")
    return args


def _flags(args):
    defines = []; includes = []; i = 1
    while i < len(args):
        flag = args[i]
        if flag in {"-D", "/D", "-I", "/I", "-isystem", "-iquote"}:
            if i + 1 < len(args):
                (defines if flag in {"-D", "/D"} else includes).append(args[i + 1]); i += 2; continue
        elif flag.startswith(("-D", "/D")) and len(flag) > 2:defines.append(flag[2:])
        elif flag.startswith(("-I", "/I")) and len(flag) > 2:includes.append(flag[2:])
        i += 1
    return defines, includes


def _compile(declaration, source, maps):
    if not declaration:
        return [], [], [], None
    path = Path(declaration["path"]); raw = path.read_bytes()
    entries = json.loads(raw.decode("utf-8-sig")); require(isinstance(entries, list), "Compilation database must be a JSON array")
    index = _source_index(source); contexts = []; normalized = []; issues = []; seen = set()
    maps = declaration.get("path_maps", maps)
    require(isinstance(maps, list), "path_maps must be an array")
    for number, entry in enumerate(entries, 1):
        row = {"source_row": number, "source_path": str(path), "source_pointer": "/" + str(number - 1),
               "analysis_status": "not_run", "binding": "unparsed", "status": "invalid", "asset": None, "file": None,
               "original_entry": entry, "mapping_method": None, "issues": []}
        try:
            require(isinstance(entry, dict) and isinstance(entry.get("file"), str) and entry["file"].strip(), "compile entry requires a file string")
            directory = entry.get("directory", str(path.parent))
            require(isinstance(directory, str) and directory, "compile directory must be a string")
            if not _absolute(_path(directory)):directory = _join(str(path.parent), directory)
            args = _arguments(entry, directory)
            reference = _join(directory, entry["file"])
            defines, includes = _flags(args)
            cid = identity("compile-context", [directory, reference, args, entry.get("output")])
            row.update(id=cid, original_directory=entry.get("directory", str(path.parent)), original_file=entry["file"],
                       original_arguments=args, original_command=entry.get("command"), original_output=entry.get("output"),
                       file_reference=reference, compiler=args[0], defines=defines, includes=includes)
            mapped, method, choices = _mapped_file(reference, entry["file"], source, maps, index)
            row["mapping_method"] = method
            if mapped:
                relative = mapped.relative_to(source).as_posix()
                row.update(status="mapped", file=relative, asset="server/" + relative, mapped_file=str(mapped))
                normalized.append({"directory": str(source), "file": str(mapped), "arguments": args,
                                   **({"output": entry["output"]} if entry.get("output") else {})})
            else:
                row["status"] = "ambiguous" if choices else "unlocated"
                row["candidates"] = choices
                row["issues"].append({"kind": row["status"] + "_compile_file", "file_reference": reference, "candidates": choices})
            if cid in seen:row["duplicate_of"] = cid
            seen.add(cid)
        except (ValueError, TypeError, OSError) as error:
            row["issues"].append({"kind": "invalid_compile_entry", "reason": str(error)})
        row.setdefault("id", identity("compile-context-invalid", [entry, number]))
        contexts.append(row)
        issues.extend({"source_row": number, **item} for item in row["issues"])
    return contexts, normalized, issues, {"path": str(path), "sha256": digest(raw), "entries": len(entries)}


def prepare(spec, output_dir):
    """Return/write a deterministic manifest and host-only inventory CDB.

    Returned feature records preserve every original row, including duplicates.
    compile_contexts preserve every original command, including invalid/unmapped
    entries.  summary.features is the number of distinct feature identities.
    """
    source = Path(spec["source"]).expanduser().resolve()
    require(source.is_dir(), "Source directory does not exist")
    feature_decl = _declaration(spec, "features")
    compile_decl = _declaration(spec, "compile_db")
    features, feature_issues, feature_info = _features(feature_decl, spec.get("product", "unbound"))
    contexts, normalized, compile_issues, compile_info = _compile(compile_decl, source, spec.get("path_maps", []))
    materials = []
    if feature_decl:
        materials.append({"id": "historical_features", "path": feature_decl["path"], "material_kind": "feature_catalog",
                          "status": "unreviewed", "revision": feature_decl.get("version", "user-material-snapshot")})
    if compile_decl:
        materials.append({"id": "compile_database", "path": compile_decl["path"], "material_kind": "build_context",
                          "status": "unreviewed", "revision": "original-compilation-database"})
    summary = {"features": len({r["id"] for r in features}), "feature_rows": len(features),
               "duplicates": sum(r["status"] == "duplicate" for r in features),
               "ambiguous": sum(r["status"] == "ambiguous" for r in features),
               "compile_contexts": len(contexts), "mapped_contexts": sum(r["status"] == "mapped" for r in contexts),
               "unlocated_contexts": sum(r["status"] != "mapped" for r in contexts),
               "source_files_in_compile_db": len({r["file"] for r in contexts if r["file"]})}
    value = {"schema": SCHEMA, "source_root": str(source), "inputs": {"features": feature_info, "compile_db": compile_info},
             "features": features, "compile_contexts": contexts, "materials": materials, "summary": summary,
             "issues": feature_issues + compile_issues,
             "capabilities": {"tu_parsing": "not_run", "compiler_bindings_verified": False,
                              "normalized_cdb_purpose": "host inventory only; use original CDB on real build/ECS host"}}
    value["digest"] = digest(value)
    folder = Path(output_dir).expanduser().resolve() / ("inputs-" + value["digest"][:24])
    value["manifest_path"] = str(folder / "manifest.json")
    value["normalized_compile_db"] = str(folder / "compile_commands.inventory.json") if normalized else None
    if normalized:
        atomic_write(value["normalized_compile_db"], json.dumps(normalized, ensure_ascii=False, indent=2) + "\n")
    atomic_write(value["manifest_path"], json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    return value


def contexts(store,module=None,asset=None,offset=0,limit=20):
    """Bounded build declarations for one module; never compiler validation."""
    from .study import current
    require(type(offset) is int and offset>=0 and type(limit) is int and 1<=limit<=100,'Read 1..100 compile contexts per page')
    plan=current(store);manifest=store.get_meta('learning_inputs',{})
    if module:require(module in plan['modules'],'Unknown build-context module')
    allowed=set(plan['modules'][module]['files']) if module else None
    rows=[r for r in manifest.get('compile_contexts',[]) if (allowed is None or r.get('asset') in allowed) and (not asset or r.get('asset')==asset)]
    fields=('id','source_row','source_pointer','status','asset','file','original_file','original_directory','compiler','defines','includes','analysis_status','binding','mapping_method','issues')
    cdb=manifest.get('inputs',{}).get('compile_db') or {}
    return {'schema':'compile-context-page/v1','total':len(rows),
        'items':[{k:r.get(k) for k in fields} for r in rows[offset:offset+limit]],
        'next_offset':offset+limit if offset+limit<len(rows) else None,
        'frozen_material':'compile_database/'+Path(cdb['path']).name if cdb.get('path') else None,
        'evidence':'Declarations only. Search/read the frozen CDB material for citations; this query creates no read receipts.',
        'compiler_validation':'not_inferred'}
