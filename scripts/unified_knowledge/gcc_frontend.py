"""Read original GCC language semantics through a locally built, version-checked plugin."""
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import json
import os
import signal
from pathlib import Path
import shlex
import shutil
import subprocess
import time

from .store import atomic_write, canonical, digest, identity, require


def is_cpp(entry):
    argv = entry["arguments"]
    language = None
    for i,value in enumerate(argv[:-1]):
        if value=="-x":
            language = argv[i+1]
    if language and language!="none":
        return "++" in language
    driver = argv[1] if Path(argv[0]).name in {"ccache","sccache","distcc"} else argv[0]
    return "++" in Path(driver).name or Path(entry["file"]).suffix!=".c"


def compiler_info(driver):
    binary = shutil.which(str(driver))
    require(binary, "Build compiler missing: " + str(driver))
    binary = Path(binary).resolve()
    result = subprocess.run([str(binary), "--version"], capture_output=True, text=True, timeout=20)
    require(result.returncode == 0, "Cannot query configured build compiler")
    require("clang" not in result.stdout.lower() and any(x in result.stdout.lower() for x in ("gcc", "g++", "free software foundation")),
            "The GCC frontend requires a GCC build compiler")
    version = subprocess.check_output([str(binary), "-dumpfullversion", "-dumpversion"], text=True, timeout=20).strip()
    plugin = Path(subprocess.check_output([str(binary), "-print-file-name=plugin"], text=True, timeout=20).strip())
    require((plugin / "include/gcc-plugin.h").is_file(),
            "Matching GCC plugin headers are missing for " + str(binary) + "; install its exact plugin-devel package or explicitly use --frontend clang")
    return {"binary":str(binary), "sha256":digest(binary.read_bytes()), "version":version,
            "plugin_headers":str(plugin / "include"), "banner":result.stdout.splitlines()[0]}


def build_plugin(work, driver, cxx_driver, *, cpp=True):
    info = compiler_info(driver)
    host = compiler_info(cxx_driver)
    require(info["version"] == host["version"], "Build the GCC plugin with the matching C++ compiler version")
    source = Path(__file__).resolve().parents[1] / "native/gausskb_gcc.cpp"
    headers = Path(info["plugin_headers"])
    version_sha = digest((headers / "plugin-version.h").read_bytes())
    key = digest([source.read_bytes().hex(), info, host, version_sha, cpp])
    folder = work / "plugins" / key
    binary = folder / "gausskb_gcc.so"
    receipt = folder / "build.json"
    if binary.is_file() and receipt.is_file():
        old = json.loads(receipt.read_bytes())
        require(old["sha256"] == digest(binary.read_bytes()), "Cached GCC plugin was modified")
        return old
    folder.mkdir(parents=True, exist_ok=True)
    command = [host["binary"], "-std=c++14", "-shared", "-fPIC", "-fno-rtti", "-I" + str(headers)]
    # Standalone product toolchains commonly place GMP beside their gcc/ directory.
    gmp = Path(host["binary"]).parent.parent.parent / "gmp/include"
    if gmp.is_dir():
        command.append("-I" + str(gmp))
    if cpp:
        command.append("-DGAUSSKB_CXX")
    temporary = binary.with_suffix(".building.so")
    proc = subprocess.run([*command, str(source), "-o", str(temporary)], capture_output=True, text=True, timeout=120)
    require(proc.returncode == 0, "Cannot build the matching GCC analysis plugin: " + proc.stderr[-3000:])
    temporary.replace(binary)
    result = {"path":str(binary), "sha256":digest(binary.read_bytes()), "source_sha256":digest(source.read_bytes()),
              "compiler":info, "cpp":cpp, "plugin_headers_version_sha256":version_sha}
    atomic_write(receipt, canonical(result))
    return result


