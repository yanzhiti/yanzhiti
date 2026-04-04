# 📦 打包发布指南 | Packaging & Release Guide

> 如何将衍智体打包为各平台可执行文件
> How to package YANZHITI as executables for all platforms

---

## 🎯 概述 | Overview

本指南介绍如何将衍智体打包为:
- Windows: `.exe` 安装包
- macOS: `.dmg` 安装包  
- Linux: `.deb` / `.rpm` 安装包

---

## 📋 准备工作 | Prerequisites

### 安装打包工具 | Install Packaging Tools

```bash
# 安装开发依赖 (包含 PyInstaller)
pip install -e ".[dev]"

# 或单独安装
pip install pyinstaller>=6.0
```

### 准备图标文件 | Prepare Icon Files

```bash
assets/
  ├── icon.ico      # Windows 图标 (256x256)
  ├── icon.icns     # macOS 图标
  └── icon.png      # Linux 图标 (256x256)
```

---

## 🪟 Windows 打包 | Windows Packaging

### 方法 1: 使用 PyInstaller

```bash
# 1. 进入项目目录
cd e:\Git\yanzhiti

# 2. 运行 PyInstaller
pyinstaller --name=YANZHITI ^
            --onefile ^
            --icon=assets/icon.ico ^
            --add-data "src/yanzhiti;yanzhiti" ^
            --hidden-import=anthropic ^
            --hidden-import=pydantic ^
            --hidden-import=rich ^
            src/yanzhiti/cli/main.py

# 3. 测试可执行文件
.\dist\YANZHITI.exe --version
```

### 方法 2: 使用 Inno Setup 创建安装包

1. **下载并安装 Inno Setup**
   - 网址：https://jrsoftware.org/isdl.php

2. **创建安装脚本 `installer.iss`**

```iss
[Setup]
AppName=YANZHITI
AppVersion=1.0.0
AppPublisher=YANZHITI Team
DefaultDirName={autopf}\YANZHITI
DefaultGroupName=YANZHITI
OutputDir=installer
OutputBaseFilename=yanzhiti-setup

[Files]
Source: "dist\YANZHITI.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\YANZHITI"; Filename: "{app}\YANZHITI.exe"
Name: "{commondesktop}\YANZHITI"; Filename: "{app}\YANZHITI.exe"

[Run]
Filename: "{app}\YANZHITI.exe"; Description: "启动 YANZHITI"; Flags: postinstall skipifsilent
```

3. **编译安装包**
   ```bash
   iscc installer.iss
   ```

---

## 🍎 macOS 打包 | macOS Packaging

### 使用 PyInstaller + create-dmg

```bash
# 1. 打包为 .app
pyinstaller --name=YANZHITI \
            --onefile \
            --icon=assets/icon.icns \
            --osx-bundle-identifier=com.yanzhiti.cli \
            src/yanzhiti/cli/main.py

# 2. 安装 create-dmg
brew install create-dmg

# 3. 创建 DMG
create-dmg \
  --volname "YANZHITI Installer" \
  --volicon "assets/icon.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --app-drop-link 400 200 \
  --hide-extension "YANZHITI.app" \
  installer/yanzhiti.dmg \
  dist/YANZHITI.app
```

---

## 🐧 Linux 打包 | Linux Packaging

### 创建 DEB 包 (Debian/Ubuntu)

```bash
# 1. 创建目录结构
mkdir -p yanzhiti_amd64/DEBIAN
mkdir -p yanzhiti_amd64/usr/bin
mkdir -p yanzhiti_amd64/usr/share/applications

# 2. 复制文件
cp dist/YANZHITI yanzhiti_amd64/usr/bin/yanzhiti

# 3. 创建控制文件
cat > yanzhiti_amd64/DEBIAN/control << EOF
Package: yanzhiti
Version: 1.0.0
Section: utils
Priority: optional
Architecture: amd64
Depends: python3
Maintainer: YANZHITI Team
Description: AI-Powered Intelligent Code Assistant
 YANZHITI is an open-source AI coding assistant.
EOF

# 4. 创建桌面文件
cat > yanzhiti_amd64/usr/share/applications/yanzhiti.desktop << EOF
[Desktop Entry]
Name=YANZHITI
Comment=AI Coding Assistant
Exec=/usr/bin/yanzhiti
Icon=yanzhiti
Type=Application
Categories=Development;Utility;
EOF

# 5. 构建 DEB 包
dpkg-deb --build yanzhiti_amd64 yanzhiti_1.0.0_amd64.deb
```

### 创建 RPM 包 (Fedora/RHEL)

```bash
# 安装 rpm-build
sudo dnf install rpm-build

# 创建 spec 文件
cat > yanzhiti.spec << EOF
Name: yanzhiti
Version: 1.0.0
Release: 1%{?dist}
Summary: AI-Powered Intelligent Code Assistant
License: MIT
BuildArch: x86_64

%description
YANZHITI is an open-source AI coding assistant.

%install
mkdir -p %{buildroot}/usr/bin
cp dist/YANZHITI %{buildroot}/usr/bin/yanzhiti

%files
/usr/bin/yanzhiti
EOF

# 构建 RPM
rpmbuild -bb yanzhiti.spec
```

