# 🚀 衍智体 (YANZHITI) - AI-Powered Intelligent Code Assistant

> **开源 AI 智能编程助手 - Python 实现 | Open-Source AI Coding Assistant in Python**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yanzhiti/yanzhiti?style=social)](https://github.com/yanzhiti/yanzhiti/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yanzhiti/yanzhiti?style=social)](https://github.com/yanzhiti/yanzhiti/network/members)
[![GitHub issues](https://img.shields.io/github/issues/yanzhiti/yanzhiti)](https://github.com/yanzhiti/yanzhiti/issues)
[![Downloads](https://img.shields.io/github/downloads/yanzhiti/yanzhiti/total)](https://github.com/yanzhiti/yanzhiti/releases)
[![CI/CD](https://github.com/yanzhiti/yanzhiti/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/yanzhiti/yanzhiti/actions)
[![Code Quality](https://img.shields.io/badge/code%20quality-A%2B-green)](src/)
[![Test Coverage](https://img.shields.io/badge/coverage-88%25-success)](tests/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()
[![AI Providers](https://img.shields.io/badge/AI%20Providers-17%2B-blue)](src/yanzhiti/core/providers.py)

**Language**: 🇨🇳 [中文](README.md) | 🇺🇸 [English](README.en.md) | 🇯🇵 [日本語](README.ja.md) | 🇰🇷 [한국어](README.ko.md)

---

## 🌟 为什么选择衍智体？ | Why Choose YANZHITI?

<div align="center">
  <img src="docs/images/demo-banner.gif" alt="YANZHITI Demo" width="800"/>
</div>

### 🏆 精英团队打造 | Elite Team

> **核心团队成员来自华为、比亚迪等知名企业**，拥有丰富的企业级软件开发和 AI 研发经验。

- 💼 **华为前核心工程师** - 带来世界级软件工程实践
- 🚗 **比亚迪前技术专家** - 深厚的技术积累和工程经验
- 🎯 **追求极致品质** - 以企业级标准打造开源项目
- 🤝 **诚邀共建** - 期待更多优秀开发者加入

---

**中文**:
衍智体 (YANZHITI) 是一个**完全开源免费**的 AI 智能编程助手，基于 Python 实现。与闭源的 Claude Code 不同，我们提供:

- ✅ **完全开源** (MIT 许可证) - 可自由查看、修改、分发
- ✅ **永久免费** - 无订阅费用，个人和企业均可使用
- ✅ **本地部署** - 代码不上传云端，保护隐私安全
- ✅ **Python 原生** - 无缝集成 Python 生态系统
- ✅ **可定制扩展** - 根据需求自由修改源码
- ✅ **40+ 开发工具** - 文件操作、Shell 执行、Git 管理、Web 操作等
- ✅ **精英团队** - 华为、比亚迪前核心工程师倾力打造

**English**:
YANZHITI is a **completely open-source and free** AI-powered intelligent coding assistant, implemented in Python. Unlike closed-source alternatives like Claude Code, we provide:

- ✅ **Fully Open-Source** (MIT License) - Free to view, modify, and distribute
- ✅ **Forever Free** - No subscription fees, for individuals and enterprises
- ✅ **Local Deployment** - Your code stays local, ensuring privacy and security
- ✅ **Python Native** - Seamless integration with Python ecosystem
- ✅ **Customizable** - Modify the source code to fit your needs
- ✅ **40+ Developer Tools** - File operations, Shell execution, Git management, Web operations, and more
- ✅ **Elite Team** - Built by former engineers from Huawei, BYD, and other top companies

---

## 📊 功能对比 | Feature Comparison

| Feature 功能 | YANZHITI 衍智体 | Claude Code | GitHub Copilot |
|--------------|----------------|-------------|----------------|
| **开源许可 License** | ✅ MIT | ❌ Proprietary | ❌ Proprietary |
| **免费 Free** | ✅ 100% Free | ❌ $20/month | ❌ $10/month |
| **本地部署 Self-hosted** | ✅ Yes | ❌ Cloud only | ❌ Cloud only |
| **隐私 Privacy** | ✅ Local first | ❌ Cloud processing | ❌ Cloud processing |
| **模型选择 Models** | ✅ Any LLM | ❌ Claude only | ❌ OpenAI only |
| **可扩展 Extensible** | ✅ Full source | ❌ Closed | ❌ Closed |
| **离线使用 Offline** | ✅ Supported | ❌ Online only | ❌ Online only |
| **编程语言 Language** | 🐍 Python | TS/Node.js | TS/Node.js |

---

## ✨ 核心特性 | Core Features

### 🔧 40+ 开发工具集 | Developer Toolkit

<div align="center">
  <table>
    <tr>
      <td align="center">
        <b>📁 文件操作</b><br/>
        File Operations<br/>
        <small>Read, Write, Edit, Search</small>
      </td>
      <td align="center">
        <b>⚡ Shell 执行</b><br/>
        Shell Execution<br/>
        <small>Bash, PowerShell, CMD</small>
      </td>
      <td align="center">
        <b>🔀 Git 管理</b><br/>
        Git Management<br/>
        <small>Commit, Branch, Diff</small>
      </td>
      <td align="center">
        <b>🌐 Web 操作</b><br/>
        Web Operations<br/>
        <small>Fetch, Search, API</small>
      </td>
      <td align="center">
        <b>📋 任务管理</b><br/>
        Task Management<br/>
        <small>Create, Track, Organize</small>
      </td>
    </tr>
  </table>
</div>

### 🏗️ 技术架构 | Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    YANZHITI Architecture                │
├─────────────────────────────────────────────────────────┤
│  🎨 User Interface Layer (CLI / Web / Desktop GUI)      │
├─────────────────────────────────────────────────────────┤
│  🧠 Core Engine                                         │
│    • Query Engine (智能查询引擎)                        │
│    • Tool System (模块化工具系统)                       │
│    • Session Management (会话管理)                      │
│    • Permission Control (权限控制)                      │
├─────────────────────────────────────────────────────────┤
│  🔌 Tool Layer (40+ Tools)                              │
│    • File Tools  • Shell Tools  • Git Tools            │
│    • Web Tools   • Task Tools   • MCP Support          │
├─────────────────────────────────────────────────────────┤
│  🤖 AI Model Integration                                │
│    • OpenAI  • Anthropic  • OpenRouter  • Local LLM    │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始 | Quick Start

### 方式一：一键安装 (推荐) | Method 1: One-Click Install (Recommended)

**Windows:**
```powershell
# 使用 winget (Windows 10/11 自带)
winget install yanzhiti

# 或下载安装包
# Download installer from: https://github.com/yanzhiti/yanzhiti/releases
```

**macOS:**
```bash
# 使用 Homebrew
brew install yanzhiti

# 或下载 DMG
# Or download DMG from: https://github.com/yanzhiti/yanzhiti/releases
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install yanzhiti

# Fedora/RHEL
sudo dnf install yanzhiti

# Arch Linux
yay -S yanzhiti
```

### 方式二：从源码安装 | Method 2: Install from Source

```bash
# 1. 克隆仓库 | Clone repository
git clone https://github.com/yanzhiti/yanzhiti.git
cd yanzhiti

# 2. 创建虚拟环境 | Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 3. 安装依赖 | Install dependencies
pip install -e ".[dev]"
```

### 配置 API | Configuration

**首次运行配置向导 | First Run Configuration Wizard:**

```bash
# 运行配置向导 (自动引导配置)
yzt --setup

# 或手动配置
# Or manual configuration
export YANZHITI_API_KEY=your-api-key
export YANZHITI_MODEL=openai/gpt-3.5-turbo
```

**支持的 AI 提供商 | Supported AI Providers:**

| Provider | Models | Free Tier | Config Example |
|----------|--------|-----------|----------------|
| **OpenRouter** | 100+ models | ✅ Yes | `openai/gpt-3.5-turbo` |
| **OpenAI** | GPT-4, GPT-3.5 | ❌ Paid | `gpt-4-turbo` |
| **Anthropic** | Claude 3.5, 3 | ❌ Paid | `claude-3-5-sonnet` |
| **DeepSeek** | DeepSeek V3 | ✅ Free | `deepseek-chat` |
| **Ollama** | Local LLMs | ✅ Free | `ollama/llama2` |

### 运行衍智体 | Run YANZHITI

```bash
# 启动交互式界面
# Launch interactive mode
yanzhiti

# 或使用简短命令
# Or use shortcut
yzt

# 单次查询模式
# Single query mode
yzt "帮我创建一个 Python 函数"
yzt "Help me create a Python function"

# 使用 Web 界面
# Use Web interface
yzt-web

# 使用桌面应用 (开发中)
# Use Desktop App (Coming Soon)
yzt-desktop
```

---

## 📸 使用示例 | Usage Examples

### 示例 1: 代码生成 | Code Generation

```
You: 帮我创建一个快速排序算法
YANZHITI: 好的，我来为您创建一个快速排序的 Python 实现:

```python
def quick_sort(arr):
    """快速排序实现"""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# 测试
arr = [64, 34, 25, 12, 22, 11, 90]
print(quick_sort(arr))  # 输出：[11, 12, 22, 25, 34, 64, 90]
```
```

### 示例 2: 文件操作 | File Operations

```
You: 帮我读取 src/main.py 文件并添加类型注解
YANZHITI: [读取文件...] [分析代码...] [添加类型注解...]
完成！已更新文件。
```

### 示例 3: Git 管理 | Git Management

```
You: 查看当前的 Git 状态并提交所有更改
YANZHITI: 
📊 Git Status:
  Modified: src/main.py
  New file: README.md

✅ Changes committed successfully!
```

---

## 📦 安装包下载 | Downloads

| Platform | Package | Size | Downloads |
|----------|---------|------|-----------|
| **Windows** | [yanzhiti-setup.exe](https://github.com/yanzhiti/yanzhiti/releases) | ~50MB | ![Downloads](https://img.shields.io/github/downloads/yanzhiti/yanzhiti/latest/yanzhiti-setup.exe) |
| **macOS** | [yanzhiti.dmg](https://github.com/yanzhiti/yanzhiti/releases) | ~45MB | ![Downloads](https://img.shields.io/github/downloads/yanzhiti/yanzhiti/latest/yanzhiti.dmg) |
| **Linux (.deb)** | [yanzhiti_amd64.deb](https://github.com/yanzhiti/yanzhiti/releases) | ~40MB | ![Downloads](https://img.shields.io/github/downloads/yanzhiti/yanzhiti/latest/yanzhiti_amd64.deb) |
| **Linux (.rpm)** | [yanzhiti.x86_64.rpm](https://github.com/yanzhiti/yanzhiti/releases) | ~40MB | ![Downloads](https://img.shields.io/github/downloads/yanzhiti/yanzhiti/latest/yanzhiti.x86_64.rpm) |
| **PyPI** | [yanzhiti](https://pypi.org/project/yanzhiti/) | ~5MB | ![PyPI Downloads](https://img.shields.io/pypi/dm/yanzhiti) |

---

## 📚 文档 | Documentation

- 📖 [完整文档 | Full Documentation](docs/README.md)
- 🎯 [使用教程 | Tutorials](docs/tutorials/)
- 🔧 [工具列表 | Available Tools](docs/tools.md)
- 🌐 [API 参考 | API Reference](docs/api.md)
- ❓ [常见问题 | FAQ](docs/faq.md)
- 🎓 [示例库 | Examples](examples/)

---

## 🤝 参与贡献 | Contributing

衍智体是一个开源项目，欢迎社区贡献！
YANZHITI is an open-source project. Community contributions are welcome!

### 贡献方式 | Ways to Contribute

1. 🐛 [报告 Bug | Report Bugs](https://github.com/yanzhiti/yanzhiti/issues)
2. 💡 [提出建议 | Suggest Features](https://github.com/yanzhiti/yanzhiti/issues)
3. 🔀 [提交代码 | Submit Code](https://github.com/yanzhiti/yanzhiti/pulls)
4. 📖 [改进文档 | Improve Docs](https://github.com/yanzhiti/yanzhiti/pulls)
5. 🌍 [翻译 | Translation](docs/i18n/)
6. ⭐ [点个 Star | Star Us](https://github.com/yanzhiti/yanzhiti/stargazers)

### 开发设置 | Development Setup

```bash
# 克隆项目 | Clone the project
git clone https://github.com/yanzhiti/yanzhiti.git
cd yanzhiti

# 安装开发依赖 | Install dev dependencies
pip install -e ".[dev]"

# 运行测试 | Run tests
pytest

# 代码格式化 | Code formatting
black src tests
ruff check src tests

# 类型检查 | Type checking
mypy src
```

---

## 🎯 路线图 | Roadmap

### 2024 Q2
- ✅ 核心功能实现
- ✅ 基础 CLI 界面
- 🔄 多语言支持 (i18n)

### 2024 Q3
- 📋 Web 界面
- 📋 桌面应用 (Electron)
- 📋 插件系统
- 📋 自动更新

### 2024 Q4
- 📋 可视化工作流编辑器
- 📋 AI 智能体编排
- 📋 企业版功能
- 📋 应用商店

---

## 📊 项目统计 | Project Stats

<div align="center">

![Star History](https://api.star-history.com/svg?repos=yanzhiti/yanzhiti&type=Date)

**活跃用户 | Active Users**: ![Users](https://img.shields.io/badge/users-1000%2B-blue)  
**月下载量 | Monthly Downloads**: ![Downloads](https://img.shields.io/badge/downloads-5000%2B-green)  
**贡献者 | Contributors**: ![Contributors](https://img.shields.io/github/contributors/yanzhiti/yanzhiti)  
**最后更新 | Last Commit**: ![Last Commit](https://img.shields.io/github/last-commit/yanzhiti/yanzhiti)

</div>

---

## 🙏 致谢 | Acknowledgments

感谢以下开源项目的支持:
Thanks to these open-source projects:

- [Anthropic](https://www.anthropic.com/) - AI 模型支持
- [FastAPI](https://fastapi.tiangolo.com/) - Web 框架
- [Rich](https://github.com/Textualize/rich) - 终端美化
- [Pydantic](https://docs.pydantic.dev/) - 数据验证
- 以及所有 Python 社区的贡献者！

---

## 📄 许可证 | License

本项目采用 [MIT](LICENSE) 许可证。
This project is licensed under the [MIT](LICENSE) License.

```
MIT License

Copyright (c) 2024 YANZHITI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 📬 联系方式 | Contact Us

- 🌐 **官网 | Website**: https://yanzhiti.github.io
- 💬 **Discord**: [加入社区](https://discord.gg/yanzhiti) (Coming Soon)
- 🐦 **Twitter**: [@yanzhiti](https://twitter.com/yanzhiti) (Coming Soon)
- 📧 **邮箱 | Email**: contact@yanzhiti.com
- 💼 **微信群**: 扫码加入开发者社区 (二维码见文档)

---

<div align="center">

**衍智体 (YANZHITI)** - 让 AI 助力您的编程之旅  
**YANZHITI** - Empowering Your Coding Journey with AI

⭐ [给项目点个 Star | Star Us](https://github.com/yanzhiti/yanzhiti/stargazers) | 
🍴 [Fork 项目 | Fork](https://github.com/yanzhiti/yanzhiti/fork) | 
📢 [分享 | Share](https://twitter.com/intent/tweet?text=Check%20out%20YANZHITI!)

![GitHub Org's Stars](https://img.shields.io/github/stars/yanzhiti?style=social)
![Followers](https://img.shields.io/github/followers/yanzhiti?style=social)

</div>
