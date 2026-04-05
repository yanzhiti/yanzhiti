"""
Web UI 后端服务 - 衍智体 (YANZHITI)
Web Backend Server - FastAPI with full provider support

功能：
- 统一 AI 聊天接口（支持 17+ 供应商）
- 实时 WebSocket 流式输出
- 多模型选择和切换
- API Key 配置管理
- 会话管理和统计
"""

import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from yanzhiti import __version__
from yanzhiti.core.providers import (
    ProviderType,
    get_all_providers,
    get_cloud_providers,
    get_local_providers,
    get_provider,
    get_recommended_providers,
    search_models,
)

# 导入统一引擎和供应商系统 | Import unified engine and provider system
from yanzhiti.core.unified_engine import (
    BackendPriority,
    EngineConfig,
    UnifiedAIEngine,
)

# 配置日志 | Configure logging
logger = logging.getLogger(__name__)


# ============================================================
# 📦 Pydantic 数据模型 | Data Models
# ============================================================


class Message(BaseModel):
    """消息数据 | Message data"""

    role: str = "user"
    content: str = ""


class ChatRequest(BaseModel):
    """聊天请求 | Chat request"""

    message: str
    session_id: str | None = None
    provider: str | None = None  # 供应商 ID，如 "openrouter"、"ollama" 等
    model: str | None = None  # 模型名称
    temperature: float | None = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=4096, ge=1, le=32768)


class ChatResponse(BaseModel):
    """聊天响应 | Chat response"""

    response: str
    session_id: str
    provider: str = ""
    model: str = ""


class ProviderConfigRequest(BaseModel):
    """供应商配置请求 | Provider config request"""

    provider_id: str
    api_key: str | None = None
    base_url: str | None = None


class SettingsUpdate(BaseModel):
    """设置更新 | Settings update"""

    primary_backend: str | None = None
    priority: str | None = None  # "cloud", "local", "builtin", "auto"
    temperature: float | None = None
    max_tokens: int | None = None


# ============================================================
# 🚀 FastAPI 应用初始化 | App Initialization
# ============================================================

