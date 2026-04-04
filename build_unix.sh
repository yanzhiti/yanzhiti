#!/bin/bash
# ============================================================
# 衍智体 (YANZHITI) - Mac/Linux 构建脚本
# Cross-platform Build Script for macOS and Linux
# ============================================================

set -e  # 遇到错误立即退出

echo "========================================"
echo "  衍智体 (YANZHITI) 构建工具 v2.0"
echo "========================================"
echo

# 检测操作系统 | Detect OS
OS_TYPE="$(uname -s)"
case "$OS_TYPE" in
    Darwin*)    PLATFORM="macos";;
    Linux*)     PLATFORM="linux";;
    *)          echo "❌ 不支持的操作系统: $OS_TYPE"; exit 1;;
esac

echo "📌 平台: $PLATFORM"
echo "🐍 Python: $(python3 --version 2>&1 | cut -d' ' -f2)"

# 检查依赖 | Check dependencies
check_dependencies() {
    echo ""
    echo "📦 检查依赖..."
    
    # 检查 Python | Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ 未找到 Python3，请先安装"
        exit 1
    fi
    
    # 检查 PyInstaller | Check PyInstaller
    if ! python3 -m PyInstaller --version &> /dev/null; then
        echo "⬇️ 正在安装 PyInstaller..."
        pip3 install pyinstaller
    fi
    
    echo "✅ 依赖检查完成"
}

# 构建 macOS 版本 | Build macOS version
build_macos() {
    echo ""
    echo "========================================"
    echo "🍎 构建 macOS 应用..."
    echo "========================================"
    
    # 安装项目依赖 | Install project dependencies
    echo "[1/5] 安装项目依赖..."
    pip3 install -e . -q
    
    # 构建 | Build
    echo "[2/5] 执行 PyInstaller 构建..."
    pyinstaller yanzhiti.spec \
        --clean \
        --noconfirm \
        --windowed \
        --icon=assets/icon.icns 2>/dev/null || true
    
    if [ $? -eq 0 ]; then
        echo "[3/5] 创建 .app 包..."
        
        # 创建 .app 结构 | Create .app structure
        APP_DIR="dist/衍智体.app"
        mkdir -p "$APP_DIR/Contents/MacOS"
        mkdir -p "$APP_DIR/Contents/Resources"
        
        # 复制可执行文件 | Copy executable
        cp dist/yanzhiti/衍智体 "$APP_DIR/Contents/MacOS/" 2>/dev/null || \
        cp dist/yanzhiti/yanzhiti "$APP_DIR/Contents/MacOS/"
        
        # 创建 Info.plist | Create Info.plist
        cat > "$APP_DIR/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>yanzhiti</string>
    <key>CFBundleIdentifier</key>
    <string>com.yanzhiti.app</string>
    <key>CFBundleName</key>
    <string>衍智体</string>
    <key>CFBundleDisplayName</key>
    <string>衍智体 YANZHITI</string>
    <key>CFBundleVersion</key>
    <string>2.1.88</string>
    <key>CFBundleShortVersionString</key>
    <string>2.1.88</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>10.13.0</string>
</dict>
</plist>
EOF
        
        echo "[4/5] 创建启动脚本..."
        
        # GUI 启动器 | GUI Launcher
        cat > "dist/衍智体.app/Contents/Resources/launch_gui.sh" << 'EOF'
#!/bin/bash
open http://127.0.0.1:8080
"$0/../MacOS/yanzhiti"
EOF
        chmod +x "dist/衍智体.app/Contents/Resources/launch_gui.sh"
        
        echo "[5/5] ✅ macOS 应用构建成功！"
        echo ""
        echo "📦 输出目录: dist/"
        echo "🚀 运行方式: open dist/衍智体.app"
        
        open dist/
    else
        echo "❌ 构建失败！"
        exit 1
    fi
}

# 构建 Linux 版本 | Build Linux version
build_linux() {
    echo ""
    echo "========================================"
    echo "🐧 构建 Linux 应用..."
    echo "========================================"
    
    # 安装项目依赖 | Install project dependencies
    echo "[1/4] 安装项目依赖..."
    pip3 install -e . -q
    
    # 构建 | Build
    echo "[2/4] 执行 PyInstaller 构建..."
    pyinstaller yanzhiti.spec \
        --clean \
        --noconfirm 2>/dev/null || true
    
    if [ $? -eq 0 ]; then
        echo "[3/4] 创建桌面快捷方式..."
        
        # 创建 Desktop Entry | Create desktop entry
        cat > ~/.local/share/applications/yanzhiti.desktop << EOF
[Desktop Entry]
Name=衍智体 YANZHITI
Comment=AI 编程助手
Exec=sh -c "cd $(pwd)/dist/yanzhiti && ./yanzhiti & sleep 2 && xdg-open http://127.0.0.1:8080"
Icon=$(pwd)/assets/icon.png
Terminal=false
Type=Application
Categories=Development;Utility;
StartupNotify=true
EOF
        
        chmod +x ~/.local/share/applications/yanzhiti.desktop
        
        echo "[4/4] ✅ Linux 应用构建成功！"
        echo ""
        echo "📦 输出目录: dist/yanzhiti/"
        echo "🚀 运行方式: ./dist/yanzhiti/yanzhiti"
        echo "🖥️ 或在应用菜单中搜索'衍智体'"
        
        xdg-open dist/ 2>/dev/null &
    else
        echo "❌ 构建失败！"
        exit 1
    fi
}

# 清理构建文件 | Clean build files
clean_build() {
    echo ""
    echo "🧹 正在清理构建文件..."
    rm -rf build/ dist/ *.spec
    echo "✅ 清理完成！"
}

# 主菜单 | Main menu
show_menu() {
    echo ""
    echo "请选择操作:"
    echo "  [1] 构建 $PLATFORM 可执行文件 (推荐)"
    echo "  [2] 构建单文件版本"
    echo "  [3] 清理构建文件"
    echo "  [4] 运行测试"
    echo "  [0] 退出"
    echo ""
    read -p "请输入选项 (0-4): " choice
    
    case $choice in
        1) 
            check_dependencies
            if [ "$PLATFORM" = "macos" ]; then
                build_macos
            else
                build_linux
            fi
            ;;
        2) 
            check_dependencies
            pyinstaller --onefile \
                --name=yanzhiti \
                src/yanzhiti/cli/gui_launcher.py
            echo "✅ 单文件构建成功: dist/yanzhiti"
            ;;
        3) clean_build ;;
        4) python3 -m pytest tests/ -v ;;
        0) exit 0 ;;
        *) echo "❌ 无效选项"; show_menu ;;
    esac
}

# 如果有参数直接执行 | Execute directly if arguments provided
if [ $# -gt 0 ]; then
    case $1 in
        build)   check_dependencies; build_${PLATFORM} ;;
        clean)   clean_build ;;
        test)    python3 -m pytest tests/ -v ;;
        *)       echo "用法: $0 [build|clean|test]" ;;
    esac
else
    show_menu
fi