def dependencies(entries, source, work, cc, cxx, jobs, timeout):
    """Resolve real includes before freezing, including macro-selected data files."""
    from .indexer import compiler_arguments
    roots = {"server":source}
    directory = work / "dependency-probes"
    directory.mkdir(exist_ok=True)

    def one(pair):
        number, entry = pair
        cpp = is_cpp(entry)
        driver = cxx if cpp else cc
        output = directory / (str(number) + ".d")
        argv = compiler_arguments(entry, {}, roots, roots)
        proc = subprocess.run([driver, *argv, "-M", "-MT", "gausskb", "-MF", str(output), str(source / entry["file"])],
                              cwd=entry["directory"], capture_output=True, text=True, timeout=timeout)
        if proc.returncode or not output.is_file():
            return {"entry":number,"file":entry["file"],"error":proc.stderr[-2000:]}, []
        text = output.read_text().replace("\\\n", " ")
        # The target is fixed by us. shlex decodes Make's backslash-escaped paths.
        names = shlex.split(text.split(":", 1)[1], comments=False)
        files = []
        for name in names:
            path = (Path(entry["directory"]) / name).resolve()
            if path.is_file() and path.is_relative_to(source):
                files.append(path.relative_to(source).as_posix())
        return None, files

    started = time.monotonic()
    included, errors = set(), []
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for error, files in pool.map(one, enumerate(entries)):
            included.update(files)
            if error:
                errors.append(error)
    manifest = {"files":sorted(included), "errors":errors}
    atomic_write(directory / "manifest.json", canonical(manifest))
    return sorted(included), {"invocations":len(entries), "files":len(included), "errors":errors,
                              "sha256":digest(manifest), "seconds":round(time.monotonic()-started,3)}


def parse(request):
    output = Path(request["gcc_output"])
    args = [request["gcc_driver"], *request["arguments"], "-fsyntax-only", "-fdiagnostics-format=json",
            "-fplugin=" + request["gcc_plugin"], "-fplugin-arg-gausskb_gcc-output=" + str(output)]
    args.extend("-fplugin-arg-gausskb_gcc-root=" + root
                for group in (request["roots"],request["original_roots"]) for root in group.values())
    # Rebase builtin __FILE__/__BASE_FILE__ values while parsing immutable copies.
    args.extend("-ffile-prefix-map="+root+"="+request["original_roots"][repo]
                for repo,root in request["roots"].items())
    proc = subprocess.Popen([*args,request["file"]],stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                            text=True,start_new_session=True)
    try:
        stdout, stderr = proc.communicate(timeout=request.get("timeout",300))
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid,signal.SIGKILL)
        proc.communicate()
        output.unlink(missing_ok=True)
        return {"symbols":[],"relations":[],"includes":[],"diagnostics":[],"status":"failed","error":"GCC TU timeout"}
    diagnostics = []
    try:
        for item in json.loads(stderr or "[]"):
            caret = next(iter(item.get("locations", [])), {}).get("caret", {})
            diagnostics.append({"severity":{"error":3,"fatal error":4,"warning":2,"note":1}.get(item["kind"],2),
                                "message":item["message"], "file":caret.get("file"), "line":caret.get("line",0)})
    except (ValueError, KeyError, TypeError):
        if stderr.strip():
            diagnostics.append({"severity":3 if proc.returncode else 2,"message":stderr[-4000:],"line":0})
    if not output.is_file():
        return {"symbols":[], "relations":[], "includes":[], "diagnostics":diagnostics,
                "status":"failed", "error":"GCC produced no analysis stream"}
    try:
        return decode(output, request, diagnostics, proc.returncode)
    finally:
        output.unlink(missing_ok=True)


