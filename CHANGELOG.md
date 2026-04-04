# 📝 变更日志 | Changelog

所有重要的项目变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
项目遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added - 新增
- 配置向导 CLI (`yzt --setup`)
- 错误诊断工具 (`yzt --diagnose`)
- 多语言支持框架 (`--lang` 选项)
- 国际化 README (中英双语)
- 快速入门指南
- 打包发布指南
- PyInstaller 打包配置

### Changed - 变更
- 改进 README 文档结构和内容
- 增强 CLI 命令选项
- 优化错误提示信息

### Fixed - 修复
- API 连接测试逻辑
- 配置文件加载问题

---

## [1.0.0] - 2024-04-04

### Added - 新增
- 核心查询引擎
- 40+ 开发工具集
  - 文件操作工具 (Read, Write, Edit, Glob, Grep)
  - Shell 执行工具 (Bash, PowerShell)
  - Git 管理工具 (Status, Diff, Log, Branch)
  - Web 操作工具 (Fetch, Search, Scrape, API Test)
  - 任务管理工具
- 交互式 CLI 界面
- Web 界面支持
- MCP 协议支持
- 权限控制系统
- 会话管理
- 基础文档

### Changed - 变更
- 支持 OpenRouter API
- 优化 Anthropic SDK 集成

---

## 版本说明 | Version Notes

### [Unreleased]
- 专注于降低使用门槛
- 提升用户体验
- 完善文档和工具链

### [1.0.0]
- 初始发布版本
- 核心功能实现
- 基础 CLI 和 Web 界面

---

## 提交规范 | Commit Guidelines

我们遵循以下提交规范:

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

示例:
```
feat (setup): 添加配置向导功能

- 实现交互式配置向导
- 支持 5 大 AI 提供商
- 自动测试 API 连接
```

---

**目标：GitHub TOP10 ⭐**