app = FastAPI(
    title="衍智体 (YANZHITI) Web UI",
    description="衍智体 Web 界面后端 - 支持 17+ AI 供应商",
    version=__version__,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS 中间件 - 允许前端跨域访问 | CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 🌐 全局状态管理 | Global State Management
# ============================================================

# 会话引擎缓存 | Session engine cache
engines: dict[str, UnifiedAIEngine] = {}

# API Key 存储（内存中，生产环境应使用加密存储）| API Key storage (in-memory)
api_keys: dict[str, str] = {}

# 全局默认设置 | Global default settings
global_settings = {
    "primary_backend": "openrouter",
    "priority": "auto",
    "temperature": 0.7,
    "max_tokens": 4096,
}


async def _get_or_create_engine(
    session_id: str,
    preferred_provider: str | None = None,
) -> UnifiedAIEngine:
    """
    获取或创建会话引擎 | Get or create session engine

    如果会话已存在则复用，否则创建新引擎并初始化。
    Reuse existing session or create a new engine.
    """
    if session_id in engines:
        return engines[session_id]

    # 构建引擎配置 | Build engine config
    config_kwargs = {
        "primary_backend": global_settings["primary_backend"],
        "priority": BackendPriority(global_settings.get("priority", "auto")),
        "temperature": global_settings.get("temperature", 0.7),
        "max_tokens": global_settings.get("max_tokens", 4096),
    }

    # 如果指定了供应商和 API Key | If provider and API key specified
    if preferred_provider:
        config_kwargs["primary_backend"] = preferred_provider
    if preferred_provider and preferred_provider in api_keys:
        config_kwargs["api_key"] = api_keys[preferred_provider]

    config = EngineConfig(**config_kwargs)
    engine = UnifiedAIEngine(config)
    await engine.initialize()
    engines[session_id] = engine
    return engine


# ============================================================
# 📡 API 路由 - 首页和静态文件 | Routes - Home & Static
# ============================================================


@app.get("/")
async def root():
    """提供主页面 | Serve main HTML page"""
    html_path = Path(__file__).parent / "static" / "index.html"
    if html_path.exists():
        return FileResponse(html_path)
    else:
        return HTMLResponse(content=_get_default_html())


@app.get("/health")
async def health_check():
    """健康检查端点 | Health check endpoint"""
    return {
        "status": "ok",
        "version": __version__,
        "active_sessions": len(engines),
        "providers_configured": len(api_keys),
    }


# ============================================================
# 🤖 API 路由 - 供应商管理 | Routes - Providers
# ============================================================


@app.get("/api/providers")
async def list_providers():
    """
    列出所有可用的 AI 供应商 | List all available AI providers

    返回 17+ 供应商的详细信息，包括云端、本地和内置类型。
    """
    providers_list = []
    for provider in get_all_providers():
        has_key = provider.name in api_keys and bool(api_keys[provider.name])
        providers_list.append(
            {
                "id": provider.name,
                "display_name": provider.display_name,
                "description": provider.description,
                "type": provider.provider_type.value,
                "has_free_tier": provider.has_free_tier,
                "recommended": provider.recommended,
                "configured": has_key or provider.provider_type != ProviderType.CLOUD,
                "model_count": len(provider.models),
                "features": provider.features,
                "signup_url": provider.signup_url,
            }
        )

    return {
        "total": len(providers_list),
        "cloud_count": len(get_cloud_providers()),
        "local_count": len(get_local_providers()),
        "providers": providers_list,
    }


@app.get("/api/providers/{provider_id}/models")
async def list_provider_models(provider_id: str):
    """
    列出指定供应商的所有模型 | List models for a specific provider
    """
    provider = get_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail=f"未找到供应商: {provider_id}")

    models_list = []
    for model in provider.models:
        models_list.append(
            {
                "name": model.name,
                "display_name": model.display_name,
                "description": model.description,
                "context_window": model.context_window,
                "max_output": model.max_output,
                "is_free": model.is_free,
                "requires_api_key": model.requires_api_key,
                "input_price": model.input_price,
                "output_price": model.output_price,
                "capabilities": model.capabilities,
            }
        )

    return {"provider": provider.display_name, "models": models_list}


@app.post("/api/providers/configure")
async def configure_provider(config: ProviderConfigRequest):
    """
    配置供应商的 API Key | Configure provider API key

    支持设置/更新/删除各供应商的密钥。
    """
    provider = get_provider(config.provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail=f"未找到供应商: {config.provider_id}")

    # 设置或清除 API Key | Set or clear API key
    if config.api_key is not None:
        api_keys[config.provider_id] = config.api_key
        logger.info(f"已配置供应商 {config.provider_id} 的 API Key")
    elif config.provider_id in api_keys:
        del api_keys[config.provider_id]
        logger.info(f"已清除供应商 {config.provider_id} 的 API Key")

    return {
        "status": "success",
        "provider": config.provider_id,
        "has_api_key": config.api_key is not None and len(config.api_key) > 0,
    }


@app.get("/api/search-models")
async def search_models_endpoint(q: str):
    """
    搜索模型 | Search models by keyword

    支持按名称、显示名、描述搜索所有供应商的模型。
    """
    results = search_models(q)
    matched = []
    for provider, model in results[:20]:  # 限制返回数量
        matched.append(
            {
                "provider_name": provider.name,
                "provider_display": provider.display_name,
                "model_name": model.name,
                "model_display": model.display_name,
                "is_free": model.is_free,
                "context_window": model.context_window,
            }
        )
    return {"query": q, "count": len(matched), "results": matched}


