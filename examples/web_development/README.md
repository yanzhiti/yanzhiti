# 🌐 Web 开发示例 | Web Development Examples

本目录包含 Web 开发相关的使用示例。

---

## 📚 示例列表

### 1. Flask REST API 示例
创建一个简单的 RESTful API 服务。

**使用命令**:
```
帮我创建一个 Flask REST API，包含用户 CRUD 操作
```

**预期输出**: 完整的 Flask 应用代码，包括：
- 用户模型定义
- 路由和视图函数
- 请求验证
- 错误处理
- API 文档

### 2. FastAPI 异步服务
创建高性能的异步 Web 服务。

**使用命令**:
```
用 FastAPI 创建一个异步任务队列服务
```

**特性**:
- 异步请求处理
- WebSocket 支持
- 后台任务管理
- 自动生成 OpenAPI 文档

### 3. 网页爬虫示例
爬取网页数据并存储。

**使用命令**:
```
编写一个爬虫，抓取 GitHub Trending 页面的项目信息
```

**功能**:
- HTTP 请求处理
- HTML 解析
- 数据提取
- 存储到 JSON/数据库

### 4. 前端页面生成
生成 HTML/CSS/JavaScript 代码。

**使用命令**:
```
创建一个响应式的登录页面，包含表单验证
```

**包含**:
- HTML5 结构
- CSS3 样式（响应式）
- JavaScript 表单验证
- 现代化 UI 设计

---

## 💡 使用技巧

### 1. 指定框架
```
# 使用 Django 框架
"用 Django 创建一个博客系统"

# 使用 Express (Node.js)
"用 Express 创建 REST API"
```

### 2. 添加特定功能
```
# 包含认证功能
"创建带 JWT 认证的 API"

# 包含数据库
"创建用户管理系统，使用 PostgreSQL"
```

### 3. 性能优化
```
# 要求高性能
"创建高并发的 WebSocket 服务器"

# 缓存支持
"实现 Redis 缓存的 API"
```

---

## 🔧 相关工具

衍智体提供以下 Web 开发相关工具：

| 工具名称 | 功能描述 |
|---------|---------|
| `web_fetch` | 获取网页内容 |
| `web_search` | 网络搜索 |
| `web_scrape` | 网页数据抓取 |
| `api_test` | API 接口测试 |

---

## 📖 最佳实践

### 代码结构
```
project/
├── app/
│   ├── __init__.py
│   ├── models/        # 数据模型
│   ├── routes/        # 路由定义
│   ├── services/      # 业务逻辑
│   └── utils/         # 工具函数
├── tests/             # 测试文件
├── config.py          # 配置文件
└── requirements.txt   # 依赖列表
```

### 安全建议
- ✅ 输入验证和清理
- ✅ SQL 注入防护
- ✅ XSS 攻击防护
- ✅ CSRF 保护
- ✅ HTTPS 强制使用

### 性能优化
- 使用异步框架（FastAPI, asyncio）
- 数据库连接池
- Redis 缓存
- CDN 静态资源
- Gzip 压缩

---

## 🎯 实战案例

### 案例 1: 创建完整的 Web 应用

```bash
# 步骤 1: 项目初始化
yzt "创建项目结构，包括 app, tests, docs 目录"

# 步骤 2: 数据库模型
yzt "创建 User 和 Post 模型，包含字段定义"

# 步骤 3: API 路由
yzt "实现用户注册、登录、获取信息的 API"

# 步骤 4: 测试代码
yzt "为 API 编写单元测试"
```

### 案例 2: 微服务架构

```bash
# 用户服务
yzt "创建用户微服务，包含认证功能"

# 订单服务
yzt "创建订单微服务，与用户服务通信"

# API 网关
yzt "创建 API 网关，路由到不同服务"
```

---

**继续探索更多示例！**

[返回上级](../README.md) | [代码生成](../code_generation/README.md) | [Git 集成](../git_integration/README.md)
