"""Cache parsed translation units by their own inputs and include resolution."""
import os
from pathlib import Path
import re

from .store import digest


def environment():
    return digest({k: os.environ.get(k) for k in (
        "CPATH", "C_INCLUDE_PATH", "CPLUS_INCLUDE_PATH", "INCLUDE", "SDKROOT",
        "MACOSX_DEPLOYMENT_TARGET", "LIBCLANG_LIBRARY_PATH")})


def parse_key(repository, entry, arguments, profile, tools, source_sha):
    # Keep command provenance in the snapshot. Only parser inputs belong here.
    return digest(["native-tu/v2", repository, entry["file"], source_sha,
                   entry["arguments"][:1], arguments, profile.get("toolchain"),
                   tools["libclang"], tools["clang_worker"], environment()])


def locator(path, originals):
    path = Path(os.path.abspath(path))
    for repo, root in originals.items():
        if path.is_relative_to(root):
            return "asset:" + repo + "/" + path.relative_to(root).as_posix()
    return "file:" + str(path)


def present(store, snapshot, key):
    if key.startswith("file:"):
        path = Path(key[5:])
        return str(path.resolve()) if path.is_file() else None
    row = store.db.execute("SELECT status FROM assets WHERE snapshot=? AND key=?",
                           (snapshot, key[6:])).fetchone()
    return bool(row and row[0] == "frozen")


def guard(store, snapshot, source_key, arguments, originals, includes):
    """Track literal include lookup alternatives, including previously absent names.

    For computed names, include_next and filesystem feature tests, decline reuse
    across builds. A positive dependency manifest alone cannot prove a cache hit.
    """
    roots, probes = [], {}
    # An explicit closed search path makes literal negative lookups reproducible.
    closed_search = "-nostdinc" in arguments and not any(os.environ.get(k) for k in
        ("CPATH", "C_INCLUDE_PATH", "CPLUS_INCLUDE_PATH", "INCLUDE"))
    for i, value in enumerate(arguments):
        if value in ("-I", "-iquote", "-isystem"):
            roots.append(Path(arguments[i + 1]))
        elif value.startswith("-I") and len(value) > 2:
            roots.append(Path(value[2:]))
    inputs = [{"asset": source_key}, *includes]
    for item in inputs:
        if item.get("asset"):
            key = item["asset"]
            repo, path = key.split("/", 1)
            parent = (originals[repo] / path).parent
            raw = store.blob(store.asset(snapshot, key)["sha"])
        else:
            path = Path(item["path"])
            parent, raw = path.parent, path.read_bytes()
        text = raw.decode("utf-8", errors="replace").replace("\\\n", "").replace("\\\r\n", "")
        if re.search(r"__TIMESTAMP__|__TIME__|__DATE__|#\s*(?:include_next|import)\b", text):
            return None
        if "__has_include" in text:
            if not closed_search:
                return None
            parts = list(re.finditer(r'__has_include\s*\(\s*[<"]([^">]+)[>"]\s*\)', text))
            if len(parts) != text.count("__has_include"):
                return None
            for match in parts:
                for directory in [parent, *roots]:
                    key = locator(directory / match[1], originals)
                    probes[key] = present(store, snapshot, key)
        for directive in re.findall(r"(?m)^\s*#\s*include\s*([^\n]+)", text):
            m = re.match(r'\s*[<"]([^>"]+)[>"]', directive)
            if not m:
                return None
            for directory in [parent, *roots]:
                key = locator(directory / m[1], originals)
                if key not in probes:
                    probes[key] = present(store, snapshot, key)
    return probes


def valid(store, snapshot, payload):
    probes = payload.get("lookup_guard")
    if probes is None or any(present(store, snapshot, k) != v for k, v in probes.items()):
        return False
    for item in payload["includes"]:
        if item.get("asset"):
            row = store.db.execute("SELECT sha FROM assets WHERE snapshot=? AND key=?",
                                   (snapshot, item["asset"])).fetchone()
            if not row or row[0] != item["sha"]:
                return False
        else:
            path = Path(item["path"])
            if not path.is_file() or digest(path.read_bytes()) != item["sha"]:
                return False
    return True