@app.get("/api/recommendations")
async def get_recommendations():
    """
    获取推荐给新手的供应商和模型 | Get recommended providers for beginners
    """
    recommended = []
    for provider in get_recommended_providers():
        models_info = []
        for model in provider.models[:2]:  # 只取前两个推荐模型
            models_info.append(
                {
                    "name": model.name,
                    "display_name": model.display_name,
                    "is_free": model.is_free,
                }
            )
        recommended.append(
            {
                "id": provider.name,
                "display_name": provider.display_name,
                "description": provider.description,
                "has_free_tier": provider.has_free_tier,
                "top_models": models_info,
            }
        )

    return {"recommended": recommended}


# ============================================================
# 💬 API 路由 - 聊天功能 | Routes - Chat
# ============================================================


@app.get("/api/models")
async def get_all_models():
    """
    获取所有可用模型列表 | Get all available models list

    整合所有供应商的模型信息，供前端下拉选择。
    """
    all_models = []
    for provider in get_all_providers():
        for model in provider.models:
            all_models.append(
                {
                    "id": f"{provider.name}/{model.name}",
                    "name": model.name,
                    "display_name": model.display_name,
                    "provider": provider.name,
                    "provider_type": provider.provider_type.value,
                    "description": model.description,
                    "is_free": model.is_free,
                    "context_window": model.context_window,
                    "max_output": model.max_output,
                    "capabilities": model.capabilities,
                }
            )

    # 按：推荐 > 免费 > 付费 排序 | Sort by: recommended > free > paid
    all_models.sort(
        key=lambda m: (
            0 if m["provider"] in ["openrouter", "groq", "google", "deepseek"] else 1,
            0 if m["is_free"] else 1,
        )
    )

    return {
        "total": len(all_models),
        "models": all_models,
    }


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    聊天接口 - 统一 AI 对话 | Chat endpoint - unified AI conversation

    支持指定供应商、模型、温度等参数，
    自动通过 UnifiedAIEngine 进行故障转移。
    """
    import uuid as uuid_mod

    # 生成或复用会话 ID | Generate or reuse session ID
    session_id = request.session_id or str(uuid_mod.uuid4())

    try:
        # 获取或创建引擎 | Get or create engine
        engine = await _get_or_create_engine(session_id, request.provider)

        # 如果指定了 API Key 且当前引擎未配置 | If API key specified but engine not configured
        if request.provider and request.provider in api_keys:
            engine.config.api_key = api_keys[request.provider]

        # 如果指定了模型 | If model specified
        if request.model:
            engine.config.model = request.model

        # 执行查询 | Execute query
        response_text = await engine.query(
            prompt=request.message,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            preferred_backend=request.provider,
        )

        return ChatResponse(
            response=response_text,
            session_id=session_id,
            provider=engine.config.primary_backend,
            model=engine.config.model or "",
        )

    except Exception as e:
        logger.error(f"聊天请求失败: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket 端点 - 实时流式对话 | WebSocket endpoint - real-time streaming chat

    支持流式输出、状态通知、错误处理。
    """
    await websocket.accept()

    # 创建引擎 | Create engine
    engine = await _get_or_create_engine(session_id)

    try:
        while True:
            # 接收消息 | Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)

            message = message_data.get("message", "")
            provider = message_data.get("provider")
            model = message_data.get("model")
            temperature = message_data.get("temperature", 0.7)
            max_tokens = message_data.get("max_tokens", 4096)

            if not message.strip():
                await websocket.send_json({"type": "error", "detail": "消息不能为空"})
                continue

            # 发送思考状态 | Send thinking status
            await websocket.send_json(
                {
                    "type": "status",
                    "status": "thinking",
                    "message": "正在思考中...",
                }
            )

            try:
                # 配置临时参数 | Configure temporary parameters
                if provider:
                    engine.config.primary_backend = provider
                if provider and provider in api_keys:
                    engine.config.api_key = api_keys[provider]
                if model:
                    engine.config.model = model

                # 使用流式查询 | Use streaming query
                full_response = ""
                async for chunk in engine.stream_query(
                    prompt=message,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    preferred_backend=provider,
                ):
                    full_response += chunk
                    # 发送文本块 | Send text chunk
                    await websocket.send_json(
                        {
                            "type": "chunk",
                            "content": chunk,
                        }
                    )

                # 发送完成信号 | Send completion signal
                await websocket.send_json(
                    {
                        "type": "complete",
                        "content": full_response,
                        "provider": engine.config.primary_backend,
                        "model": engine.config.model or "",
                    }
                )

            except Exception as e:
                logger.error(f"WebSocket 处理消息失败: {e}")
                await websocket.send_json(
                    {
                        "type": "error",
                        "detail": str(e),
                    }
                )

    except WebSocketDisconnect:
        # 清理会话资源 | Clean up session resources
        if session_id in engines:
            del engines[session_id]
        logger.info(f"会话 {session_id} 已断开")


