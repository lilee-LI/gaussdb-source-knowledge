"""Install the internal bundle using its pinned platform wheels, entirely offline."""
import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import venv

from verify_unified_bundle import verify


def platform_key():
    if sys.version_info[:2] != (3,12):
        raise ValueError("This offline bundle requires CPython 3.12; provide Python 3.12 on the target host")
    machine=platform.machine().lower()
    arch="x64" if machine in {"x86_64","amd64"} else "arm64" if machine in {"aarch64","arm64"} else machine
    system="windows" if os.name=="nt" else "linux" if sys.platform.startswith("linux") else sys.platform
    return system+"-"+arch+"-py312"


def install(root, target):
    root,target=Path(root).resolve(),Path(target).resolve()
    if root==target or root.is_relative_to(target):raise ValueError("Venv must not overlap the engine directory")
    check=verify(root,allow_local_runtime=True)
    key=platform_key()
    ecs = (root/"ECS-EDITION").is_file()
    if ecs and key not in {"windows-x64-py312","linux-x64-py312","linux-arm64-py312"}:
        raise ValueError("Unsupported target platform: "+key)
    wheels=root/"wheels"/("common-py312" if ecs else key)
    lock=wheels/"requirements.lock"
    if not lock.is_file():raise ValueError("No offline wheels for "+key)
    if not shutil.which("git"):raise ValueError("Provide Git on PATH; external runtimes are not bundled")
    venv.EnvBuilder(with_pip=True,system_site_packages=False).create(target)
    python=target/("Scripts/python.exe" if os.name=="nt" else "bin/python")
    env=dict(os.environ,PYTHONNOUSERSITE="1",PYTHONDONTWRITEBYTECODE="1")
    env.pop("PYTHONPATH",None);env.pop("PYTHONHOME",None)
    command=[str(python),"-X","utf8","-m","pip","install","--disable-pip-version-check","--no-index",
             "--require-hashes","--only-binary=:all:","--find-links",str(wheels),"-r",str(lock)]
    subprocess.run(command,check=True,env=env)
    subprocess.run([str(python),"-m","pip","check","--disable-pip-version-check"],check=True,env=env)
    report={"result":"installed","platform":key,"python":str(python),"engine_manifest":check["manifest_sha256"],
            "wheel_set":wheels.name,"package_index_used":False,"external_agent_bundled":False}
    (root/"local").mkdir(exist_ok=True)
    (root/"local/install-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--root",type=Path,required=True);p.add_argument("--venv",type=Path)
    a=p.parse_args();print(json.dumps(install(a.root,a.venv or a.root/".venv"),ensure_ascii=False,indent=2))
