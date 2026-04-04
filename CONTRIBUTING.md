# 🤝 贡献指南 | Contributing Guide

首先，感谢您对衍智体 (YANZHITI) 感兴趣！我们欢迎各种形式的贡献。

本文档将帮助您了解如何参与项目开发。

---

## 📋 目录

1. [行为准则](#行为准则)
2. [贡献方式](#贡献方式)
3. [开发环境设置](#开发环境设置)
4. [提交流程](#提交流程)
5. [代码规范](#代码规范)
6. [测试](#测试)
7. [文档](#文档)
8. [常见问题](#常见问题)

---

## 行为准则

本项目遵循 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。

**我们的承诺**:
- 营造开放、友好的环境
- 尊重不同观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

**不可接受的行为**:
- 使用性化的语言或图像
- 人身攻击或侮辱性评论
- 公开或私下骚扰
- 未经许可发布他人信息
- 其他不道德或不专业的行为

---

## 贡献方式

### 1. 报告 Bug 🐛

发现 Bug? 请提交 Issue:

1. 使用 GitHub Issue 模板
2. 填写详细信息:
   - 复现步骤
   - 预期行为
   - 实际行为
   - 环境信息 (OS, Python 版本等)
   - 截图 (如有)

### 2. 提出建议 💡

有新功能想法？请提交 Issue:

1. 使用 Feature Request 模板
2. 详细描述:
   - 功能用途
   - 使用场景
   - 实现思路 (可选)

### 3. 提交代码 🔀

**首次贡献**:

1. Fork 项目
2. Clone 到本地
   ```bash
   git clone https://github.com/your-username/yanzhiti.git
   cd yanzhiti
   ```
3. 创建分支
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. 开发并测试
5. 提交更改
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```
6. 推送到分支
   ```bash
   git push origin feature/amazing-feature
   ```
7. 创建 Pull Request

**代码审查流程**:
1. 自动检查 (CI/CD)
2. 维护者审查
3. 反馈修改
4. 合并到主分支

### 4. 改进文档 📖

文档同样重要！欢迎:

- 修正拼写/语法错误
- 改进说明清晰度
- 添加示例代码
- 翻译文档 (多语言支持)

### 5. 帮助他人 💬

在以下方面提供帮助:

- 回答 Issue 中的问题
- 分享使用经验
- 创建教程和示例

---

## 开发环境设置

### 1. 克隆项目

```bash
git clone https://github.com/yanzhiti/yanzhiti.git
cd yanzhiti
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
# 安装开发依赖
pip install -e ".[dev]"
```

### 4. 配置 API

```bash
# 运行配置向导
yzt --setup

# 或手动创建 .env 文件
cat > .env << EOF
YANZHITI_API_KEY=your-api-key
YANZHITI_BASE_URL=https://openrouter.ai/api/v1
YANZHITI_MODEL=openai/gpt-3.5-turbo
EOF
```

### 5. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_tools.py

# 查看测试覆盖率
pytest --cov=src/yanzhiti --cov-report=html
```

---

## 提交流程

### Git 工作流

1. **分支命名**
   - `feature/xxx` - 新功能
   - `fix/xxx` - Bug 修复
   - `docs/xxx` - 文档更新
   - `refactor/xxx` - 重构

2. **提交信息格式**

   ```
   <类型> (<范围>): <描述>
   
   [可选的正文]
   
   [可选的脚注]
   ```

   **类型说明**:
   - `feat`: 新功能
   - `fix`: Bug 修复
   - `docs`: 文档更新
   - `style`: 代码格式
   - `refactor`: 重构
   - `test`: 测试
   - `chore`: 构建/工具

   **示例**:
   ```
   feat (setup): 添加配置向导功能
   
   - 实现交互式配置向导
   - 支持 5 大 AI 提供商
   - 自动测试 API 连接
   
   Closes #123
   ```

3. **Pull Request 流程**
   - 填写 PR 模板
   - 关联 Issue
   - 等待 CI 通过
   - 响应审查意见
   - 合并代码

---

## 代码规范

### Python 代码风格

遵循 [PEP 8](https://pep8.org/) 规范:

1. **命名规范**
   ```python
   # 变量和函数：小写 + 下划线
   def my_function():
       pass
   
   # 类：大驼峰
   class MyClass:
       pass
   
   # 常量：全大写 + 下划线
   MAX_VALUE = 100
   ```

2. **注释要求**
   ```python
   def calculate_sum(a, b):
       """
       计算两个数的和
       
       Args:
           a: 第一个数
           b: 第二个数
           
       Returns:
           两数之和
       """
       return a + b
   ```

3. **代码格式化**
   ```bash
   # 使用 Black 格式化
   black src tests
   
   # 使用 Ruff 检查
   ruff check src tests
   ```

### 工具配置

项目已配置以下工具:

- **Black** - 代码格式化
- **Ruff** - 代码检查
- **Mypy** - 类型检查
- **Pytest** - 测试框架

---

## 测试

### 运行测试

```bash
# 所有测试
pytest

# 特定文件
pytest tests/test_tools.py

# 特定函数
pytest tests/test_tools.py::test_file_read

# 带覆盖率
pytest --cov=src/yanzhiti
```

### 编写测试

测试文件命名：`test_*.py`

```python
def test_example():
    """测试示例"""
    assert 1 + 1 == 2
```

### 测试要求

- 核心功能覆盖率 >80%
- 包含正常和异常情况
- 测试独立，无副作用

---

## 文档

### 文档结构

```
docs/
├── README.md          # 主文档
├── QUICKSTART.md      # 快速入门
├── BUILDING.md        # 打包指南
├── IMPLEMENTATION_SUMMARY.md  # 实施总结
└── TOP10_IMPROVEMENT_PLAN.md  # 改进计划
```

### 文档规范

1. **中英双语** - 重要文档提供双语版本
2. **清晰简洁** - 避免冗长
3. **包含示例** - 代码示例帮助理解
4. **格式统一** - 遵循 Markdown 规范

---

## 常见问题

### Q: 如何开始第一次贡献？
**A**: 从简单的任务开始，比如:
- 修正文档拼写错误
- 添加注释
- 修复简单的 Bug

查看 [Good First Issues](https://github.com/yanzhiti/yanzhiti/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

### Q: 提交后多久能得到反馈？
**A**: 通常在 24 小时内。如果超过 48 小时，请礼貌地提醒。

### Q: 可以同时提交多个 PR 吗？
**A**: 可以，但建议先完成一个再开始下一个。

### Q: 需要签署 CLA 吗？
**A**: 不需要。提交代码即表示您同意项目使用您的贡献。

---

## 🎯 项目目标

**我们的目标：成为 GitHub 上 Star 数前 10 的开源项目！**

每个贡献都在帮助我们更接近这个目标。

---

## 📞 联系方式

- 💬 GitHub Discussions
- 📧 Email: contact@yanzhiti.com
- 🐦 Twitter: @yanzhiti (Coming Soon)

---

## 🙏 致谢

感谢所有为项目做出贡献的开发者！

特别感谢:
- 核心贡献者
- 文档翻译者
- Bug 报告者
- 社区帮助者

---

<div align="center">

**衍智体 (YANZHITI)** - 让 AI 助力您的编程之旅

[开始贡献](#贡献方式) | [查看 Issue](https://github.com/yanzhiti/yanzhiti/issues) | [加入讨论](https://github.com/yanzhiti/yanzhiti/discussions)

⭐ [Star 项目](https://github.com/yanzhiti/yanzhiti/stargazers)

</div>
