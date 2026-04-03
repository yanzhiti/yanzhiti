# 衍智体 (YANZHITI)

> AI-Powered Intelligent Code Assistant - Python Implementation

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 项目简介

衍智体（YANZHITI）是一个基于 Python 实现的 AI 智能编程助手，提供强大的代码生成、重构和开发辅助功能。本项目是对 Anthropic Claude Code CLI 的完整 Python 重构实现。

## 核心特性

- **40+ 工具集**: 涵盖文件操作、代码编辑、Shell 执行、Git 操作等
- **智能查询引擎**: 高级查询处理和执行系统
- **桥接通信系统**: 支持远程操作和会话管理
- **权限控制系统**: 细粒度的权限管理
- **会话管理**: 持久化会话存储和历史记录
- **MCP 支持**: Model Context Protocol 集成
- **多智能体支持**: 基于智能体的任务执行

## 安装

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/yanzhiti/yanzhiti.git
cd yanzhiti

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 开发模式安装
pip install -e ".[dev]"
```

### 使用 pip 安装

```bash
pip install yanzhiti
```

## 快速开始

```bash
# 设置 API 密钥
export ANTHROPIC_API_KEY=your-api-key

# 运行衍智体
yanzhiti

# 或使用简短别名
yzt
```

## 项目结构

```
yanzhiti/
├── src/
│   └── yanzhiti/
│       ├── cli/           # 命令行接口
│       ├── core/          # 核心功能（查询引擎、工具系统）
│       ├── tools/         # 40+ 工具实现
│       ├── bridge/        # 通信和桥接系统
│       ├── utils/         # 工具函数
│       ├── services/      # 外部服务（API、MCP 等）
│       ├── types/         # 类型定义
│       └── commands/      # 斜杠命令
├── tests/                 # 测试套件
├── docs/                  # 文档
└── examples/              # 示例用法
```

## 核心组件

### 查询引擎 (QueryEngine)

衍智体的核心 - 处理查询并协调工具执行。

### 工具系统 (Tool System)

40+ 工具包括:
- 文件操作 (Read, Write, Edit, Glob, Grep)
- Shell 执行 (Bash, PowerShell)
- Git 操作
- 任务管理
- Web 操作 (Fetch, Search)
- 更多...

### 桥接系统 (Bridge System)

通信层支持:
- 远程控制
- 会话管理
- 事件传输

## 开发

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

## 配置

配置通过以下方式管理:
- 环境变量
- `.env` 文件
- 配置文件 (TOML/YAML)
- 命令行参数

详见 [配置指南](docs/configuration.md)。

## API 参考

完整 API 文档: [https://yanzhiti.github.io/yanzhiti](https://yanzhiti.github.io/yanzhiti)

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE)。

## 致谢

- Anthropic 原始 TypeScript 实现
- Python 社区的优秀库和工具

## 免责声明

这是一个独立的 Python 实现，与 Anthropic 没有官方关联或认可。

---

**衍智体** - 让 AI 助力您的编程之旅
