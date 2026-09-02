@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo ============================================================
echo 数学建模工作区依赖增量更新
echo ============================================================
echo.

:: ============================================================
:: 第一步：确认虚拟环境存在
:: ============================================================
echo [1/4] 检查虚拟环境...

dir ".venv-modeling\Scripts\python.exe" >nul 2>&1
if errorlevel 1 (
    echo [错误] 虚拟环境不存在。
    echo 请先运行 setup.bat 创建虚拟环境。
    pause
    exit /b 1
)

echo 虚拟环境存在。

:: ============================================================
:: 第二步：确认 requirements 文件存在
:: ============================================================
echo [2/4] 检查依赖清单...

dir "config\python\requirements-modeling.txt" >nul 2>&1
if errorlevel 1 (
    echo [错误] config\python\requirements-modeling.txt 不存在。
    pause
    exit /b 1
)

echo 依赖清单存在。

:: ============================================================
:: 第三步：对比并补全缺失的包
:: ============================================================
echo [3/4] 检查缺失的依赖...

:: 获取已安装包列表（只取包名）
.\.venv-modeling\Scripts\python.exe -m pip list --format=freeze > %TEMP%\installed_packages.txt

set MISSING_COUNT=0
set MISSING_LIST=

:: 逐行读取 requirements 中的包名（取第一个 = 前的部分，或整行）
for /f "delims=" %%i in ('type config\python\requirements-modeling.txt') do (
    set "line=%%i"
    :: 跳过空行和注释行
    if not "!line!"=="" (
        echo !line! | findstr /r "^[A-Za-z0-9]" >nul
        if not errorlevel 1 (
            :: 取第一个 = 或 < 或 > 之前的字符作为包名
            for /f "delims=<=>" %%p in ("!line!") do set "pkg=%%p"
            :: 去掉可能的空格
            set "pkg=!pkg: =!"
            if not "!pkg!"=="" (
                findstr /i "!pkg!==" %TEMP%\installed_packages.txt >nul
                if errorlevel 1 (
                    set /a MISSING_COUNT+=1
                    set "MISSING_LIST=!MISSING_LIST! !pkg!"
                )
            )
        )
    )
)

if !MISSING_COUNT!==0 (
    echo 所有依赖已安装，无需更新。
    goto :skip_install
)

echo 发现 !MISSING_COUNT! 个缺失的依赖包：!MISSING_LIST!
echo.

:: ============================================================
:: 第四步：安装缺失包
:: ============================================================
echo [4/4] 安装缺失的依赖...

.\.venv-modeling\Scripts\python.exe -m pip install -r config\python\requirements-modeling.txt
if errorlevel 1 (
    echo [错误] 部分依赖安装失败，请查看上方日志。
    pause
    exit /b 1
)

echo 依赖安装完成。

:: 运行环境检查
echo.
echo 运行环境检查...
dir "tools\check-modeling-env.py" >nul 2>&1
if not errorlevel 1 (
    .\.venv-modeling\Scripts\python.exe tools\check-modeling-env.py
    if errorlevel 1 (
        echo [警告] 环境检查存在部分问题，请查看上方输出。
    ) else (
        echo 环境检查全部通过。
    )
) else (
    echo [警告] tools\check-modeling-env.py 不存在，跳过环境检查。
)

:skip_install
echo.
echo ============================================================
echo 更新完成
echo ============================================================
echo.
echo 虚拟环境: .\.venv-modeling\Scripts\python.exe
echo.
pause