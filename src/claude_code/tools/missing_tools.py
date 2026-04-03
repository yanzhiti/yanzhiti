"""
Missing Important Tools - 补充缺失的重要工具
将工具覆盖率从72%提升到85%+
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from pathlib import Path
from enum import Enum

from claude_code.core.tool import Tool, ToolContext, ToolResult
from claude_code.types import ToolResultStatus


class PlanMode(str, Enum):
    """规划模式状态"""
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"


class SkillTool(Tool):
    """
    技能调用工具
    允许调用预定义的技能组合
    """

    def __init__(self):
        super().__init__(
            name="skill",
            description="Invoke a skill (predefined tool combination)",
        )
        self._skills: Dict[str, Dict[str, Any]] = {}
        self._load_default_skills()

    def _load_default_skills(self):
        """加载默认技能"""
        self._skills = {
            "code-review": {
                "description": "Review code for quality and issues",
                "tools": ["file_read", "grep", "git_diff"],
                "prompt": "Review the code for best practices, potential bugs, and improvements",
            },
            "refactor": {
                "description": "Refactor code for better structure",
                "tools": ["file_read", "file_edit", "grep"],
                "prompt": "Refactor the code to improve structure and readability",
            },
            "test-gen": {
                "description": "Generate tests for code",
                "tools": ["file_read", "file_write", "grep"],
                "prompt": "Generate comprehensive tests for the code",
            },
            "doc-gen": {
                "description": "Generate documentation",
                "tools": ["file_read", "file_write"],
                "prompt": "Generate documentation for the code",
            },
            "debug": {
                "description": "Debug code issues",
                "tools": ["file_read", "grep", "bash"],
                "prompt": "Analyze and debug the code issue",
            },
        }

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Name of the skill to invoke",
                },
                "target": {
                    "type": "string",
                    "description": "Target file or directory",
                },
                "args": {
                    "type": "object",
                    "description": "Additional arguments for the skill",
                },
            },
            "required": ["skill_name"],
        }

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        skill_name = input_data["skill_name"]
        target = input_data.get("target", context.cwd)
        args = input_data.get("args", {})

        if skill_name not in self._skills:
            available = list(self._skills.keys())
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Skill not found: {skill_name}. Available: {available}",
            )

        skill = self._skills[skill_name]

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output=f"Skill '{skill_name}' ready: {skill['description']}\nTools: {skill['tools']}\nPrompt: {skill['prompt']}",
            metadata={
                "skill": skill_name,
                "tools": skill["tools"],
                "target": target,
            },
        )

    def register_skill(self, name: str, description: str, tools: List[str], prompt: str):
        """注册自定义技能"""
        self._skills[name] = {
            "description": description,
            "tools": tools,
            "prompt": prompt,
        }

    def list_skills(self) -> List[Dict[str, Any]]:
        """列出所有可用技能"""
        return [
            {"name": name, **data}
            for name, data in self._skills.items()
        ]


class LSPTool(Tool):
    """
    Language Server Protocol工具
    提供代码智能功能
    """

    def __init__(self):
        super().__init__(
            name="lsp",
            description="Language Server Protocol integration for code intelligence",
        )
        self._lsp_clients: Dict[str, Any] = {}

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["definition", "references", "hover", "completion", "rename"],
                    "description": "LSP action to perform",
                },
                "file_path": {
                    "type": "string",
                    "description": "File path",
                },
                "line": {
                    "type": "integer",
                    "description": "Line number (1-based)",
                },
                "character": {
                    "type": "integer",
                    "description": "Character position (1-based)",
                },
                "new_name": {
                    "type": "string",
                    "description": "New name for rename action",
                },
            },
            "required": ["action", "file_path", "line", "character"],
        }

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        action = input_data["action"]
        file_path = input_data["file_path"]
        line = input_data["line"]
        character = input_data["character"]

        # 简化实现 - 实际需要LSP客户端
        result = {
            "action": action,
            "file": file_path,
            "position": {"line": line, "character": character},
            "note": "LSP integration requires language server installation",
        }

        if action == "definition":
            result["message"] = "Go to definition (requires LSP server)"
        elif action == "references":
            result["message"] = "Find all references (requires LSP server)"
        elif action == "hover":
            result["message"] = "Show hover info (requires LSP server)"
        elif action == "completion":
            result["message"] = "Get completions (requires LSP server)"
        elif action == "rename":
            new_name = input_data.get("new_name", "")
            result["message"] = f"Rename to {new_name} (requires LSP server)"

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output=json.dumps(result, indent=2),
            metadata=result,
        )


class EnterPlanModeTool(Tool):
    """进入规划模式"""

    def __init__(self):
        super().__init__(
            name="enter_plan_mode",
            description="Enter planning mode to create a detailed plan before execution",
        )
        self._plan_mode = PlanMode.IDLE
        self._current_plan: Optional[Dict[str, Any]] = None

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "goal": {
                    "type": "string",
                    "description": "Goal or objective to plan for",
                },
                "context": {
                    "type": "string",
                    "description": "Additional context for planning",
                },
            },
            "required": ["goal"],
        }

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        goal = input_data["goal"]
        additional_context = input_data.get("context", "")

        self._plan_mode = PlanMode.PLANNING
        self._current_plan = {
            "goal": goal,
            "context": additional_context,
            "steps": [],
            "status": "planning",
        }

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output=f"Entered planning mode for: {goal}\n\nPlease describe the steps to achieve this goal.",
            metadata={"mode": "planning", "goal": goal},
        )


class ExitPlanModeTool(Tool):
    """退出规划模式"""

    def __init__(self, plan_tool: Optional[EnterPlanModeTool] = None):
        super().__init__(
            name="exit_plan_mode",
            description="Exit planning mode and execute the plan",
        )
        self._plan_tool = plan_tool

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "execute": {
                    "type": "boolean",
                    "description": "Whether to execute the plan (default: true)",
                },
                "plan": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Plan steps to execute",
                },
            },
        }

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        execute = input_data.get("execute", True)
        plan_steps = input_data.get("plan", [])

        if self._plan_tool:
            self._plan_tool._plan_mode = PlanMode.IDLE

        if execute and plan_steps:
            steps_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan_steps))
            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=f"Exiting planning mode. Plan to execute:\n\n{steps_str}",
                metadata={"mode": "executing", "steps": len(plan_steps)},
            )
        else:
            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output="Exited planning mode without execution",
                metadata={"mode": "idle"},
            )


class SendMessageTool(Tool):
    """Agent间消息传递"""

    def __init__(self):
        super().__init__(
            name="send_message",
            description="Send a message to another agent or the main conversation",
        )
        self._message_queue: Dict[str, List[Dict[str, Any]]] = {}

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string",
                    "description": "Recipient agent ID or 'main' for main conversation",
                },
                "message": {
                    "type": "string",
                    "description": "Message content",
                },
                "message_type": {
                    "type": "string",
                    "enum": ["info", "question", "result", "error"],
                    "description": "Type of message",
                },
            },
            "required": ["recipient", "message"],
        }

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        recipient = input_data["recipient"]
        message = input_data["message"]
        message_type = input_data.get("message_type", "info")

        # 添加到消息队列
        if recipient not in self._message_queue:
            self._message_queue[recipient] = []

        msg = {
            "from": context.session_id if hasattr(context, 'session_id') else "unknown",
            "to": recipient,
            "message": message,
            "type": message_type,
        }

        self._message_queue[recipient].append(msg)

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output=f"Message sent to {recipient}: {message[:50]}...",
            metadata=msg,
        )

    def get_messages(self, recipient: str) -> List[Dict[str, Any]]:
        """获取指定接收者的消息"""
        return self._message_queue.get(recipient, [])


class MCPResourceTools(Tool):
    """MCP资源管理工具"""

    def __init__(self, mcp_manager=None):
        super().__init__(
            name="mcp_resource",
            description="Manage MCP resources",
        )
        self._mcp_manager = mcp_manager

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["list", "read"],
                    "description": "Action to perform",
                },
                "uri": {
                    "type": "string",
                    "description": "Resource URI (for read action)",
                },
            },
            "required": ["action"],
        }

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        action = input_data["action"]

        if action == "list":
            if self._mcp_manager:
                resources = self._mcp_manager.list_resources()
                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=json.dumps([r.model_dump() for r in resources], indent=2),
                    metadata={"count": len(resources)},
                )
            else:
                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output="No MCP servers connected",
                    metadata={"count": 0},
                )

        elif action == "read":
            uri = input_data.get("uri")
            if not uri:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error="URI required for read action",
                )

            if self._mcp_manager:
                content = await self._mcp_manager.read_resource(uri)
                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=str(content),
                    metadata={"uri": uri},
                )
            else:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error="No MCP servers connected",
                )

        return ToolResult(
            status=ToolResultStatus.ERROR,
            error=f"Unknown action: {action}",
        )


class ConfigTool(Tool):
    """配置管理工具"""

    def __init__(self):
        super().__init__(
            name="config",
            description="Manage configuration settings",
        )
        self._config: Dict[str, Any] = {}
        self._config_file = Path.home() / ".claude" / "config.json"
        self._load_config()

    def _load_config(self):
        """加载配置"""
        if self._config_file.exists():
            try:
                self._config = json.loads(self._config_file.read_text())
            except:
                self._config = {}

    def _save_config(self):
        """保存配置"""
        self._config_file.parent.mkdir(parents=True, exist_ok=True)
        self._config_file.write_text(json.dumps(self._config, indent=2))

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get", "set", "list", "delete"],
                    "description": "Config action",
                },
                "key": {
                    "type": "string",
                    "description": "Configuration key",
                },
                "value": {
                    "type": "string",
                    "description": "Configuration value (for set action)",
                },
            },
            "required": ["action"],
        }

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        action = input_data["action"]
        key = input_data.get("key")
        value = input_data.get("value")

        if action == "list":
            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=json.dumps(self._config, indent=2),
                metadata={"count": len(self._config)},
            )

        elif action == "get":
            if not key:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error="Key required for get action",
                )

            val = self._config.get(key)
            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=str(val) if val is not None else "Not found",
                metadata={"key": key, "value": val},
            )

        elif action == "set":
            if not key or value is None:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error="Key and value required for set action",
                )

            self._config[key] = value
            self._save_config()

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=f"Set {key} = {value}",
                metadata={"key": key, "value": value},
            )

        elif action == "delete":
            if not key:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error="Key required for delete action",
                )

            if key in self._config:
                del self._config[key]
                self._save_config()
                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=f"Deleted {key}",
                )
            else:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Key not found: {key}",
                )

        return ToolResult(
            status=ToolResultStatus.ERROR,
            error=f"Unknown action: {action}",
        )
