# 📞 支持指南 | Support

感谢使用衍智体 (YANZHITI)! 本文档将帮助您获得所需的支持。

---

## 📋 目录

1. [获取帮助](#获取帮助)
2. [问题报告](#问题报告)
3. [功能请求](#功能请求)
4. [社区支持](#社区支持)
5. [商业支持](#商业支持)
6. [资源](#资源)

---

## 获取帮助

### 快速帮助

遇到问题？按以下顺序寻求帮助:

1. **查看文档** 📖
   - [快速入门指南](docs/QUICKSTART.md)
   - [完整文档](docs/README.md)
   - [常见问题](#常见问题)

2. **运行诊断** 🩺
   ```bash
   yzt --diagnose
   yzt --diagnose --auto-fix
   ```

3. **搜索 Issue** 🔍
   - [GitHub Issues](https://github.com/yanzhiti/yanzhiti/issues)
   - [GitHub Discussions](https://github.com/yanzhiti/yanzhiti/discussions)

4. **提问** 💬
   - 创建 Issue
   - 加入 Discussions
   - 联系社区

---

## 问题报告

### Bug 报告

发现 Bug? 请创建 Issue 并提供:

**必需信息**:
- 📝 问题描述
- 🔄 复现步骤
- ✅ 预期行为
- ❌ 实际行为
- 💻 环境信息 (OS, Python 版本等)

**可选但有帮助**:
- 📸 截图或录屏
- 📄 日志文件
- 🔧 修复建议

**Bug 报告模板**:
```markdown
### 问题描述
简要描述问题

### 复现步骤
1. 执行...
2. 然后...
3. 出现...

### 预期行为
应该发生什么

### 实际行为
实际发生了什么

### 环境信息
- OS: Windows 11
- Python: 3.10.0
- YANZHITI: 1.0.0

### 日志
```
[粘贴相关日志]
```

### 截图
(如有)
```

### 配置问题

配置相关问题的快速排查:

1. **检查 .env 文件**
   ```bash
   # 文件是否存在
   ls -la .env  # macOS/Linux
   dir .env     # Windows
   
   # 内容是否正确
   cat .env     # macOS/Linux
   type .env    # Windows
   ```

2. **验证 API 连接**
   ```bash
   yzt --diagnose
   ```

3. **重新配置**
   ```bash
   yzt --setup
   ```

---

## 功能请求

有新功能想法？我们很乐意听取！

### 提交功能请求

1. **检查现有请求**
   - 搜索是否已有类似请求
   - 避免重复

2. **创建 Issue**
   - 使用 Feature Request 模板
   - 详细描述使用场景
   - 说明预期效果

**功能请求模板**:
```markdown
### 功能描述
简要描述想要的功能

### 使用场景
这个功能能解决什么问题？
谁会用这个功能？

### 预期效果
功能应该如何工作？

### 实现思路 (可选)
如何实现这个功能？

### 替代方案 (可选)
有没有其他解决方案？

### 附加信息
截图、示例等
```

### 投票和支持

看到感兴趣的功能请求？

- 👍 给 Issue 点赞表示支持
- 💬 评论提供反馈
- 🔄 分享让更多人看到

---

## 社区支持

### 讨论区

[GitHub Discussions](https://github.com/yanzhiti/yanzhiti/discussions) 是提问和分享的好地方:

**适合讨论的话题**:
- 💡 使用技巧分享
- 🎓 学习心得
- 📚 教程和指南
- 💬 一般性问题
- 📢 项目公告

### 提问的艺术

提出好问题能获得更好的答案:

1. **先搜索** - 避免重复问题
2. **描述清晰** - 提供足够上下文
3. **展示尝试** - 说明已做的努力
4. **提供示例** - 代码、配置、日志
5. **保持礼貌** - 尊重他人时间

### 帮助他人

有经验？欢迎帮助其他用户:

- 回答 Discussions 中的问题
- 分享使用技巧
- 编写教程
- 改进文档

---

## 商业支持

需要企业级支持？我们提供:

### 支持套餐

#### 基础支持 (免费)
- ✅ GitHub Issue 支持
- ✅ 社区帮助
- ✅ 文档访问
- ⏱️ 响应时间：48 小时

#### 优先支持 (即将推出)
- ✅ 所有基础支持功能
- ✅ 优先 Issue 处理
- ✅ 邮件支持
- ⏱️ 响应时间：24 小时
- 💰 费用：待定

#### 企业支持 (即将推出)
- ✅ 所有优先支持功能
- ✅ 专属技术支持
- ✅ 定制开发
- ✅ 培训服务
- ⏱️ 响应时间：4 小时
- 💰 费用：定制

**联系**: contact@yanzhiti.com

---

## 资源

### 文档

- 📖 [快速入门](docs/QUICKSTART.md)
- 📚 [完整文档](docs/README.md)
- 🔧 [工具列表](docs/tools.md)
- ❓ [常见问题](#常见问题)
- 📦 [打包指南](docs/BUILDING.md)

### 常见问题

#### 安装问题

**Q: 安装失败怎么办？**

A: 
1. 检查 Python 版本 (需要 3.10+)
2. 使用虚拟环境
3. 查看完整错误信息
4. 运行 `yzt --diagnose`

**Q: 命令找不到？**

A:
1. 确认已激活虚拟环境
2. 检查 PATH 设置
3. 使用 `python -m yanzhiti.cli.main`

#### 配置问题

**Q: API 密钥无效？**

A:
1. 检查密钥是否正确复制
2. 确认 API 服务商
3. 查看账户余额/配额
4. 测试连接：`yzt --diagnose`

**Q: 如何切换模型？**

A:
1. 运行 `yzt --setup` 重新配置
2. 或手动修改 `.env` 中的 `YANZHITI_MODEL`

#### 使用问题

**Q: 如何退出交互式模式？**

A:
- 输入 `/exit` 或 `/quit`
- 或按 `Ctrl+C`

**Q: 支持哪些 AI 模型？**

A:
- OpenRouter (推荐) - 100+ 模型
- OpenAI - GPT-4, GPT-3.5
- Anthropic - Claude 系列
- DeepSeek - 免费模型
- Ollama - 本地模型

**Q: 数据是否安全？**

A:
- 代码本地运行
- 不上传源代码
- 仅发送必要的 API 请求
- 可配置本地模型

### 外部资源

- 🎓 [Python 教程](https://docs.python.org/3/tutorial/)
- 📖 [Git 指南](https://git-scm.com/book)
- 🛠️ [开发工具](https://code.visualstudio.com/)

---

## 联系方式

### 社区渠道

- 💬 [GitHub Discussions](https://github.com/yanzhiti/yanzhiti/discussions)
- 🐛 [GitHub Issues](https://github.com/yanzhiti/yanzhiti/issues)
- 📧 Email: contact@yanzhiti.com

### 社交媒体 (即将推出)

- 🐦 Twitter: @yanzhiti
- 💼 LinkedIn: YANZHITI
- 📱 Discord 社区

### 工作时间

- 🕐 标准支持：周一至周五，9:00-18:00 (UTC+8)
- ⚡ 紧急支持：仅限企业用户

---

## 贡献支持

想要帮助改进支持？

- 📖 改进文档
- 💬 回答社区问题
- 🌍 翻译文档
- 🎓 编写教程

每个贡献都很珍贵！

---

<div align="center">

**衍智体 (YANZHITI)** - 让 AI 助力您的编程之旅

[开始使用](README.md) | [获取帮助](#获取帮助) | [报告问题](https://github.com/yanzhiti/yanzhiti/issues)

⭐ [Star 项目](https://github.com/yanzhiti/yanzhiti/stargazers)

</div>
