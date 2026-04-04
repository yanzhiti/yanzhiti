# 🔌 API 集成示例 | API Integration Examples

本目录包含与各种 API 服务集成的使用示例。

---

## 📚 示例列表

### 1. OpenAI API 集成
调用 OpenAI 的 GPT 模型进行文本生成。

**使用命令**:
```
帮我写一个调用 OpenAI API 的函数，实现文本摘要功能
```

**功能**:
- 文本生成
- 代码补全
- 文本嵌入
- 图像生成（DALL-E）

### 2. GitHub API 集成
操作 GitHub 仓库和资源。

**使用命令**:
```
编写脚本获取 GitHub 仓库的 Star 历史
```

**支持操作**:
- 仓库管理
- Issue 和 PR 操作
- Release 发布
- Actions 触发

### 3. 数据库 API
与云数据库服务交互。

**使用命令**:
```
连接 Supabase，实现用户 CRUD 操作
```

**支持服务**:
- Supabase
- Firebase
- AWS DynamoDB
- MongoDB Atlas

### 4. 支付集成
集成支付网关处理支付。

**使用命令**:
```
实现 Stripe 支付流程，包括订阅和一次性付款
```

**支持平台**:
- Stripe
- PayPal
- 微信支付
- 支付宝

---

## 💡 使用技巧

### 1. RESTful API 调用
```
# GET 请求
"调用 GitHub API 获取用户信息"

# POST 请求
"发送数据到 Webhook URL"
```

### 2. 认证处理
```
# API Key 认证
"使用 Bearer Token 认证调用 API"

# OAuth 2.0
"实现 OAuth 2.0 授权流程"
```

### 3. 错误处理
```
# 重试机制
"添加指数退避重试逻辑"

# 速率限制
"处理 API 速率限制 (429 错误)"
```

---

## 🔧 相关工具

衍智体提供以下 API 相关工具：

| 工具名称 | 功能描述 |
|---------|---------|
| `api_test` | 测试 API 接口 |
| `web_fetch` | 获取 HTTP 响应 |
| `bash` | 执行 curl 命令 |
| `file_write` | 保存响应数据 |

---

## 📖 代码模板

### HTTP 客户端封装

```python
"""
通用 API 客户端 - 封装常用的 HTTP 操作
"""

import httpx
from typing import Any

class APIClient:
    """API 客户端基类"""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        timeout: int = 30
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    def _get_headers(self) -> dict[str, str]:
        """构建请求头"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """GET 请求"""
        response = await self.client.get(
            f"{self.base_url}/{endpoint}",
            headers=self._get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()

    async def post(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """POST 请求"""
        response = await self.client.post(
            f"{self.base_url}/{endpoint}",
            headers=self._get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
```

### GitHub API 示例

```python
"""
GitHub API 集成 - 仓库管理
"""

class GitHubClient(APIClient):
    """GitHub API 客户端"""

    def __init__(self, token: str):
        super().__init__(
            base_url="https://api.github.com",
            api_key=token
        )

    async def get_repo(self, owner: str, repo: str) -> dict:
        """获取仓库信息"""
        return await self.get(f"repos/{owner}/{repo}")

    async def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str
    ) -> dict:
        """创建 Issue"""
        return await self.post(
            f"repos/{owner}/{repo}/issues",
            data={"title": title, "body": body}
        )

    async def list_commits(
        self,
        owner: str,
        repo: str,
        per_page: int = 10
    ) -> list[dict]:
        """获取提交历史"""
        result = await self.get(
            f"repos/{owner}/{repo}/commits",
            params={"per_page": per_page}
        )
        return result
```

### Stripe 支付示例

```python
"""
Stripe 支付集成 - 处理付款和订阅
"""

import stripe

class PaymentService:
    """支付服务"""

    def __init__(self, secret_key: str):
        stripe.api_key = secret_key

    async def create_payment_intent(
        self,
        amount: int,
        currency: str = "usd"
    ) -> stripe.PaymentIntent:
        """创建支付意图"""
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency
        )
        return intent

    async def create_customer(
        self,
        email: str,
        name: str
    ) -> stripe.Customer:
        """创建客户"""
        customer = stripe.Customer.create(
            email=email,
            name=name
        )
        return customer

    async def create_subscription(
        self,
        customer_id: str,
        price_id: str
    ) -> stripe.Subscription:
        """创建订阅"""
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}]
        )
        return subscription
```

---

## 🎯 实战案例

### 案例 1: 构建 AI 应用

```bash
# 步骤 1: API 配置
yzt "创建配置文件管理多个 API 密钥"

# 步骤 2: 核心功能
yzt "实现 AI 文本生成函数，支持流式输出"

# 步骤 3: 用户界面
yzt "创建简单的 Web 界面调用 AI 功能"

# 步骤 4: 部署
yzt "编写 Dockerfile 和部署文档"
```

### 案例 2: SaaS 平台集成

```bash
# 步骤 1: 用户认证
yzt "实现 OAuth 登录（GitHub/Google）"

# 步骤 2: 支付系统
yzt "集成 Stripe 处理订阅付款"

# 步骤 3: 数据存储
yzt "连接 PostgreSQL 存储用户数据"

# 步骤 4: 通知服务
yzt "集成 SendGrid 发送邮件通知"
```

---

## ⚠️ 最佳实践

### 安全建议
- ✅ 使用环境变量存储密钥
- ✅ 实现 API 密钥轮换机制
- ✅ 限制 API 权限范围
- ✅ 加密敏感数据传输
- ✅ 定期审计 API 使用情况

### 性能优化
- 使用连接池管理 HTTP 连接
- 实现请求缓存减少重复调用
- 批量处理提高效率
- 异步并发提升吞吐量

### 监控日志
- 记录所有 API 请求和响应
- 监控响应时间和错误率
- 设置告警阈值
- 定期分析使用模式

---

**继续探索更多示例！**

[返回上级](../README.md) | [自动化脚本](../automation/README.md) | [Web 开发](../web_development/README.md)
