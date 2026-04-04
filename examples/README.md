# 📚 示例库 | Examples

本目录包含衍智体 (YANZHITI) 的各种使用示例，帮助你快速上手。

---

## 📋 目录 | Table of Contents

### 🔰 基础示例 | Basic Examples

1. **[代码生成](code_generation/README.md)** 💻
   - 快速排序实现
   - REST API 客户端
   - 数据处理脚本
   - 算法和数据结构

2. **[文件操作](file_operations/README.md)** 📁
   - 批量文件重命名
   - 文件内容搜索
   - 目录结构分析
   - 日志文件处理

3. **[Git 集成](git_integration/README.md)** 🔄
   - 自动提交工作流
   - 分支管理策略
   - 代码审查辅助
   - Release 发布流程

### 🚀 进阶示例 | Advanced Examples

4. **[Web 开发](web_development/README.md)** 🌐
   - Flask/FastAPI 应用
   - RESTful API 设计
   - 网页爬虫开发
   - 前端页面生成
   - 微服务架构

5. **[数据处理](data_processing/README.md)** 📊
   - CSV/Excel 处理
   - JSON 数据操作
   - 数据库查询
   - 数据可视化
   - 统计分析报告

6. **[自动化脚本](automation/README.md)** ⚡
   - 文件批量处理
   - 系统监控脚本
   - 定时任务管理
   - 邮件通知服务
   - 部署自动化

7. **[API 集成](api_integration/README.md)** 🔌
   - OpenAI API 调用
   - GitHub API 操作
   - 云数据库连接
   - 支付系统集成
   - 第三方服务对接

---

## 🎯 按使用场景分类 | By Use Case

### 🏢 企业级应用
- [Web 开发](web_development/README.md) - 构建企业应用
- [API 集成](api_integration/README.md) - 连接外部服务
- [数据处理](data_processing/README.md) - 业务数据分析

### 🛠️ 开发工具
- [代码生成](code_generation/README.md) - 快速生成代码
- [Git 集成](git_integration/README.md) - 版本控制自动化
- [文件操作](file_operations/README.md) - 项目文件管理

### 🤖 自动化运维
- [自动化脚本](automation/README.md) - 运维任务自动化
- [API 集成](api_integration/README.md) - 服务监控告警
- [数据处理](data_processing/README.md) - 日志分析处理

---

## 🚀 快速开始 | Quick Start

### 运行现有示例

```bash
# 进入示例目录
cd examples/code_generation

# 查看可用示例
ls

# 运行示例 (如适用)
python quick_sort.py
```

### 使用衍智体生成新示例

```bash
# 启动衍智体交互模式
yzt

# 或使用单次命令模式
yzt "帮我写一个 Python 脚本，批量重命名文件"
```

### 浏览所有示例

```bash
# 显示示例库
yzt --examples
```

---

## 📖 示例格式说明 | Example Format

每个示例目录都包含:

```
example_category/
├── README.md          # 详细说明文档
├── example_1.py       # 示例代码（可选）
├── example_2.py       # 更多示例（可选）
└── assets/            # 相关资源（可选）
```

### 标准内容

每个示例的 README 都包含：

- ✅ **功能描述** - 这个示例做什么
- ✅ **使用场景** - 什么时候用
- ✅ **完整代码** - 可直接运行的代码
- ✅ **详细注释** - 中文注释解释每一步
- ✅ **扩展建议** - 如何改进和定制
- ✅ **最佳实践** - 专业开发建议
- ✅ **常见问题** - FAQ 和故障排除

---

## 💡 使用技巧 | Tips & Tricks

### 1. 组合使用多个工具

```bash
# 示例：完整的 Web 应用开发流程
yzt "创建项目结构"           # 文件操作
yzt "生成 Flask 应用代码"     # 代码生成
yzt "编写单元测试"           # Git 集成测试
yzt "创建 Docker 配置"      # 自动化部署
```

### 2. 利用上下文

```bash
# 告诉衍智体你的具体需求
"我正在开发一个电商网站，帮我设计用户认证模块"

# 提供更多背景信息
"这是一个 Django 项目，数据库使用 PostgreSQL..."
```

### 3. 迭代改进

```bash
# 第一版：基本功能
"创建一个用户登录页面"

# 第二版：添加验证
"在登录页面添加表单验证和错误提示"

# 第三版：完善体验
"添加记住密码、忘记密码功能"
```

---

## 🎨 自定义示例 | Create Your Own

欢迎提交你自己的使用示例！

### 提交指南

1. **Fork 项目**
   ```bash
   git clone https://github.com/yanzhiti/yanzhiti.git
   ```

2. **创建示例目录**
   ```bash
   mkdir examples/my_example
   cd my_example
   ```

3. **编写示例**

   创建 `README.md`：
   ```markdown
   # 我的示例名称

   ## 功能描述
   这个示例展示...

   ## 使用方法
   ```bash
   yzt "你的提示词"
   ```

   ## 代码示例
   ```python
   # 你的代码
   ```

   ## 扩展建议
   - 建议 1
   - 建议 2
   ```

4. **提交 PR**
   ```bash
   git add .
   git commit -m "feat: 添加我的示例"
   git push origin my-feature
   # 然后在 GitHub 创建 Pull Request
   ```

### 示例质量标准

好的示例应该：

- ✅ **实用性强** - 解决真实问题
- ✅ **代码清晰** - 易于理解和修改
- ✅ **文档完整** - 包含详细说明
- ✅ **可独立运行** - 不依赖复杂环境
- ✅ **有教育价值** - 能帮助他人学习

---

## 📊 示例统计

| 类别 | 示例数量 | 难度等级 |
|------|---------|---------|
| 代码生成 | 3+ | ⭐⭐ |
| 文件操作 | 3+ | ⭐⭐ |
| Git 集成 | 3+ | ⭐⭐⭐ |
| Web 开发 | 5+ | ⭐⭐⭐⭐ |
| 数据处理 | 4+ | ⭐⭐⭐ |
| 自动化脚本 | 4+ | ⭐⭐⭐⭐ |
| API 集成 | 4+ | ⭐⭐⭐⭐⭐ |

**总计**: 25+ 个实用示例

---

## 🤝 贡献者 | Contributors

感谢所有贡献示例的开发者！

- 👤 贡献者 1 - 代码生成示例
- 👤 贡献者 2 - Web 开发示例
- 👤 贡献者 3 - 自动化脚本示例
- *(等待你的贡献！)*

---

## 📞 需要帮助？| Need Help?

- 📖 [快速入门指南](../docs/QUICKSTART.md)
- 📘 [完整文档](../docs/)
- 🐛 [报告问题](https://github.com/yanzhiti/yanzhiti/issues)
- 💬 [社区讨论](https://github.com/yanzhiti/yanzhiti/discussions)
- 📧 [联系我们](mailto:contact@yanzhiti.com)

---

<div align="center">

**🌟 如果这些示例对你有帮助，请给项目一个 Star！🌟**

[Star 项目](https://github.com/yanzhiti/yanzhiti/stargazers)

**衍智体 (YANZHITI)** - 让 AI 助力您的编程之旅

</div>
