# 衍智体 (YANZHITI) 快速上手指南

> 本指南面向**完全没有编程经验的新手**，手把手教你在 Windows、Mac 或 Linux 电脑上安装和使用衍智体。

---

## 📋 目录

1. [什么是衍智体？](#1-什么是衍智体)
2. [第一步：安装 Python](#2-第一步安装-python)（如果电脑上没有 Python）
3. [第二步：安装衍智体](#3-第二步安装-衍智体)
4. [第三步：启动衍智体](#4-第三步启动-衍智体)
5. [首次配置 AI](#5-首次配置-ai)
6. [常见问题与解决方法](#6-常见问题与解决方法)
7. [完全卸载指南](#7-完全卸载指南)

---

## 1. 什么是衍智体？

衍智体是一个**免费的 AI 编程助手**，可以帮你：

- 🤖 用自然语言问问题，自动生成代码
- 🐛 帮你找出代码中的 bug
- 📝 解释一段代码是做什么的
- 🔧 自动执行文件操作、Git 操作等

**完全免费，开源**，不需要支付任何费用。

---

## 2. 第一步：安装 Python

衍智体基于 Python 开发，运行它需要先安装 Python。

### 2.1 检查电脑是否已安装 Python

**Windows：**
1. 按 `Win + X`，选择 **Windows PowerShell**（或 **终端**）
2. 输入：

```powershell
python --version
```

**Mac：**
1. 打开 **终端**（按 `Command + 空格`，搜索"终端"）
2. 输入：

```bash
python3 --version
```

**Linux：**
1. 打开**终端**
2. 输入：

```bash
python3 --version
```

**如果显示类似 `Python 3.11.5`，说明已经安装了 Python。**

**如果显示"找不到命令"，说明没有安装，继续下一步。**

---

### 2.2 Windows：下载并安装 Python

1. 打开浏览器，访问：https://www.python.org/downloads/
2. 点击 **Download Python 3.12.x**（或 3.11.x）

> ⚠️ **注意**：请选择 **3.10、3.11 或 3.12** 版本，**不要**选择 3.9 或更低版本。

**安装界面设置（关键步骤）：**

```
✅ 一定要勾选：Add Python to PATH   ← 这个非常重要！！！

如果不勾选，后续命令无法使用！！！
```

3. 点击 **Install Now**
4. 等待安装完成（大约 1-3 分钟）
5. 点击 **Close**

**验证安装成功：**
- **重新打开 PowerShell**
- 输入 `python --version`，能看到版本号即可

---

### 2.3 Mac：安装 Python

**方法一：使用 Homebrew（推荐）**

1. 打开终端，安装 Homebrew（如果没有）：
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. 使用 Homebrew 安装 Python：
```bash
brew install python
```

**方法二：直接从官网下载**
1. 访问 https://www.python.org/downloads/
2. 下载 macOS 安装包
3. 双击运行，按提示安装

**验证安装：**
```bash
python3 --version
pip3 --version
```

---

### 2.4 Linux：安装 Python

**Ubuntu / Debian：**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Fedora：**
```bash
sudo dnf install python3 python3-pip
```

**Arch Linux：**
```bash
sudo pacman -S python python-pip
```

**验证安装：**
```bash
python3 --version
pip3 --version
```

---

## 3. 第二步：安装 衍智体

### Windows

打开 PowerShell（**以管理员身份运行**），输入：

```powershell
pip install yanzhiti
```

### Mac

打开终端，输入：

```bash
pip3 install yanzhiti
```

### Linux

打开终端，输入：

```bash
pip3 install yanzhiti
```

**如果看到类似下面的文字，说明安装成功：**
```
Successfully installed yanzhiti-2.2.0
```

---

## 4. 第三步：启动衍智体

安装成功后，启动衍智体：

| 操作系统 | 启动命令 |
|---------|---------|
| Windows | `yzt` |
| Mac | `yzt` 或 `python3 -m yanzhiti` |
| Linux | `yzt` 或 `yanzhiti` |

### 4.1 启动方式一览

| 命令 | 说明 |
|------|------|
| `yzt` | 启动交互式对话（最常用） |
| `yzt --gui` | 启动网页界面（在浏览器中使用） |
| `yzt --setup` | 重新配置 AI 设置 |
| `yzt --diagnose` | 运行系统诊断 |

> 💡 **如果提示"找不到命令"**，尝试：
> - `python3 -m yanzhiti`（Mac/Linux）
> - `python -m yanzhiti`（Windows）

---

## 5. 首次配置 AI

第一次运行 `yzt` 时，会自动进入配置向导。

### 5.1 选择使用模式

```
🤖 衍智体配置向导

请选择 AI 供应商模式：

  [1] ☁️ 云端模式 (推荐) — 使用 OpenRouter 等云端 API
  [2] 🖥️ 本地模式 — 使用 Ollama 等本地模型
  [3] 🔧 内置模式 — 无需配置，内置小模型可用

请输入选项 (1/2/3):
```

**新手推荐选择 [1] 云端模式**，然后按照提示输入 API Key。

### 5.2 什么是 API Key？

API Key 就像一个**密码**，用于连接云端 AI 服务。

**推荐使用 OpenRouter（最简单）：**
1. 打开 https://openrouter.ai/
2. 注册账号（可以用 Google 登录）
3. 点击左侧 **Keys** → **Create Key**
4. 复制生成的 Key（一串随机字符）

### 5.3 没有 API Key 能用吗？

可以！选择 **内置模式 [3]**，会有一个内置的小模型可以体验基本功能，但能力有限。

---

## 6. 常见问题与解决方法

### 问题1：Windows 提示 "'pip' is not recognized"

**这是 Windows 新手最常遇到的问题**，意思是 Windows 找不到 Python。

#### 解决方法一：用 python -m pip 代替（最简单）

```powershell
python -m pip install yanzhiti
```

#### 解决方法二：重新安装 Python 并勾选 PATH

1. 打开 **控制面板** → **程序和功能**
2. 找到 **Python**，右键点击 **卸载**
3. 重新下载 Python：https://www.python.org/downloads/
4. **安装时一定要勾选 "Add Python to PATH"**
5. 安装完成后，**重新打开 PowerShell**，再试

#### 解决方法三：手动添加 PATH

1. 按 `Win + R`，输入 `sysdm.cpl`，回车
2. 点击 **高级** 选项卡 → **环境变量**
3. 在下方 **系统变量** 区域，找到 **Path**，双击
4. 点击 **新建**，添加这两行：
   ```
   C:\Users\你的用户名\AppData\Local\Programs\Python\Python312\
   C:\Users\你的用户名\AppData\Local\Programs\Python\Python312\Scripts\
   ```
   （把"你的用户名"换成你电脑的用户名，Python312 换成你的版本号）
5. **确定** → **确定** → **确定**
6. **重新打开 PowerShell**

---

### 问题2：Mac 提示 "Permission denied" 或 "Operation not permitted"

**解决方法：** 使用 sudo 获取管理员权限

```bash
sudo pip3 install yanzhiti
```

输入你的 Mac 开机密码即可。

---

### 问题3：Linux 提示 "Permission denied"

**解决方法：** 使用 sudo

```bash
sudo pip3 install yanzhiti
```

---

### 问题4：安装时提示 "Read timed out"（网络超时）

**解决方法：** 增加超时时间后重试

**Windows：**
```powershell
pip install yanzhiti --default-timeout=100
```

**Mac / Linux：**
```bash
pip3 install yanzhiti --default-timeout=100
```

---

### 问题5：提示 "WARNING: Ignoring invalid distribution"

这是 pip 缓存损坏，不影响正常使用。如果想清理：

**Windows：**
```powershell
pip cache purge
```

**Mac / Linux：**
```bash
pip3 cache purge
```

---

### 问题6：提示 "Python version mismatch"

你的 Python 版本太低了。衍智体需要 **Python 3.10 或更高版本**。

**Windows 解决方法：**
1. 卸载旧版本 Python
2. 从 https://www.python.org/downloads/ 下载并安装 **3.10/3.11/3.12**

**Mac 解决方法：**
```bash
brew install python@3.11
```

**Linux 解决方法：**
```bash
sudo apt update
sudo apt install python3.11
```

---

### 问题7：Mac 提示 "zsh: command not found: pip"

**解决方法：** 用 pip3 代替 pip

```bash
pip3 install yanzhiti
```

---

### 问题8：安装了但运行 `yzt` 提示找不到命令

**Windows 解决方法：**
```powershell
python -m yanzhiti
```

**Mac / Linux 解决方法：**
```bash
python3 -m yanzhiti
```

或检查安装位置：
```bash
which yzt
pip3 show yanzhiti
```

---

### 问题9：Linux 提示 "bash: pip3: command not found"

**解决方法：** 安装 pip3

```bash
sudo apt update
sudo apt install python3-pip
```

---

### 问题10：提示 "SSL" 或 "HTTPS" 相关错误

**解决方法：** 更新证书

**Windows：**
```powershell
python -m pip install --upgrade certifi
```

**Mac / Linux：**
```bash
sudo pip3 install --upgrade certifi
```

---

## 7. 完全卸载指南

### Windows

```powershell
pip uninstall yanzhiti
```

清理配置文件夹（可选）：
```powershell
Remove-Item -Recurse "$env:USERPROFILE\.yanzhiti"
```

### Mac / Linux

```bash
pip3 uninstall yanzhiti
```

清理配置文件夹（可选）：
```bash
rm -rf ~/.yanzhiti
```

---

## 📞 获取帮助

如果按照以上方法仍然无法解决问题：

1. 查看 GitHub Issues：https://github.com/yanzhiti/yanzhiti/issues
2. 创建新的 Issue，描述你的问题
3. 加入衍智体社区讨论

---

## 🎉 快速命令速查

| 操作系统 | 安装命令 | 启动命令 |
|---------|---------|---------|
| Windows | `pip install yanzhiti` | `yzt` |
| Mac | `pip3 install yanzhiti` | `yzt` 或 `python3 -m yanzhiti` |
| Linux | `pip3 install yanzhiti` | `yzt` |

**其他常用命令：**

```powershell
# 升级版本
pip install yanzhiti --upgrade

# 卸载
pip uninstall yanzhiti

# 查看版本
pip show yanzhiti
```

```bash
# 升级版本 (Mac/Linux)
pip3 install yanzhiti --upgrade

# 卸载 (Mac/Linux)
pip3 uninstall yanzhiti

# 查看版本 (Mac/Linux)
pip3 show yanzhiti
```

---

## 🖥️ 不同操作系统特殊说明

### Windows
- 如果使用 **WSL2**（Windows 子系统 Linux），可以按照 Linux 的方式安装
- 推荐使用 **PowerShell 7** 或 **Windows Terminal** 获得更好的体验

### Mac
- 如果遇到 **zsh 配置问题**，可能需要编辑 `~/.zshrc` 文件
- 推荐使用 **Homebrew** 管理 Python 版本

### Linux
- 如果遇到 **权限问题**，每个命令前加 `sudo`
- 不同发行版的包管理器不同（apt/dnf/pacman/yum），选择对应的命令

---

*本指南由衍智体 (YANZHITI) 项目组编写，专为新手设计，开源许可可自由分享。*
