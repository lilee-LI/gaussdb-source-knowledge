param([string]$Python = "python")
$ErrorActionPreference = "Stop"
& $Python -X utf8 "$PSScriptRoot/scripts/bootstrap_internal.py" --root $PSScriptRoot --venv "$PSScriptRoot/.venv"
exit $LASTEXITCODE
