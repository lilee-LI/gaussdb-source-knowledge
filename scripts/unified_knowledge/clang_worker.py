"""Isolated libclang frontend. Parses only; never invokes a compiler command."""
from __future__ import annotations

import json
import ctypes
from functools import lru_cache
from pathlib import Path
import sys

from .store import Store, atomic_write, canonical, digest, identity


def parse(request):
    if request.get("frontend")=="gcc":
        from .gcc_frontend import parse as gcc_parse
        return gcc_parse(request)
    from clang import cindex as c
    roots = {key: Path(value).resolve() for key, value in request["roots"].items()}

    def locate(path):
        return locate_name(str(path)) if path else None

    @lru_cache(maxsize=8192)
    def locate_name(name):
        p = Path(name).resolve()
        for repo, root in roots.items():
            if p.is_relative_to(root):
                return repo + "/" + p.relative_to(root).as_posix()
        return None

    index = c.Index.create()
    calls_only = request.get("facts") == "calls"
    tu = index.parse(request["file"], args=request["arguments"],
                     options=0 if calls_only else c.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
    symbols, relations, includes = {}, [], {}
    functions = {"FUNCTION_DECL", "CXX_METHOD", "CONSTRUCTOR", "DESTRUCTOR", "FUNCTION_TEMPLATE", "CONVERSION_FUNCTION"}
    accepted = functions | {"STRUCT_DECL", "CLASS_DECL", "UNION_DECL", "CLASS_TEMPLATE", "FIELD_DECL",
                            "VAR_DECL", "PARM_DECL", "TYPEDEF_DECL", "ENUM_DECL", "ENUM_CONSTANT_DECL",
                            "MACRO_DEFINITION", "MACRO_INSTANTIATION"}
    uses = {"CALL_EXPR", "DECL_REF_EXPR", "MEMBER_REF_EXPR", "TYPE_REF", "MACRO_INSTANTIATION"}
    if calls_only:
        accepted, uses = functions, {"CALL_EXPR"}

    def source_position(location, function):
        native = getattr(c.conf.lib, function)
        native.argtypes = [c.SourceLocation, ctypes.POINTER(c.c_object_p),
                           ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
        native.restype = None
        file, line, column, offset = c.c_object_p(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
        native(location, ctypes.byref(file), ctypes.byref(line), ctypes.byref(column), ctypes.byref(offset))
        return {"asset": locate(c.File(file).name) if file else None,
                "line": line.value, "column": column.value, "offset": offset.value}

    def describe(cur):
        asset = locate(cur.location.file)
        if asset is None:
            return None
        usr = cur.get_usr()
        occurrence = [asset, usr or [cur.kind.name, cur.spelling, cur.location.offset]]
        if cur.kind.name in functions and usr:
            occurrence.extend([cur.is_definition(), cur.location.offset])
            if cur.linkage.name in {"INTERNAL", "UNIQUE_EXTERNAL", "NO_LINKAGE"}:
                occurrence.append(request["unit_file"])
        logical = identity("symbol", occurrence)
        start, end = cur.extent.start.line, cur.extent.end.line
        return {"logical": logical, "name": cur.spelling or cur.displayname, "asset": asset,
                "linkage": cur.linkage.name,
                "kind": cur.kind.name.lower(), "usr": usr, "start": max(start, 1), "end": max(end, start, 1),
                "offset": cur.location.offset, "definition": cur.is_definition(),
                "type": cur.type.spelling, "resolution": "resolved",
                "spelling": cur.displayname, "frontend_selected": True,
                "spelling_location": source_position(cur.location, "clang_getSpellingLocation"),
                "expansion_location": source_position(cur.location, "clang_getExpansionLocation")}

    def add(cur):
        value = describe(cur)
        if value:
            prior = symbols.get(value["logical"])
            if prior is None or (value["definition"] and not prior["definition"]):
                symbols[value["logical"]] = value
        return value

    def target(cur):
        ref = cur.referenced
        if ref is None:
            return None
        definition = ref.get_definition()
        return add(definition if definition is not None else ref)

    stack = [(tu.cursor, None)]
    while stack:
        cur, owner = stack.pop()
        k = cur.kind.name
        asset = locate(cur.location.file)
        if cur.location.file is not None and asset is None:
            continue  # Compiler/system headers are dependencies, not repository symbols.
        value = add(cur) if k in accepted else None
        next_owner = value["logical"] if value and (k in functions or (owner is None and k in {"VAR_DECL", "FIELD_DECL"})) else owner
        if k in uses and asset:
            ref = target(cur)
            kind = {"CALL_EXPR": "CALLS", "MEMBER_REF_EXPR": "FIELD_REF",
                    "TYPE_REF": "TYPE_REF", "MACRO_INSTANTIATION": "EXPANDS"}.get(k, "REFERS_TO")
            resolution = "resolved" if ref else "unresolved"
            if k == "CALL_EXPR" and ref and ref["kind"].upper() not in functions:
                resolution = "candidate"
            dispatch = None
            if k == "CALL_EXPR" and cur.referenced is not None and cur.referenced.kind.name == "CXX_METHOD" and cur.referenced.is_virtual_method():
                dispatch, resolution = "virtual", "candidate"
            relations.append({"source": owner or identity("file", asset), "dispatch": dispatch,
                              "target": ref["logical"] if ref else identity("unresolved", [asset, cur.location.offset, cur.spelling]),
                              "kind": kind, "resolution": resolution, "asset": asset,
                              "start": max(1, cur.extent.start.line), "end": max(1, cur.extent.end.line),
                              "name": cur.spelling, "offset": cur.location.offset,
                              "spelling_location": source_position(cur.location, "clang_getSpellingLocation"),
                              "expansion_location": source_position(cur.location, "clang_getExpansionLocation")})
        if cur.kind.is_preprocessing() and k == "MACRO_DEFINITION" and value:
            value["definition_tokens"] = " ".join(t.spelling for t in cur.get_tokens())
        stack.extend((child, next_owner) for child in reversed(list(cur.get_children())))
    with Store(request["home"], readonly=True) as evidence:
        for include in tu.get_includes():
            key = locate(include.include)
            path = Path(str(include.include)).resolve()
            if str(path) not in includes:
                if key:
                    sha = evidence.asset(request["snapshot"], key)["sha"]
                    evidence.blob(sha)
                else:
                    sha = digest(path.read_bytes())
                includes[str(path)] = {"asset": key, "sha": sha, "path": str(path)}
            source = locate(include.source)
            if source and not calls_only:
                relations.append({"source": identity("file", source),
                                  "target": identity("file", key) if key else identity("external", str(path)),
                                  "kind": "INCLUDES", "resolution": "resolved" if key else "external",
                                  "asset": source, "start": max(1, include.location.line),
                                  "end": max(1, include.location.line), "name": key or str(path)})
    diagnostics = [{"severity": d.severity, "message": d.spelling, "asset": locate(d.location.file),
                    "file":str(d.location.file) if d.location.file else None,
                    "line": d.location.line} for d in tu.diagnostics]
    return {"symbols": list(symbols.values()), "relations": relations,
            "includes": list(includes.values()), "diagnostics": diagnostics,
            "status": "partial" if any(d["severity"] >= 3 for d in diagnostics) else "parsed"}


def main():
    request = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    try:
        result = parse(request)
    except Exception as error:
        result = {"symbols": [], "relations": [], "includes": [], "diagnostics": [],
                  "status": "failed", "error": type(error).__name__ + ": " + str(error)}
    atomic_write(sys.argv[2], canonical(result))


if __name__ == "__main__":
    main()
