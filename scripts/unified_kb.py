"""Portable entry point for the unified Wiki/source knowledge engine."""
import sys
from unified_knowledge.cli import main
from unified_knowledge import project

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args in (["-h"],["--help"]):
        raise SystemExit(project.main(["--help"]))
    if args == ["--version"]:
        from unified_knowledge import __version__
        print(__version__)
        raise SystemExit(0)
    raise SystemExit(project.main(args) if args[0] in project.COMMANDS else main())
