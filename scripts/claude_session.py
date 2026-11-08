"""Entry used by the current assistant; bootstraps Python, never starts a model."""
from pathlib import Path
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]


def main():
    # Tool transports consume UTF-8 even when a Windows console uses a legacy code page.
    for stream in (sys.stdin,sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    target=ROOT/'.venv'
    env={**os.environ,'PYTHONIOENCODING':'utf-8','PYTHONUTF8':'1'}
    if Path(sys.prefix).resolve()!=target.resolve():
        python=target/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
        if not python.is_file():
            # Redirect the installer *process*, including pip's inherited stdout.
            # The calling assistant must see exactly one JSON response on stdout.
            subprocess.run([sys.executable,'-X','utf8',str(ROOT/'scripts/bootstrap_internal.py'),
                            '--root',str(ROOT),'--venv',str(target)],stdout=sys.stderr,env=env,check=True)
        return subprocess.run([str(python),'-X','utf8',str(Path(__file__).resolve()),*sys.argv[1:]],cwd=ROOT,env=env).returncode
    from unified_knowledge.assistant_session import main as session_main
    return session_main(sys.argv[1:])


if __name__=='__main__':raise SystemExit(main())
