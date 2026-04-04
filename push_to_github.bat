@echo off
REM 衍智体项目推送脚本
REM Push Script for YANZHITI Project

echo ========================================
echo 衍智体 (YANZHITI) 项目推送脚本
echo ========================================
echo.

echo 正在检查 Git 状态...
git status

echo.
echo ========================================
echo 待推送的提交列表:
echo ========================================
git log --oneline origin/main..main

echo.
echo ========================================
echo 开始推送到 GitHub...
echo ========================================
echo.

REM 尝试推送
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ 推送成功!
    echo ========================================
    echo.
    echo 请检查 GitHub 页面:
    echo https://github.com/yanzhiti/yanzhiti
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ 推送失败!
    echo ========================================
    echo.
    echo 可能的原因:
    echo 1. 网络连接问题
    echo 2. GitHub 服务器问题
    echo 3. 权限问题
    echo.
    echo 建议操作:
    echo 1. 检查网络连接
    echo 2. 稍后重试
    echo 3. 或使用 GitHub Desktop 推送
    echo.
)

pause