# ============================================================
# 📊 API 路由 - 会话和统计 | Routes - Sessions & Stats
# ============================================================


@app.get("/api/sessions")
async def list_sessions():
    """列出活跃会话 | List active sessions"""
    sessions = []
    for sid, engine in engines.items():
        info = engine.get_info()
        sessions.append(
            {
                "id": sid,
                "primary_backend": info["config"]["primary_backend"],
                "model": info["config"]["model"],
                "backends": info["backends"],
            }
        )
    return {"sessions": sessions, "total": len(sessions)}


@app.get("/api/stats/{session_id}")
async def get_session_stats(session_id: str):
    """获取会话统计 | Get session statistics"""
    if session_id not in engines:
        raise HTTPException(status_code=404, detail="会话不存在")

    engine = engines[session_id]
    stats = engine.get_info()
    return stats


@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """删除会话 | Delete a session"""
    if session_id in engines:
        del engines[session_id]
        return {"status": "deleted", "session_id": session_id}
    raise HTTPException(status_code=404, detail="会话不存在")


# ============================================================
# ⚙️ API 路由 - 设置管理 | Routes - Settings
# ============================================================


@app.get("/api/settings")
async def get_settings():
    """获取全局设置 | Get global settings"""
    return {
        **global_settings,
        "configured_providers": list(api_keys.keys()),
        "version": __version__,
    }


@app.put("/api/settings")
async def update_settings(settings: SettingsUpdate):
    """更新全局设置 | Update global settings"""
    if settings.primary_backend is not None:
        provider = get_provider(settings.primary_backend)
        if provider:
            global_settings["primary_backend"] = settings.primary_backend
        else:
            raise HTTPException(status_code=400, detail=f"无效的供应商: {settings.primary_backend}")

    if settings.priority is not None:
        try:
            global_settings["priority"] = settings.priority
            BackendPriority(settings.priority)
        except ValueError:
            valid = [p.value for p in BackendPriority]
            raise HTTPException(
                status_code=400,
                detail=f"无效的优先级模式，可选值: {valid}",
            ) from None

    if settings.temperature is not None:
        global_settings["temperature"] = max(0.0, min(2.0, settings.temperature))

    if settings.max_tokens is not None:
        global_settings["max_tokens"] = max(1, min(32768, settings.max_tokens))

    logger.info(f"设置已更新: {global_settings}")
    return {"status": "success", "settings": global_settings}


# ============================================================
# 🔧 默认 HTML 页面 | Default HTML Fallback
# ============================================================


