@echo off
REM ============================================================
REM 衍智体 (YANZHITI) - 跨平台构建脚本
REM Cross-platform Build Script for Windows
REM ============================================================

echo.
echo ========================================
echo   衍智体 (YANZHITI) 构建工具 v2.0
echo ========================================
echo.

REM 检查 Python 版本 | Check Python version
python --version
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

REM 检查 PyInstaller | Check PyInstaller
python -m PyInstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [信息] 正在安装 PyInstaller...
    pip install pyinstaller
)

echo.
echo 请选择构建选项 | Please select build option:
echo   [1] 构建 Windows 可执行文件 (推荐)
echo   [2] 构建单文件可执行文件
echo   [3] 清理构建文件
echo   [4] 运行测试
echo   [0] 退出
echo.

set /p choice=请输入选项 (0-4):

if "%choice%"=="1" goto build_dir
if "%choice%"=="2" goto build_onefile
if "%choice%"=="3" goto clean
if "%choice%"=="4" goto test
if "%choice%"=="0" goto end

:build_dir
echo.
echo ========================================
echo 正在构建 Windows 目录版本...
echo Building Windows directory version...
echo ========================================

REM 安装依赖 | Install dependencies
echo.
echo [1/5] 安装项目依赖...
pip install -e . >nul 2>&1

REM 构建 | Build
echo [2/5] 执行 PyInstaller 构建...
pyinstaller yanzhiti.spec --clean --noconfirm

if %errorlevel% equ 0 (
    echo [3/5] 构建成功！
    
    REM 创建启动脚本 | Create launcher scripts
    echo [4/5] 创建启动脚本...
    
    REM GUI 启动器 | GUI Launcher
    echo @echo off > dist\yanzhiti\启动Web界面.bat
    echo start http://127.0.0.1:8080 >> dist\yanzhiti\启动Web界面.bat
    echo yanzhiti.exe >> dist\yanzhiti\启动Web界面.bat
    
    REM CLI 启动器 | CLI Launcher
    echo @echo off > dist\yanzhiti\启动命令行.bat
    echo yanzhiti.exe %%* >> dist\yanzhiti\启动命令行.bat
    
    echo [5/5] 完成！
    echo.
    echo ✅ 构建成功！输出目录: dist\yanzhiti\
    echo.
    echo 📦 包含文件:
    dir /b dist\yanzhiti\*.exe
    echo.
    explorer dist\yanzhiti
) else (
    echo ❌ 构建失败！请检查错误信息。
)
goto end

:build_onefile
echo.
echo ========================================
echo 正在构建单文件版本...
echo Building single-file version...
echo ========================================

pyinstaller --onefile ^
    --name=yanzhiti ^
    --windowed ^
    --icon=assets/icon.ico ^
    --add-data "src/yanzhiti/web/static;yanzhiti/web/static" ^
    --add-data "examples;examples" ^
    --hidden-import=fastapi ^
    --hidden-import=uvicorn ^
    src/yanzhiti/cli/gui_launcher.py

if %errorlevel% equ 0 (
    echo ✅ 单文件构建成功！输出文件: dist\yanzhiti.exe
    explorer dist
) else (
    echo ❌ 构建失败！
)
goto end

:clean
echo.
echo 正在清理构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec
echo ✅ 清理完成！
goto end

:test
echo.
echo 正在运行测试...
python -m pytest tests/ -v
goto end

:end
echo.
pause