---

## 🔄 自动化构建脚本 | Automated Build Scripts

### Windows PowerShell 脚本

```powershell
# build-windows.ps1

Write-Host "Building YANZHITI for Windows..." -ForegroundColor Cyan

# 清理
Remove-Item -Path "dist", "build" -Recurse -Force -ErrorAction SilentlyContinue

# 打包
pyinstaller --name=YANZHITI `
            --onefile `
            --icon=assets/icon.ico `
            --add-data "src/yanzhiti;yanzhiti" `
            --hidden-import=anthropic `
            --hidden-import=pydantic `
            src/yanzhiti/cli/main.py

# 测试
Write-Host "Testing executable..." -ForegroundColor Green
.\dist\YANZHITI.exe --version

Write-Host "Build completed!" -ForegroundColor Green
```

### macOS/Linux Bash 脚本

```bash
#!/bin/bash
# build.sh

echo "Building YANZHITI..."

# 清理
rm -rf dist build

# 打包
pyinstaller --name=YANZHITI \
            --onefile \
            --icon=assets/icon.png \
            --add-data "src/yanzhiti:yanzhiti" \
            --hidden-import=anthropic \
            --hidden-import=pydantic \
            src/yanzhiti/cli/main.py

# 测试
echo "Testing executable..."
./dist/YANZHITI --version

echo "Build completed!"
```

---

## 📤 发布到 GitHub Releases | Publish to GitHub Releases

### 使用 GitHub CLI

```bash
# 1. 创建新版本
gh release create v1.0.0 \
  --title "YANZHITI v1.0.0" \
  --notes "Initial release" \
  --draft

# 2. 上传构建文件
gh release upload v1.0.0 \
  dist/YANZHITI.exe \
  installer/yanzhiti-setup.exe \
  installer/yanzhiti.dmg \
  yanzhiti_1.0.0_amd64.deb \
  yanzhiti_1.0.0.x86_64.rpm
```

### 使用 GitHub Actions 自动发布

创建 `.github/workflows/release.yml`:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Build EXE
        run: |
          pyinstaller --name=YANZHITI --onefile src/yanzhiti/cli/main.py
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: windows-exe
          path: dist/YANZHITI.exe

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          brew install create-dmg
      
      - name: Build DMG
        run: |
          pyinstaller --name=YANZHITI --onefile src/yanzhiti/cli/main.py
          create-dmg --volname "YANZHITI" installer/yanzhiti.dmg dist/YANZHITI.app
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: macos-dmg
          path: installer/yanzhiti.dmg

  release:
    needs: [build-windows, build-macos]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/download-artifact@v3
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            windows-exe/YANZHITI.exe
            macos-dmg/yanzhiti.dmg
```

---

## ✅ 测试清单 | Testing Checklist

打包完成后，请测试:

- [ ] 可执行文件能正常启动
- [ ] 版本号显示正确
- [ ] 配置向导能正常运行
- [ ] 诊断工具能正常检测
- [ ] 交互式模式正常工作
- [ ] 文件操作工具正常
- [ ] 无依赖缺失错误
- [ ] 安装包大小合理 (<100MB)

---

## 📊 文件大小优化 | File Size Optimization

### 减小可执行文件大小

1. **使用 UPX 压缩**
   ```bash
   pyinstaller --upx-dir=upx ...
   ```

2. **排除不必要的模块**
   ```python
   # 在 spec 文件中添加
   excludes=['matplotlib', 'numpy', 'scipy']
   ```

3. **使用 Nuitka 编译**
   ```bash
   python -m nuitka --onefile src/yanzhiti/cli/main.py
   ```

---

## 🆘 常见问题 | FAQ

### Q: 打包后运行报错 "ModuleNotFoundError"
**A:** 添加 `--hidden-import` 选项:
```bash
pyinstaller --hidden-import=module_name ...
```

### Q: 打包文件太大
**A:** 
- 使用 UPX 压缩
- 排除不必要的模块
- 使用 `--onefile` 模式

### Q: 如何包含数据文件
**A:** 使用 `--add-data` 选项:
```bash
# Windows
pyinstaller --add-data "config;config" ...

# macOS/Linux
pyinstaller --add-data "config:config" ...
```

---

## 📚 参考资源 | Resources

- [PyInstaller 官方文档](https://pyinstaller.org/en/stable/)
- [Inno Setup](https://jrsoftware.org/isinfo.php)
- [create-dmg](https://github.com/create-dmg/create-dmg)
- [GitHub Actions](https://docs.github.com/en/actions)

---

<div align="center">

**衍智体 (YANZHITI)** - 让 AI 助力您的编程之旅

[开始打包](#-windows-打包--windows-packaging) | [查看文档](README.md) | [报告问题](https://github.com/yanzhiti/yanzhiti/issues)

</div>
