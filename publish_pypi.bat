@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

:: ============================================================
:: 衍智体 (YANZHITI) - PyPI 发布脚本
:: PyPI Publishing Script
:: ============================================================
:: 用法 | Usage:
::   publish_pypi.bat          - 发布到 TestPyPI (测试)
::   publish_pypi.bat prod    - 发布到正式 PyPI
::   publish_pypi.bat build   - 仅构建，不发布
:: ============================================================

echo.
echo ╔══════════════════════════════════════════════════╗
echo ║     🤖 衍智体 (YANZHITI) PyPI 发布工具       ║
echo ╚══════════════════════════════════════════════════╝
echo.

:: 检查 Python 环境 | Check Python environment
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

:: 清理旧的构建产物 | Clean old builds
echo 🧹 清理旧构建产物...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.egg-info rmdir /s /q *.egg-info 2>nul
echo ✅ 清理完成
echo.

:: 构建包 | Build packages
echo 📦 正在构建 sdist 和 wheel...
python -m build
if errorlevel 1 (
    echo ❌ 构建失败！请检查上面的错误信息
    pause
    exit /b 1
)
echo ✅ 构建完成！
echo.

:: 显示构建结果 | Show build results
echo 📋 构建产物:
for %%f in (dist\*) do echo    %%f
echo.

:: 根据参数决定操作 | Decide action based on parameter
if "%1"=="build" (
    echo ✅ 仅构建模式，跳过发布。
    echo    要发布请运行: publish_pypi.bat [prod]
    goto :end
)

if "%1"=="prod" (
    echo 🚀 发布到正式 PyPI...
    echo ⚠️  这将发布到 https://pypi.org/p/yanzhiti/
    echo.
    set /p confirm=确认发布？(y/N): 
    if not "!confirm!"=="y" if not "!confirm!"=="Y" (
        echo 已取消
        goto :end
    )
    python -m twine upload dist/*
    if errorlevel 1 (
        echo ❌ 发布到 PyPI 失败！
        pause
        exit /b 1
    )
    echo.
    echo ✅ 成功发布到 PyPI！
    echo    用户可通过 pip install yanzhiti 安装
) else (
    echo 🧪 发布到 TestPyPI (测试环境)...
    python -m twine upload --repository testpypi dist/*
    if errorlevel 1 (
        echo ❌ 发布到 TestPyPI 失败！
        echo    提示: 需要在 ~/.pypirc 中配置 TestPyPI 凭据
        pause
        exit /b 1
    )
    echo.
    echo ✅ 成功发布到 TestPyPI！
    echo    测试安装: pip install --index-url https://test.pypi.org/simple/ yanzhiti
)

:end
echo.
pause
