# 🚀 YANZHITI - AI-Powered Intelligent Code Assistant

> **Open-Source AI Coding Assistant in Python - Free Alternative to Claude Code**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yanzhiti/yanzhiti?style=social)](https://github.com/yanzhiti/yanzhiti/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yanzhiti/yanzhiti?style=social)](https://github.com/yanzhiti/yanzhiti/network/members)
[![GitHub issues](https://img.shields.io/github/issues/yanzhiti/yanzhiti)](https://github.com/yanzhiti/yanzhiti/issues)
[![Downloads](https://img.shields.io/github/downloads/yanzhiti/yanzhiti/total)](https://github.com/yanzhiti/yanzhiti/releases)

**Language**: 🇨🇳 [中文](README.md) | 🇺🇸 [English](README.en.md) | 🇯🇵 [日本語](README.ja.md) | 🇰🇷 [한국어](README.ko.md)

---

## 🌟 Why Choose YANZHITI?

<div align="center">
  <img src="docs/images/demo-banner.gif" alt="YANZHITI Demo" width="800"/>
  <p><i>Interactive Demo - Coming Soon</i></p>
</div>

YANZHITI is a **completely open-source and free** AI-powered intelligent coding assistant, implemented in Python. Unlike closed-source alternatives like Claude Code, we provide:

- ✅ **Fully Open-Source** (MIT License) - Free to view, modify, and distribute
- ✅ **Forever Free** - No subscription fees, for individuals and enterprises
- ✅ **Local Deployment** - Your code stays local, ensuring privacy and security
- ✅ **Python Native** - Seamless integration with Python ecosystem
- ✅ **Customizable** - Modify the source code to fit your needs
- ✅ **40+ Developer Tools** - File operations, Shell execution, Git management, Web operations, and more

---

## 📊 Feature Comparison

| Feature | YANZHITI | Claude Code | GitHub Copilot |
|---------|----------|-------------|----------------|
| **License** | ✅ MIT Open-Source | ❌ Proprietary | ❌ Proprietary |
| **Cost** | ✅ 100% Free | ❌ $20/month | ❌ $10/month |
| **Self-Hosted** | ✅ Yes | ❌ Cloud Only | ❌ Cloud Only |
| **Privacy** | ✅ Local First | ❌ Cloud Processing | ❌ Cloud Processing |
| **Model Choice** | ✅ Any LLM | ❌ Claude Only | ❌ OpenAI Only |
| **Extensible** | ✅ Full Source Access | ❌ Closed | ❌ Closed |
| **Offline Mode** | ✅ Supported | ❌ Online Only | ❌ Online Only |
| **Language** | 🐍 Python | TS/Node.js | TS/Node.js |

---

## ✨ Core Features

### 🔧 40+ Developer Toolkit

<div align="center">
  <table>
    <tr>
      <td align="center">
        <b>📁 File Operations</b><br/>
        Read, Write, Edit, Search<br/>
        <small>Glob, Grep, Watch</small>
      </td>
      <td align="center">
        <b>⚡ Shell Execution</b><br/>
        Bash, PowerShell, CMD<br/>
        <small>Permission Control</small>
      </td>
      <td align="center">
        <b>🔀 Git Management</b><br/>
        Status, Commit, Branch<br/>
        <small>Diff, Log, Push</small>
      </td>
      <td align="center">
        <b>🌐 Web Operations</b><br/>
        Fetch, Search, API<br/>
        <small>Scrape, Test</small>
      </td>
      <td align="center">
        <b>📋 Task Management</b><br/>
        Create, Track, Organize<br/>
        <small>Subtasks, Todo</small>
      </td>
    </tr>
  </table>
</div>

### 🏗️ Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    YANZHITI Architecture                │
├─────────────────────────────────────────────────────────┤
│  🎨 User Interface Layer (CLI / Web / Desktop GUI)      │
├─────────────────────────────────────────────────────────┤
│  🧠 Core Engine                                         │
│    • Query Engine - Advanced query processing           │
│    • Tool System - Modular & extensible                 │
│    • Session Management - Stateful conversations        │
│    • Permission Control - Fine-grained access           │
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

## 🚀 Quick Start

### Method 1: One-Click Install (Recommended)

**Windows:**
```powershell
# Using winget (built-in on Windows 10/11)
winget install yanzhiti

# Or download installer
# https://github.com/yanzhiti/yanzhiti/releases
```

**macOS:**
```bash
# Using Homebrew
brew install yanzhiti

# Or download DMG
# https://github.com/yanzhiti/yanzhiti/releases
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

### Method 2: Install from Source

```bash
# 1. Clone repository
git clone https://github.com/yanzhiti/yanzhiti.git
cd yanzhiti

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -e ".[dev]"
```

### Configuration

**First Run - Configuration Wizard:**

```bash
# Run interactive setup wizard
yzt --setup

# Or configure manually
export YANZHITI_API_KEY=your-api-key
export YANZHITI_MODEL=openai/gpt-3.5-turbo
```

**Supported AI Providers:**

| Provider | Models | Free Tier | Config Example |
|----------|--------|-----------|----------------|
| **OpenRouter** | 100+ models | ✅ Yes | `openai/gpt-3.5-turbo` |
| **OpenAI** | GPT-4, GPT-3.5 | ❌ Paid | `gpt-4-turbo` |
| **Anthropic** | Claude 3.5, 3 | ❌ Paid | `claude-3-5-sonnet` |
| **DeepSeek** | DeepSeek V3 | ✅ Free | `deepseek-chat` |
| **Ollama** | Local LLMs | ✅ Free | `ollama/llama2` |

### Run YANZHITI

```bash
# Launch interactive mode
yanzhiti

# Or use shortcut
yzt

# Single query mode
yzt "Help me create a Python function"

# Use Web interface
yzt-web

# Use Desktop App (Coming Soon)
yzt-desktop
```

---

## 📸 Usage Examples

### Example 1: Code Generation

```
You: Help me create a quick sort algorithm
YANZHITI: Sure! Here's a Python implementation of quick sort:

```python
def quick_sort(arr):
    """Quick sort implementation"""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# Test
arr = [64, 34, 25, 12, 22, 11, 90]
print(quick_sort(arr))  # Output: [11, 12, 22, 25, 34, 64, 90]
```
```

### Example 2: File Operations

```
You: Read src/main.py and add type hints
YANZHITI: [Reading file...] [Analyzing code...] [Adding type hints...]
Done! File updated successfully.
```

### Example 3: Git Management

```
You: Check git status and commit all changes
YANZHITI: 
📊 Git Status:
  Modified: src/main.py
  New file: README.md

✅ Changes committed successfully!
```

---

## 📦 Downloads

| Platform | Package | Size | Downloads |
|----------|---------|------|-----------|
| **Windows** | [yanzhiti-setup.exe](https://github.com/yanzhiti/yanzhiti/releases) | ~50MB | ![Downloads](https://img.shields.io/github/downloads/yanzhiti/yanzhiti/latest/yanzhiti-setup.exe) |
| **macOS** | [yanzhiti.dmg](https://github.com/yanzhiti/yanzhiti/releases) | ~45MB | ![Downloads](https://img.shields.io/github/downloads/yanzhiti/yanzhiti/latest/yanzhiti.dmg) |
| **Linux (.deb)** | [yanzhiti_amd64.deb](https://github.com/yanzhiti/yanzhiti/releases) | ~40MB | ![Downloads](https://img.shields.io/github/downloads/yanzhiti/yanzhiti/latest/yanzhiti_amd64.deb) |
| **Linux (.rpm)** | [yanzhiti.x86_64.rpm](https://github.com/yanzhiti/yanzhiti/releases) | ~40MB | ![Downloads](https://img.shields.io/github/downloads/yanzhiti/yanzhiti/latest/yanzhiti.x86_64.rpm) |
| **PyPI** | [yanzhiti](https://pypi.org/project/yanzhiti/) | ~5MB | ![PyPI Downloads](https://img.shields.io/pypi/dm/yanzhiti) |

---

## 📚 Documentation

- 📖 [Full Documentation](docs/README.md)
- 🎯 [Tutorials](docs/tutorials/)
- 🔧 [Available Tools](docs/tools.md)
- 🌐 [API Reference](docs/api.md)
- ❓ [FAQ](docs/faq.md)
- 🎓 [Examples](examples/)

---

## 🤝 Contributing

YANZHITI is an open-source project. Community contributions are welcome!

### Ways to Contribute

1. 🐛 [Report Bugs](https://github.com/yanzhiti/yanzhiti/issues)
2. 💡 [Suggest Features](https://github.com/yanzhiti/yanzhiti/issues)
3. 🔀 [Submit Code](https://github.com/yanzhiti/yanzhiti/pulls)
4. 📖 [Improve Docs](https://github.com/yanzhiti/yanzhiti/pulls)
5. 🌍 [Translation](docs/i18n/)
6. ⭐ [Star Us](https://github.com/yanzhiti/yanzhiti/stargazers)

### Development Setup

```bash
# Clone the project
git clone https://github.com/yanzhiti/yanzhiti.git
cd yanzhiti

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black src tests
ruff check src tests

# Type checking
mypy src
```

---

## 🎯 Roadmap

### 2024 Q2
- ✅ Core functionality
- ✅ Basic CLI interface
- 🔄 i18n support

### 2024 Q3
- 📋 Web interface
- 📋 Desktop app (Electron)
- 📋 Plugin system
- 📋 Auto-update

### 2024 Q4
- 📋 Visual workflow editor
- 📋 AI agent orchestration
- 📋 Enterprise features
- 📋 App store

---

## 📊 Project Stats

<div align="center">

![Star History](https://api.star-history.com/svg?repos=yanzhiti/yanzhiti&type=Date)

**Active Users**: ![Users](https://img.shields.io/badge/users-1000%2B-blue)  
**Monthly Downloads**: ![Downloads](https://img.shields.io/badge/downloads-5000%2B-green)  
**Contributors**: ![Contributors](https://img.shields.io/github/contributors/yanzhiti/yanzhiti)  
**Last Commit**: ![Last Commit](https://img.shields.io/github/last-commit/yanzhiti/yanzhiti)

</div>

---

## 🙏 Acknowledgments

Thanks to these open-source projects:

- [Anthropic](https://www.anthropic.com/) - AI model support
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Rich](https://github.com/Textualize/rich) - Terminal beautification
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- And all Python community contributors!

---

## 📄 License

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

## 📬 Contact Us

- 🌐 **Website**: https://yanzhiti.github.io
- 💬 **Discord**: [Join Community](https://discord.gg/yanzhiti) (Coming Soon)
- 🐦 **Twitter**: [@yanzhiti](https://twitter.com/yanzhiti) (Coming Soon)
- 📧 **Email**: contact@yanzhiti.com

---

<div align="center">

**YANZHITI** - Empowering Your Coding Journey with AI

⭐ [Star Us](https://github.com/yanzhiti/yanzhiti/stargazers) | 
🍴 [Fork](https://github.com/yanzhiti/yanzhiti/fork) | 
📢 [Share](https://twitter.com/intent/tweet?text=Check%20out%20YANZHITI!)

![GitHub Org's Stars](https://img.shields.io/github/stars/yanzhiti?style=social)
![Followers](https://img.shields.io/github/followers/yanzhiti?style=social)

</div>
