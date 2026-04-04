# 贡献指南 | Contributing to 衍智体 (YANZHITI)

感谢您对衍智体项目的关注！我们欢迎各种形式的贡献。

## 📋 目录 | Contents

- [行为准则](#-行为准则-code-of-conduct)
- [如何贡献](#-如何贡献-how-to-contribute)
- [开发环境搭建](#-开发环境-setup)
- [代码规范](#-代码规范-code-style)
- [提交规范](#-提交规范-commit-guidelines)
- [Pull Request 流程](#-pull-request-流程)
- [测试要求](#-测试要求-testing)

---

## 🤝 行为准则 | Code of Conduct

- **尊重他人** - 保持礼貌和建设性的讨论
- **包容开放** - 欢迎不同背景的贡献者
- **专注技术** - 讨论聚焦于代码和功能本身
- **遵守许可** - 所有贡献遵循项目开源协议

## 🚀 如何贡献 | How to Contribute

### 贡献方式

| 类型 | 说明 |
|------|------|
| 🐛 Bug 报告 | 发现问题请提 Issue，尽量提供复现步骤 |
| 💡 功能建议 | 新功能想法请先提 Issue 讨论 |
| 🔧 代码贡献 | 修复 Bug 或实现新功能（见下方流程） |
| 📖 文档改进 | 中英文文档、示例、教程等 |
| 🌐 国际化 | 多语言翻译支持 |

### 不适合的情况

- 纯粹的 UI 偏好调整
- 与项目目标不符的功能
- 未经过讨论的大型重构

---

## 🛠️ 开发环境 | Setup

### 前置要求

```bash
# Python 版本 | Python version
Python >= 3.10 (推荐 3.11+)

# 依赖管理 | Dependencies
pip install -e ".[dev]"
```

### 克隆和安装

```bash
# 克隆仓库 | Clone repository
git clone https://github.com/yanzhiti/yanzhiti.git
cd yanzhiti

# 创建虚拟环境 | Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖 | Install dependencies
pip install -e ".[dev]"

# 验证安装 | Verify installation
yzt --version
```

### 项目结构概览

```
yanzhiti/
├── src/yanzhiti/          # 核心源码
│   ├── core/              # 核心引擎、供应商系统
│   │   ├── providers.py   # AI 供应商配置 (17+)
│   │   ├── unified_engine.py  # 统一 AI 引擎
│   │   └── builtin_models.py  # 内置模型管理
│   ├── web/               # Web GUI
│   │   ├── server.py      # FastAPI 后端
│   │   └── static/        # 前端静态文件
│   ├── cli/               # 命令行工具
│   └── tools/             # 工具集
├── tests/                 # 测试文件
├── docs/                  # 文档
└── pyproject.toml         # 项目配置
```

---

## ✍️ 代码规范 | Code Style

### Python 规范

```bash
# 自动格式化 | Auto-format
ruff format src/ tests/

# Lint 检查 | Lint check
ruff check src/ tests/

# 类型检查 | Type checking
mypy src/yanzhiti/
```

**关键规则**:
- 遵循 PEP 8
- 使用 Ruff 格式化器
- 行宽: 100 字符
- 所有函数必须有 docstring
- 注释使用中文 + 英文双语

### JavaScript/CSS 规范

- 使用 2 空格缩进
- CSS 变量统一在 `:root` 定义
- 函数命名使用 camelCase
- 类名使用 kebab-case

---

## 📝 提交规范 | Commit Guidelines

### Commit Message 格式

```
<类型> (<范围>): <描述>

[可选的正文]

[可选的脚注]
```

### 类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat (providers): 添加 Groq 供应商` |
| `fix` | Bug 修复 | `fix (server): 修复 WebSocket 断连问题` |
| `docs` | 文档更新 | `docs (readme): 更新安装指南` |
| `style` | 代码格式 | `style: 统一 import 排序` |
| `refactor` | 重构 | `refactor (engine): 简化 failover 逻辑` |
| `test` | 测试相关 | `test (core): 添加供应商单元测试` |
| `chore` | 构建/工具 | `chore: 更新 CI 配置` |

---

## 🔀 Pull Request 流程

### PR 步骤

1. **Fork 并克隆**
   ```bash
   git clone https://github.com/<your-username>/yanzhiti.git
   ```

2. **创建特性分支**
   ```bash
   git checkout -b feature/你的功能名
   ```

3. **编写代码并测试**
   ```bash
   ruff check src/ --fix
   ruff format src/
   pytest tests/ -v
   ```

4. **提交并推送**
   ```bash
   git commit -m "feat (scope): 你的改动"
   git push origin feature/你的功能名
   ```

5. **创建 PR** - 在 GitHub 上创建 Pull Request

### PR 模板

```markdown
## 改动类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档改进
- [ ] 其他: _____

## 改动描述
简要描述你的改动内容和原因。

## 测试情况
- [ ] 已运行 `pytest tests/`
- [ ] 已通过 `ruff check` 检查
- [ ] 已通过 `ruff format` 格式化

## 相关 Issue
Closes #(Issue 编号)
```

---

## 🧪 测试要求 | Testing

### 运行测试

```bash
# 全部测试 | All tests
pytest tests/ -v

# 覆盖率报告 | Coverage report
pytest tests/ --cov=src/yanzhiti --cov-report=html

# 单个模块 | Single module
pytest tests/test_core.py -v
```

### 新功能必须包含测试

- 核心功能: 单元测试覆盖率 > 80%
- API 端点: 至少包含正常和异常两种场景
- 工具类: 包含边界条件测试

---

## 💡 建议 | Tips for Contributors

1. **先看 Issue** - 在动手前查看是否有类似的工作在进行
2. **小步快跑** - 每个 PR 尽量保持专注和精简
3. **写好文档** - 公开的 API 和复杂逻辑需要注释
4. **关注性能** - 注意异步操作和资源释放
5. **多语言友好** - UI 文本考虑国际化

---

## 📞 联系方式 | Contact

- **Issue**: [GitHub Issues](https://github.com/yanzhiti/yanzhiti/issues)
- **讨论**: [GitHub Discussions](https://github.com/yanzhiti/yanzhiti/discussions)

---

**感谢您为衍智体做出贡献！🎉**

*每个贡献者都会被记录在 [CONTRIBUTORS.md](CONTRIBUTORS.md) 中。*
