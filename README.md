# 🚀 衍智体 (YANZHITI)

> **开源 AI 智能编程助手 - Python 实现**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yanzhiti/yanzhiti?style=social)](https://github.com/yanzhiti/yanzhiti)

---

## 🌟 为什么选择衍智体？

衍智体（YANZHITI）是一个**完全开源免费**的 AI 智能编程助手，基于 Python 实现。与闭源的 Claude Code 不同，我们提供：

- ✅ **完全开源** (MIT 许可证) - 可自由查看、修改、分发
- ✅ **永久免费** - 无订阅费用，个人和企业均可使用
- ✅ **本地部署** - 代码不上传云端，保护隐私安全
- ✅ **Python 原生** - 无缝集成 Python 生态系统
- ✅ **可定制扩展** - 根据需求自由修改源码

---

## 📊 与 Claude Code 对比

| 特性 | 衍智体 (YANZHITI) | Claude Code |
|------|------------------|-------------|
| **开源许可** | ✅ 完全开源 (MIT) | ❌ 闭源商业软件 |
| **使用成本** | ✅ 永久免费 | ❌ 需要付费订阅 |
| **自托管支持** | ✅ 支持本地部署 | ❌ 仅云服务 |
| **自定义扩展** | ✅ 可自由修改源码 | ❌ 无法修改 |
| **数据隐私** | ✅ 代码完全本地 | ❌ 需上传云端 |
| **模型选择** | ✅ 支持多种模型 | ❌ 仅限 Claude |
| **社区支持** | ✅ 开放社区贡献 | ❌ 官方支持 |
| **Python 生态** | ✅ 原生 Python | ❌ 基于 TypeScript |
| **离线使用** | ✅ 支持离线模式 | ❌ 需要网络 |

---

## ✨ 核心特性

### 🔧 40+ 开发工具集

- **📁 文件操作工具**: 读写、编辑、Glob 匹配、Grep 搜索、文件监控
- **⚡ Shell 执行工具**: Bash/PowerShell 支持，内置权限控制
- **🔀 Git 操作工具**: 状态查看、提交、分支管理
- **🌐 Web 操作工具**: 网页获取、搜索、API 调用
- **📋 任务管理工具**: 任务创建、分配、跟踪、子任务分解
- **🔒 权限控制系统**: 细粒度权限管理，安全可控

### 🏗️ 技术架构

- **⚙️ 智能查询引擎**: 高级查询处理和执行系统
- **🧩 模块化工具系统**: 支持动态注册和扩展
- **🌉 桥接通信系统**: 支持远程操作和会话管理
- **📡 MCP 支持**: Model Context Protocol 集成，支持多种 AI 模型
- **👥 多智能体支持**: 基于智能体的任务执行

---

## 🚀 快速开始

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/yanzhiti/yanzhiti.git
cd yanzhiti

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -e ".[dev]"
```

### 运行衍智体

```bash
# 设置 API 密钥
export YANZHITI_API_KEY=your-api-key

# 运行衍智体
yanzhiti

# 或使用简短别名
yzt
```

---

## 📁 项目结构

```
yanzhiti/
├── src/
│   └── yanzhiti/
│       ├── cli/           # 命令行接口
│       ├── core/          # 核心功能（查询引擎、工具系统）
│       ├── tools/         # 40+ 工具实现
│       ├── web/           # Web 服务
│       ├── utils/         # 工具函数
│       └── types/         # 类型定义
├── tests/                 # 测试套件
├── docs/                  # 文档
└── examples/              # 示例用法
```

---

## 🛠️ 开发

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black src tests
ruff check src tests
```

### 类型检查

```bash
mypy src
```

---

## 🎯 核心优势

| 优势 | 说明 |
|------|------|
| 🎁 **完全免费** | MIT 许可证，个人和企业均可免费使用 |
| 🔓 **源码开放** | 可查看、修改、定制源代码 |
| 🏠 **本地部署** | 代码不上传云端，保护隐私安全 |
| 🐍 **Python 原生** | 无缝集成 Python 生态系统 |
| 🔧 **易于扩展** | 简单 API 即可添加自定义工具 |
| 🚀 **轻量快速** | 低资源占用，响应迅速 |

---

## ⚙️ 配置

配置通过以下方式管理:
- 环境变量
- `.env` 文件
- 配置文件 (TOML/YAML)
- 命令行参数

---

## 🤝 参与贡献

衍智体是一个开源项目，欢迎社区贡献！

- 🐛 [提交 Issue](https://github.com/yanzhiti/yanzhiti/issues)
- 🔀 [提交 Pull Request](https://github.com/yanzhiti/yanzhiti/pulls)
- ⭐ 给项目点个 Star 支持我们！

---

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证 - 详见 LICENSE 文件。

---

## 🙏 致谢

感谢 Python 社区提供的优秀库和工具支持。

---

<div align="center">

**衍智体 (YANZHITI)** - 让 AI 助力您的编程之旅

⭐ 如果这个项目对您有帮助，请给我们一个 Star！

</div>
