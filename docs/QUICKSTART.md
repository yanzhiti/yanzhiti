# 🚀 快速入门指南 | Quick Start Guide

> 5 分钟快速开始使用衍智体 | Get started with YANZHITI in 5 minutes

[![快速开始](https://img.shields.io/badge/快速开始-5 分钟-green)]()
[![难度](https://img.shields.io/badge/难度-简单-blue)]()
[![更新时间](https://img.shields.io/badge/更新时间-2024--04-yellow)]()

---

## 📋 目录 | Table of Contents

1. [安装](#安装)
2. [配置](#配置)
3. [运行](#运行)
4. [第一个任务](#第一个任务)
5. [下一步](#下一步)

---

## 1️⃣ 安装 | Installation

### 方式 A: 一键安装 (推荐) | One-Click Install (Recommended)

**Windows:**
```powershell
winget install yanzhiti
```

**macOS:**
```bash
brew install yanzhiti
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install yanzhiti
```

### 方式 B: 从源码安装 | Install from Source

```bash
# 1. 克隆仓库 | Clone repository
git clone https://github.com/yanzhiti/yanzhiti.git
cd yanzhiti

# 2. 创建虚拟环境 | Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 3. 安装依赖 | Install dependencies
pip install -e ".[dev]"
```

---

## 2️⃣ 配置 | Configuration

### 方式 A: 使用配置向导 (推荐) | Using Setup Wizard (Recommended)

```bash
# 运行配置向导
yzt --setup

# 或
yanzhiti --setup
```

配置向导会引导您完成:
1. 选择 AI 提供商 (OpenRouter/OpenAI/DeepSeek 等)
2. 输入 API 密钥
3. 选择模型
4. 测试连接
5. 保存配置

### 方式 B: 手动配置 | Manual Configuration

1. **获取 API 密钥 | Get API Key**

   访问 [OpenRouter](https://openrouter.ai/keys) 或其他提供商获取 API 密钥

2. **创建 .env 文件 | Create .env File**

在项目根目录创建 `.env` 文件:

```bash
# Windows PowerShell
notepad .env

# macOS/Linux
nano .env
```

添加以下内容:

```env
# API 配置
YANZHITI_API_KEY=sk-or-v1-your-api-key-here
YANZHITI_BASE_URL=https://openrouter.ai/api/v1
YANZHITI_MODEL=openai/gpt-3.5-turbo

# 模型参数
YANZHITI_MAX_TOKENS=4096
YANZHITI_TEMPERATURE=1.0
```

3. **测试配置 | Test Configuration**

```bash
# 运行诊断工具
yzt --diagnose
```

---

## 3️⃣ 运行 | Run

### 交互式模式 | Interactive Mode

```bash
# 启动交互式界面
yanzhiti

# 或使用简短命令
yzt
```

启动后会看到:

```
╭──────────────────────────────────────────────────────╮
│ 衍智体 (YANZHITI) - Python Edition                   │
│ Version: 2.1.88                                      │
│ Type your query and press Enter. Use Ctrl+C to exit. │
╰──────────────────────────────────────────────────────╯

You: 
```

### 单次查询模式 | Single Query Mode

```bash
# 执行单个任务
yzt "帮我创建一个 Python 函数"

# 或
yanzhiti "Help me create a Python function"
```

---

## 4️⃣ 第一个任务 | First Task

### 任务 1: 代码生成 | Code Generation

**输入 | Input:**
```
帮我创建一个快速排序算法，用 Python 实现
```

**期望输出 | Expected Output:**
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

### 任务 2: 文件操作 | File Operations

**输入 | Input:**
```
读取当前目录下的 README.md 文件，总结主要内容
```

**期望输出 | Expected Output:**
```
我已读取 README.md 文件，主要内容包括:

1. 项目简介：衍智体是一个开源 AI 编程助手
2. 核心特性：40+ 开发工具集
3. 安装方法：支持多种安装方式
4. 使用示例：代码生成、文件操作等
...
```

### 任务 3: Git 管理 | Git Management

**输入 | Input:**
```
查看当前的 Git 状态
```

**期望输出 | Expected Output:**
```
📊 Git Status:
  On branch: main
  Modified files:
    - src/main.py
    - README.md
  
  No staged changes
```

---

## 5️⃣ 下一步 | Next Steps

### 学习更多功能 | Learn More Features

- 📖 [完整文档 | Full Documentation](docs/README.md)
- 🎯 [使用教程 | Tutorials](docs/tutorials/)
- 🔧 [可用工具 | Available Tools](docs/tools.md)
- ❓ [常见问题 | FAQ](docs/faq.md)

### 实践练习 | Practice Exercises

1. **代码重构** | Code Refactoring
   ```
   优化这段代码，使其更简洁高效
   ```

2. **调试帮助** | Debug Help
   ```
   分析这个错误并给出修复建议：[粘贴错误信息]
   ```

3. **文档生成** | Documentation Generation
   ```
   为这个函数添加详细的注释和文档字符串
   ```

4. **测试生成** | Test Generation
   ```
   为这个模块创建单元测试
   ```

### 加入社区 | Join Community

- 💬 [GitHub Discussions](https://github.com/yanzhiti/yanzhiti/discussions)
- 🐛 [报告问题 | Report Issues](https://github.com/yanzhiti/yanzhiti/issues)
- ⭐ [给项目 Star](https://github.com/yanzhiti/yanzhiti/stargazers)

---

## 🆘 常见问题 | FAQ

### Q1: 找不到 API 密钥怎么办？
**A:** 访问 [OpenRouter](https://openrouter.ai/keys) 或其他 AI 提供商注册获取。推荐使用 OpenRouter，支持多个模型。

### Q2: 配置向导无法连接 API？
**A:** 
1. 检查网络连接
2. 确认 API 密钥正确
3. 检查防火墙设置
4. 运行 `yzt --diagnose` 诊断问题

### Q3: 如何切换模型？
**A:** 修改 `.env` 文件中的 `YANZHITI_MODEL` 变量，或重新运行配置向导 `yzt --setup`。

### Q4: 命令不存在怎么办？
**A:** 
- Windows: 确保 Scripts 目录已添加到 PATH
- macOS/Linux: 确保运行 `source venv/bin/activate`
- 或使用完整路径：`python -m yanzhiti.cli.main`

### Q5: 如何退出交互式模式？
**A:** 输入 `/exit` 或按 `Ctrl+C`。

---

## 📞 获取帮助 | Get Help

如果遇到问题:

1. **查看文档** | Check Documentation
   - [完整文档](docs/README.md)
   - [常见问题](docs/faq.md)

2. **运行诊断** | Run Diagnostic
   ```bash
   yzt --diagnose
   ```

3. **寻求帮助** | Ask for Help
   - [GitHub Issues](https://github.com/yanzhiti/yanzhiti/issues)
   - [Discussions](https://github.com/yanzhiti/yanzhiti/discussions)

---

## 🎉 恭喜！| Congratulations!

您已经完成了快速入门！现在可以开始使用衍智体进行 AI 辅助编程了。

**祝您编程愉快！| Happy Coding!** 🚀

---

<div align="center">

**衍智体 (YANZHITI)** - 让 AI 助力您的编程之旅

[开始使用](#1️⃣-安装) | [查看文档](docs/README.md) | [报告问题](https://github.com/yanzhiti/yanzhiti/issues)

</div>
