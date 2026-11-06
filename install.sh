#!/bin/sh
set -eu
bundle_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec "${PYTHON:-python3}" -X utf8 "$bundle_root/scripts/bootstrap_internal.py" --root "$bundle_root" --venv "$bundle_root/.venv"
