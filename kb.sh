#!/bin/sh
set -eu
bundle_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ ! -x "$bundle_root/.venv/bin/python" ] || [ ! -f "$bundle_root/local/install-report.json" ]; then
    py=${PYTHON:-python3.12}
    "$py" -X utf8 "$bundle_root/scripts/bootstrap_internal.py" --root "$bundle_root" >&2
fi
exec "$bundle_root/.venv/bin/python" -X utf8 "$bundle_root/scripts/unified_kb.py" "$@"
