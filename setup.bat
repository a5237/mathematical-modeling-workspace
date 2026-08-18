@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo ============================================================
echo 数学建模工作区环境搭建
echo ============================================================
echo.

:: ============================================================
:: 第一步：检测 Python 环境
:: ============================================================
echo [1/6] 检测 Python 环境...

set PY_CMD=
for %%v in (3.13 3.12 3.11 3.10) do (
    py -%%v -c "import sys; print(sys.version.split()[0])" >nul 2>&1
    if not errorlevel 1 (
        set PY_CMD=py -%%v
        for /f "delims=" %%i in ('py -%%v -c "import sys; print(sys.version.split()[0])"') do set PY_VER=%%i
        echo 找到 Python !PY_VER!
        goto :pyfound
    )
)

:: 回退检测
py -c "print(1)" >nul 2>&1
if not errorlevel 1 (
    set PY_CMD=py
    for /f "delims=" %%i in ('py -c "import sys; print(sys.version.split()[0])"') do set PY_VER=%%i
    echo 找到默认 Python !PY_VER!
    goto :check_version
)

python -c "print(1)" >nul 2>&1
if not errorlevel 1 (
    set PY_CMD=python
    for /f "delims=" %%i in ('python -c "import sys; print(sys.version.split()[0])"') do set PY_VER=%%i
    echo 找到系统 Python !PY_VER!
    goto :check_version
)

echo [错误] 未找到 Python。
echo 请安装 Python 3.10 ~ 3.13，并确保 py 启动器可用。
pause
exit /b 1

:check_version
echo !PY_VER! | findstr /r "^3\.1[4-9] ^3\.[2-9][0-9]" >nul
if not errorlevel 1 (
    echo [错误] Python !PY_VER! 不被支持。
    echo 本项目需要 Python 3.10、3.11、3.12 或 3.13。
    echo 请安装受支持的版本后重试。
    pause
    exit /b 1
)

:pyfound
echo 使用 Python 版本: !PY_VER!
echo.

:: ============================================================
:: 第二步：检查虚拟环境状态
:: ============================================================
echo [2/6] 检查虚拟环境状态...

set VENV_EXISTS=0
if exist ".venv-modeling\Scripts\python.exe" set VENV_EXISTS=1

if !VENV_EXISTS!==1 (
    echo 虚拟环境已存在。
    .\.venv-modeling\Scripts\python.exe -c "import numpy, scipy, pandas, matplotlib" >nul 2>&1
    if errorlevel 1 (
        echo [警告] 虚拟环境存在但核心依赖缺失，需要重建。
        set NEED_REBUILD=1
    ) else (
        echo 虚拟环境完整，核心依赖可用。
        set NEED_REBUILD=0
    )
) else (
    echo 虚拟环境不存在，需要创建。
    set NEED_REBUILD=1
)

if !NEED_REBUILD!==1 (
    echo.
    echo 是否重建虚拟环境？
    echo   y - 删除旧环境并重新创建
    echo   n - 跳过（仅检测环境）
    set /p CHOICE="请输入 y 或 n [y]: "
    if "!CHOICE!"=="" set CHOICE=y
    if /i not "!CHOICE!"=="y" (
        echo 跳过虚拟环境重建。
        goto :skip_venv
    )
    
    echo.
    echo [3/6] 重建虚拟环境...
    if exist ".venv-modeling" (
        echo 删除旧环境...
        rmdir /s /q ".venv-modeling"
        if errorlevel 1 (
            echo [错误] 无法删除 .venv-modeling 目录。
            echo 请关闭占用该目录的程序后重试。
            pause
            exit /b 1
        )
    )
    
    echo 创建新虚拟环境...
    %PY_CMD% -m venv .venv-modeling
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败。
        pause
        exit /b 1
    )
    
    echo.
    echo [4/6] 安装依赖...
    if not exist "requirements-modeling.txt" (
        echo [错误] requirements-modeling.txt 不存在。
        pause
        exit /b 1
    )
    
    .\.venv-modeling\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1
    .\.venv-modeling\Scripts\python.exe -m pip install -r requirements-modeling.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败，请检查上方错误信息。
        pause
        exit /b 1
    )
    
    echo.
    echo [5/6] 运行环境检查...
    .\.venv-modeling\Scripts\python.exe shared-tools\check-modeling-env.py
    if errorlevel 1 (
        echo [警告] 环境检查存在部分问题，请查看上方输出。
    ) else (
        echo 环境检查全部通过。
    )
) else (
    echo.
    echo 跳过虚拟环境重建，使用现有环境。
)

:skip_venv
echo.

:: ============================================================
:: 第六步：检测 LaTeX 环境
:: ============================================================
echo [6/6] 检测 LaTeX 环境...

where xelatex >nul 2>&1
if errorlevel 1 (
    echo [提示] 未找到 xelatex。
    echo.
    echo 论文编译需要 LaTeX 环境。你已安装 LaTeX 了吗？
    echo   y - 已安装但 xelatex 不在 PATH 中（跳过检测）
    echo   n - 未安装，需要安装 LaTeX
    set /p LATEX_CHOICE="请输入 y 或 n [n]: "
    if "!LATEX_CHOICE!"=="" set LATEX_CHOICE=n
    if /i "!LATEX_CHOICE!"=="y" (
        echo 已跳过 LaTeX 检测（使用非标准 PATH 安装）。
    ) else (
        echo.
        echo 请自行安装 LaTeX 环境：
        echo   - Windows: 安装 MikTeX 或 TeX Live
        echo   - 安装后确保 xelatex 在 PATH 中
        echo.
        echo [警告] LaTeX 未配置，将无法编译 PDF 论文。
        echo 你可以稍后安装 LaTeX，然后重新运行本脚本检测。
    )
) else (
    for /f "delims=" %%i in ('xelatex --version ^| findstr /i "version"') do set XELATEX_VER=%%i
    echo 找到 xelatex: !XELATEX_VER!
    echo LaTeX 环境可用。
)

echo.
echo ============================================================
echo 环境搭建完成
echo ============================================================
echo.
echo 虚拟环境: .\.venv-modeling\Scripts\python.exe
echo.
echo 常用命令：
echo   环境检查: .\.venv-modeling\Scripts\python.exe shared-tools\check-modeling-env.py
echo   运行模型: .\.venv-modeling\Scripts\python.exe projects\...\03-models\q00-run-all.py
echo.
pause