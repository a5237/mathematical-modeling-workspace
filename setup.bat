@echo off
setlocal enabledelayedexpansion

:: 切换到脚本所在目录（即项目根目录）
cd /d "%~dp0"

echo [1/7] Searching for compatible Python version (3.10, 3.11, 3.12, 3.13)...

set PY_CMD=
for %%v in (3.13 3.12 3.11 3.10) do (
    py -%%v -c "import sys; print(sys.version.split()[0])" >nul 2>&1
    if not errorlevel 1 (
        set PY_CMD=py -%%v
        for /f "delims=" %%i in ('py -%%v -c "import sys; print(sys.version.split()[0])"') do set PY_VER=%%i
        echo Found Python !PY_VER!
        goto :pyfound
    )
)

:: 回退到默认 py
py -c "print(1)" >nul 2>&1
if not errorlevel 1 (
    set PY_CMD=py
    for /f "delims=" %%i in ('py -c "import sys; print(sys.version.split()[0])"') do set PY_VER=%%i
    echo Found default Python !PY_VER! via py launcher.
    goto :check_version
)

:: 回退到 PATH 中的 python
python -c "print(1)" >nul 2>&1
if not errorlevel 1 (
    set PY_CMD=python
    for /f "delims=" %%i in ('python -c "import sys; print(sys.version.split()[0])"') do set PY_VER=%%i
    echo Found default Python !PY_VER! via PATH.
    goto :check_version
)

echo ERROR: No Python found. Please install Python 3.10 to 3.13.
pause
exit /b 1

:check_version
echo !PY_VER! | findstr /r "^3\.1[4-9] ^3\.[2-9][0-9]" >nul
if not errorlevel 1 (
    echo ERROR: Python !PY_VER! is not supported.
    echo This project requires Python 3.10, 3.11, 3.12, or 3.13.
    echo.
    echo Please install one of the following:
    echo   - Python 3.12.10: https://www.python.org/downloads/release/python-31210/
    echo   - Python 3.11.x: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:pyfound
echo Using Python version: !PY_VER!

echo [2/7] Removing old virtual environment (if exists)...
if exist ".venv-modeling" (
    rmdir /s /q ".venv-modeling"
    if errorlevel 1 (
        echo ERROR: Failed to remove old .venv-modeling directory.
        echo Please close any programs using files in this directory and try again.
        pause
        exit /b 1
    )
)

echo [3/7] Creating new virtual environment...
%PY_CMD% -m venv .venv-modeling
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

echo [4/7] Installing dependencies from requirements-modeling.txt...
if not exist "requirements-modeling.txt" (
    echo ERROR: requirements-modeling.txt not found in project root.
    pause
    exit /b 1
)

.\.venv-modeling\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: Pip upgrade failed, continuing with existing pip.
)

.\.venv-modeling\Scripts\python.exe -m pip install -r requirements-modeling.txt
if errorlevel 1 (
    echo ERROR: Failed to install some dependencies.
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo [5/7] Running pip check...
.\.venv-modeling\Scripts\python.exe -m pip check
if errorlevel 1 (
    echo WARNING: Some dependencies have conflicts.
    echo Please check the output above and resolve manually.
    pause
)

echo [6/7] Running environment check script...
if not exist "shared-tools\check-modeling-env.py" (
    echo ERROR: shared-tools\check-modeling-env.py not found.
    echo Please ensure the file exists in the project root.
    pause
    exit /b 1
)

.\.venv-modeling\Scripts\python.exe shared-tools\check-modeling-env.py
if errorlevel 1 (
    echo WARNING: Environment check reported issues.
    echo See output above for details.
    pause
) else (
    echo SUCCESS: All checks passed.
)

echo [7/7] Recording environment fingerprint...
.\.venv-modeling\Scripts\python.exe -c "import sys, json; print(json.dumps({'python_version': sys.version.split()[0]}))" > tmp\env_fingerprint.json 2>nul
if not errorlevel 1 (
    echo Environment fingerprint saved to tmp\env_fingerprint.json
)

echo.
echo Virtual environment setup completed.
echo Using Python version: !PY_VER!
echo To use it, run: .\.venv-modeling\Scripts\python.exe your_script.py
echo.

pause