def decode(output, request, diagnostics, returncode=0):
    roots = {key:Path(value).resolve() for key,value in request["roots"].items()}
    originals = {key:Path(value).resolve() for key,value in request["original_roots"].items()}
    files, symbols, calls, include_paths = {}, {}, [], set()

    @lru_cache(maxsize=8192)
    def resolved(name):
        return Path(name).resolve()

    @lru_cache(maxsize=8192)
    def frozen_path(name):
        if not name or name.startswith("<"):
            return None
        if not Path(name).is_absolute():
            return None
        path = resolved(name)
        for group in (roots,originals):
            for repo,root in group.items():
                if path.is_relative_to(root):
                    return roots[repo]/path.relative_to(root)
        return None

    @lru_cache(maxsize=8192)
    def locate(name):
        path = frozen_path(name)
        if path:
            for repo,root in roots.items():
                if path.is_relative_to(root):
                    return repo+"/"+path.relative_to(root).as_posix()
        return None

    def position(value):
        name = value.get("file")
        if not name or name.startswith("<") or value["line"] < 1:
            return None
        require("physical_file" in value and "physical_line" in value,"Missing GCC physical source mapping")
        path,line = frozen_path(value["physical_file"]),value["physical_line"]
        asset = locate(str(path)) if path else None
        if not asset:
            return None
        include_paths.add(path)
        if path not in files:
            raw = path.read_bytes()
            starts = [0]
            for chunk in raw.splitlines(keepends=True):
                starts.append(starts[-1]+len(chunk))
            files[path] = starts
        starts = files[path]
        require(1<=line<len(starts), "GCC returned an out-of-range source location: "+name+":"+str(value["line"]))
        result = {"asset":asset,"line":line,"column":value["column"],
                  "offset":starts[line-1] + max(0,value["column"]-1)}
        if name!=value["physical_file"] or line!=value["line"]:
            presumed = frozen_path(name) if Path(name).is_absolute() else frozen_path(str((path.parent/name).resolve()))
            result.update(source_mapping="gcc-line-map",presumed_location={"file":name,"asset":locate(str(presumed)) if presumed and presumed.is_file() else None,
                          "line":value["line"],"column":value["column"]})
        return result

    with output.open(encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            if item["event"] == "include":
                path = Path(item["file"])
                if path.is_file():
                    include_paths.add(path.resolve())
            elif item["event"] == "symbol":
                previous = symbols.get(item["uid"])
                if previous is None or item["definition"]:
                    symbols[item["uid"]] = item
            else:
                calls.append(item)
    include_paths.add(Path(request["file"]).resolve())
    values, identities = {}, {}
    for uid, item in symbols.items():
        pos = position(item["position"])
        if not pos:
            continue
        occurrence = ["gcc-abi/v1", pos["asset"], item["abi"], item["definition"], pos["offset"]]
        if not item["external"]:
            occurrence.append(request["unit_file"])
        logical = identity("symbol", occurrence)
        identities[uid] = logical
        end = position(item.get("end_position",{**item["position"],"line":item["end"]}))
        values[logical] = {"logical":logical,"usr":"gcc-abi:"+item["abi"], "name":item["name"],
            "spelling":item["spelling"], "kind":item["kind"],"asset":pos["asset"], "type":item["type"],
            "start":pos["line"], "end":max(pos["line"],end["line"] if end and end["asset"]==pos["asset"] else pos["line"]), "offset":pos["offset"],
            "linkage":"EXTERNAL" if item["external"] else "INTERNAL", "definition":item["definition"],
            "resolution":"resolved", "frontend_selected":True, "frontend":"gcc-pre-genericize",
            "implicit":item["implicit"], "spelling_location":pos,"expansion_location":pos}
    relations = []
    for call in calls:
        pos = position(call["expansion_location"])
        if not pos or call["owner"] not in identities:
            continue
        target = identities.get(call["target"])
        dispatch = call["dispatch"]
        relations.append({"source":identities[call["owner"]],"target":target or identity("unresolved",[pos["asset"],pos["offset"],call["name"]]),
            "asset":pos["asset"],"start":pos["line"],"end":pos["line"],"offset":pos["offset"],"name":call["name"],
            "kind":"CALLS","resolution":"candidate" if dispatch!="direct" else "resolved" if target else "unresolved",
            "dispatch":dispatch, "implicit":call["implicit"], "frontend":"gcc-pre-genericize",
            "spelling_location":position(call["spelling_location"]),"expansion_location":pos})
    includes = [{"path":str(path),"asset":locate(str(path)),"sha":digest(path.read_bytes())} for path in sorted(include_paths)]
    for diagnostic in diagnostics:
        diagnostic["asset"] = locate(diagnostic.get("file"))
    return {"symbols":list(values.values()),"relations":relations,"includes":includes,"diagnostics":diagnostics,
            "status":"partial" if returncode or any(d["severity"]>=3 for d in diagnostics) else "parsed"}
