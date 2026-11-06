$ErrorActionPreference = "Stop"
$enginePython = Join-Path $PSScriptRoot ".venv/Scripts/python.exe"
if (-not (Test-Path -LiteralPath $enginePython)) { throw "Run install.ps1 with Python 3.12 first." }
& $enginePython -X utf8 "$PSScriptRoot/scripts/unified_kb.py" @args
exit $LASTEXITCODE
