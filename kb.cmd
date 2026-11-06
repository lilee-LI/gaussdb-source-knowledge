@echo off
setlocal
set "KBROOT=%~dp0"
set "KBPY=%~dp0.venv\Scripts\python.exe"
if not exist "%KBPY%" goto bootstrap
if exist "%KBROOT%local\install-report.json" goto run
:bootstrap
where py >nul 2>&1
if errorlevel 1 goto usepython
py -3.12 -c "import sys" >nul 2>&1
if errorlevel 1 goto usepython
py -3.12 -X utf8 "%KBROOT%scripts\bootstrap_internal.py" --root "%KBROOT%." 1>&2
if errorlevel 1 exit /b 1
goto run
:usepython
python -X utf8 "%KBROOT%scripts\bootstrap_internal.py" --root "%KBROOT%." 1>&2
if errorlevel 1 exit /b 1
:run
"%KBPY%" -X utf8 "%KBROOT%scripts\unified_kb.py" %*
exit /b %errorlevel%
