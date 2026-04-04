"""
Web UI for 衍智体 (YANZHITI) Local
FastAPI backend with WebSocket support
"""

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from yanzhiti import __version__
from yanzhiti.core import ToolRegistry
from yanzhiti.core.local_query_engine import LocalQueryEngine, LocalQueryEngineConfig
from yanzhiti.tools import (
    APITestTool,
    BashTool,
    FileEditTool,
    FileReadTool,
    FileWriteTool,
    GitBranchTool,
    GitDiffTool,
    GitLogTool,
    GitStatusTool,
    GitTool,
    GlobTool,
    GrepTool,
    PowerShellTool,
    TaskCreateTool,
    TaskDeleteTool,
    TaskGetTool,
    TaskListTool,
    TaskTool,
    TaskUpdateTool,
    TodoWriteTool,
    WebFetchTool,
    WebScrapeTool,
    WebSearchTool,
)

# Create FastAPI app
app = FastAPI(
    title="衍智体 (YANZHITI) Local Web UI",
    description="Web interface for 衍智体 (YANZHITI) Local",
    version=__version__,
)


# Models
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


# Global state
engines = {}  # session_id -> LocalQueryEngine


def create_tool_registry() -> ToolRegistry:
    """Create tool registry"""
    registry = ToolRegistry()

    # File tools
    registry.register(FileReadTool())
    registry.register(FileWriteTool())
    registry.register(FileEditTool())
    registry.register(GlobTool())
    registry.register(GrepTool())

    # Shell tools
    registry.register(BashTool())
    registry.register(PowerShellTool())
    registry.register(TaskTool())

    # Web tools
    registry.register(WebFetchTool())
    registry.register(WebSearchTool())
    registry.register(WebScrapeTool())
    registry.register(APITestTool())

    # Git tools
    registry.register(GitTool())
    registry.register(GitStatusTool())
    registry.register(GitDiffTool())
    registry.register(GitLogTool())
    registry.register(GitBranchTool())

    # Task tools
    registry.register(TaskCreateTool())
    registry.register(TaskListTool())
    registry.register(TaskGetTool())
    registry.register(TaskUpdateTool())
    registry.register(TaskDeleteTool())
    registry.register(TodoWriteTool())

    return registry


def create_engine(session_id: str, backend: str = "lm_studio") -> LocalQueryEngine:
    """Create a new query engine for a session"""
    tool_registry = create_tool_registry()

    config = LocalQueryEngineConfig(
        cwd=".",
        backend=backend,
        tools=tool_registry.list_tools(),
    )

    engine = LocalQueryEngine(config)
    engines[session_id] = engine
    return engine


# API routes
@app.get("/")
async def root():
    """Serve the main HTML page"""
    html_path = Path(__file__).parent / "static" / "index.html"
    if html_path.exists():
        return FileResponse(html_path)
    else:
        return HTMLResponse(content=get_default_html())


@app.get("/api/models")
async def get_models():
    """Get available models from LM Studio"""
    from yanzhiti.core.lm_studio_client import LMStudioClient

    client = LMStudioClient()
    try:
        models = await client.get_models()
        await client.close()
        return {"models": models}
    except Exception as e:
        await client.close()
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat endpoint"""
    import uuid

    session_id = request.session_id or str(uuid.uuid4())

    # Get or create engine
    engine = create_engine(session_id) if session_id not in engines else engines[session_id]

    # Process message
    try:
        response = await engine.query(request.message)
        return ChatResponse(
            response=response.content,
            session_id=session_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()

    # Create engine for this session
    engine = create_engine(session_id) if session_id not in engines else engines[session_id]

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Process message
            message = message_data.get("message", "")

            # Send status
            await websocket.send_json({
                "type": "status",
                "status": "thinking",
            })

            # Get response
            response = await engine.query(message)

            # Send response
            await websocket.send_json({
                "type": "response",
                "content": response.content,
            })

    except WebSocketDisconnect:
        # Clean up
        if session_id in engines:
            del engines[session_id]


@app.get("/api/stats/{session_id}")
async def get_stats(session_id: str):
    """Get session statistics"""
    if session_id not in engines:
        raise HTTPException(status_code=404, detail="Session not found")

    engine = engines[session_id]
    stats = engine.get_stats()
    return stats


@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    if session_id in engines:
        del engines[session_id]
        return {"status": "deleted"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")


def get_default_html() -> str:
    """Get default HTML if static file not found"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>衍智体 (YANZHITI) Local</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 90%;
            max-width: 900px;
            height: 85vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 { font-size: 24px; margin-bottom: 5px; }
        .header p { font-size: 14px; opacity: 0.9; }
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
        }
        .message.user { align-items: flex-end; }
        .message.assistant { align-items: flex-start; }
        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .message.assistant .message-content {
            background: white;
            color: #333;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        .input-container input {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #eee;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        .input-container input:focus {
            border-color: #667eea;
        }
        .input-container button {
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .input-container button:hover {
            transform: scale(1.05);
        }
        .status {
            text-align: center;
            padding: 10px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 衍智体 (YANZHITI) Local</h1>
            <p>Powered by LM Studio - Running on your Mac</p>
        </div>
        <div class="chat-container" id="chat"></div>
        <div class="status" id="status"></div>
        <div class="input-container">
            <input type="text" id="input" placeholder="Type your message..." autofocus>
            <button onclick="send()">Send</button>
        </div>
    </div>

    <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('input');
        const status = document.getElementById('status');
        let sessionId = null;

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') send();
        });

        function addMessage(role, content) {
            const msg = document.createElement('div');
            msg.className = `message ${role}`;
            msg.innerHTML = `<div class="message-content">${content}</div>`;
            chat.appendChild(msg);
            chat.scrollTop = chat.scrollHeight;
        }

        async function send() {
            const message = input.value.trim();
            if (!message) return;

            input.value = '';
            addMessage('user', message);
            status.textContent = '⏳ Thinking...';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message, session_id: sessionId})
                });

                const data = await response.json();
                sessionId = data.session_id;

                addMessage('assistant', data.response);
                status.textContent = '';
            } catch (error) {
                status.textContent = '❌ Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
"""


# Mount static files if they exist
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