def _get_default_html() -> str:
    """
    当静态文件不存在时的备用页面 | Fallback page when static file missing
    """
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>衍智体 (YANZHITI)</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{
            font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
            background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
            height:100vh;display:flex;justify-content:center;align-items:center;
        }
        .container{
            background:#1a1a2e;border-radius:16px;box-shadow:0 25px 80px rgba(0,0,0,.5);
            width:92%;max-width:960px;height:88vh;display:flex;flex-direction:column;overflow:hidden;
        }
        .header{
            background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:24px;text-align:center;
        }
        .header h1{font-size:26px;font-weight:700}
        .header p{font-size:14px;opacity:.85;margin-top:6px}
        .chat-area{flex:1;overflow-y:auto;padding:24px;background:#16213e}
        .msg{margin-bottom:16px;display:flex;flex-direction:column}
        .msg.user{align-items:flex-end}.msg.assistant{align-items:flex-start}
        .bubble{
            max-width:75%;padding:14px 20px;border-radius:18px;word-break:break-word;line-height:1.5;
            font-size:15px;
        }
        .msg.user .bubble{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff}
        .msg.assistant .bubble{background:#0f3460;color:#e0e0e0;border:1px solid #1a1a40}
        .input-area{
            padding:20px;background:#1a1a2e;border-top:1px solid #2a2a4a;
            display:flex;gap:12px;align-items:flex-end;
        }
        .input-area textarea{
            flex:1;padding:14px 18px;border:2px solid #2a2a4a;border-radius:14px;
            background:#0f0c29;color:#fff;font-size:15px;resize:none;outline:none;
            transition:border-color .3s;height:auto;min-height:48px;max-height:150px;
        }
        .input-area textarea:focus{border-color:#667eea}
        .input-area button{
            padding:12px 28px;background:linear-gradient(135deg,#667eea,#764ba2);
            color:#fff;border:none;border-radius:14px;font-size:15px;font-weight:600;
            cursor:pointer;transition:transform .2s,box-shadow .2s;white-space:nowrap;
        }
        .input-area button:hover{transform:scale(1.05);box-shadow:0 8px 25px rgba(102,126,234,.4)}
        .status-bar{text-align:center;padding:10px;color:#888;font-size:13px}
        .code-block{background:#0d1117;border-radius:8px;padding:12px;margin:8px 0;
            font-family:'Cascadia Code','Fira Code',monospace;font-size:13px;overflow-x:auto;
        }
        pre{margin:0}code{color:#79c0ff}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🤖 衍智体 (YANZHITI)</h1>
        <p>支持 17+ AI 供应商 · 开箱即用 · 隐私优先</p>
    </div>
    <div class="chat-area" id="chat"></div>
    <div class="status-bar" id="status">就绪 - 选择模型开始对话</div>
    <div class="input-area">
        <textarea id="input" placeholder="输入你的问题..." rows="1"></textarea>
        <button onclick="send()">发送</button>
    </div>
</div>

<script>
const chat=document.getElementById('chat'),input=document.getElementById('input'),
      status=document.getElementById('status');
let sessionId=null;

input.addEventListener('input',()=>{ input.style.height='auto';input.style.height=Math.min(input.scrollHeight,150)+'px' });
input.addEventListener('keydown',(e)=>{ if(e.key==='Enter'&&!e.shiftKey){ e.preventDefault();send() } });

function addMsg(role,content){
    const div=document.createElement('div');div.className='msg '+role;
    const fmt=formatContent(content);
    div.innerHTML='<div class="bubble">'+fmt+'</div>';
    chat.appendChild(div);chat.scrollTop=chat.scrollHeight;
}

function formatContent(text){
    let h=text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    h=h.replace(/```(\\w*)\n?([\\s\\S]*?)```/g,'<pre class="code-block"><code>$2</code></pre>');
    h=h.replace(/`([^`]+)`/g,'<code>$1</code>');
    h=h.replace(/\n/g,'<br>');return h;
}

async function send(){
    const msg=input.value.trim();if(!msg)return;
    input.value='';input.style.height='auto';addMsg('user',msg);
    status.textContent='⏳ 思考中...';
    try{
        const res=await fetch('/api/chat',{method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({message:msg,session_id:sessionId})
        });
        const d=await res.json();sessionId=d.session_id;
        addMsg('assistant',d.response);status.textContent='';
    }catch(e){ status.textContent='❌ 错误: '+e.message }
}
</script>
</body></html>
"""


# ============================================================
# 📁 挂载静态文件 | Mount Static Files
# ============================================================

static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


# ============================================================
# 🏃 启动入口 | Entry Point
# ============================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("🤖 衍智体 (YANZHITI) Web UI 启动中...")
    print(f"📋 版本: {__version__}")
    print("🌐 地址: http://localhost:8000")
    print("📖 文档: http://localhost:8000/api/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
