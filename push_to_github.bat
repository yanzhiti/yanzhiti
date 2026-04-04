@echo off
echo ========================================
echo GitHub 推送脚本 (带加速优化)
echo ========================================
echo.

REM 设置 Git 优化参数
git config --global http.postBuffer 524288000
git config --global https.postBuffer 524288000
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999
git config --global http.sslVerify false

echo [1/3] Git 配置已优化
echo.

REM 设置环境变量
set GIT_HTTP_LOW_SPEED_LIMIT=0
set GIT_HTTP_LOW_SPEED_TIME=999999

echo [2/3] 环境变量已设置
echo.

echo [3/3] 开始推送到 GitHub...
echo 可能需要 1-3 分钟，请耐心等待...
echo.

git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ 推送成功!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ❌ 推送失败，请检查网络连接
    echo ========================================
    echo.
    echo 建议:
    echo 1. 使用手机热点试试
    echo 2. 稍后再试
    echo 3. 使用代理服务器
)

pause
