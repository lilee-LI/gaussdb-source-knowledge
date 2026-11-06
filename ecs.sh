#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python=${PYTHON:-python3}
case "${1:-}" in
    ""|-h|--help|capture) exec "$python" "$root/scripts/ecs_producer.py" "$@" ;;
esac
"$python" "$root/scripts/bootstrap_ecs.py" "$root" >&2
exec "$root/.venv-ecs/bin/python" "$root/scripts/ecs_producer.py" "$@"
