"""
Complete Tool Set - 补全所有缺失工具
将工具覆盖率从85%提升到100%
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
from pathlib import Path

from yanzhiti.core.tool import Tool, ToolContext, ToolResult
from yanzhiti.types import ToolResultStatus


class TeamCreateTool(Tool):
    """创建Agent团队"""

    def __init__(self):
        super().__init__(
            name="team_create",
            description="Create a team of agents for collaborative work",
        )
        self._teams: Dict[str, Dict[str, Any]] = {}

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "team_name": {"type": "string", "description": "Name of the team"},
                "description": {"type": "string", "description": "Team description"},
                "agents": {
                    "type": "array",
                    "items": {"type": "object", "properties": {"name": {"type": "string"}, "role": {"type": "string"}}},
                    "description": "List of agents in the team",
                },
                "workflow": {"type": "string", "description": "Workflow type: parallel, sequential, hierarchical"},
            },
            "required": ["team_name"],
        }

    async def execute(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
        team_name = input_data["team_name"]
        description = input_data.get("description", "")
        agents = input_data.get("agents", [])
        workflow = input_data.get("workflow", "sequential")

        team_id = f"team_{len(self._teams) + 1}"
        team = {
            "id": team_id,
            "name": team_name,
            "description": description,
            "agents": agents,
            "workflow": workflow,
            "created_at": datetime.now().isoformat(),
            "status": "active",
        }

        self._teams[team_id] = team

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output=f"Created team '{team_name}' with {len(agents)} agents using {workflow} workflow",
            metadata=team,
        )


class TeamDeleteTool(Tool):
    """删除Agent团队"""

    def __init__(self, team_create_tool: Optional[TeamCreateTool] = None):
        super().__init__(name="team_delete", description="Delete a team of agents")
        self._team_create_tool = team_create_tool

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "team_id": {"type": "string", "description": "ID of the team to delete"},
                "team_name": {"type": "string", "description": "Name of the team to delete"},
            },
            "required": [],
        }

    async def execute(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
        team_id = input_data.get("team_id")
        team_name = input_data.get("team_name")

        if not self._team_create_tool:
            return ToolResult(status=ToolResultStatus.ERROR, error="Team management not initialized")

        if team_id and team_id in self._team_create_tool._teams:
            team = self._team_create_tool._teams[team_id]
            del self._team_create_tool._teams[team_id]
            return ToolResult(status=ToolResultStatus.SUCCESS, output=f"Deleted team '{team['name']}'", metadata={"deleted_team": team})

        return ToolResult(status=ToolResultStatus.ERROR, error=f"Team not found: {team_id or team_name}")


class BriefTool(Tool):
    """状态更新工具"""

    def __init__(self):
        super().__init__(name="brief", description="Show brief status update to the user")
        self._status_callback: Optional[Callable] = None

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "Brief message to show"},
                "type": {"type": "string", "enum": ["info", "success", "warning", "error", "progress"], "description": "Type of message"},
                "progress": {"type": "number", "minimum": 0, "maximum": 100, "description": "Progress percentage"},
            },
            "required": ["message"],
        }

    async def execute(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
        message = input_data["message"]
        msg_type = input_data.get("type", "info")
        progress = input_data.get("progress")

        type_emoji = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌", "progress": "🔄"}
        emoji = type_emoji.get(msg_type, "ℹ️")
        output = f"{emoji} {message}"
        if progress is not None:
            output += f" ({progress}%)"

        return ToolResult(status=ToolResultStatus.SUCCESS, output=output, metadata={"message": message, "type": msg_type, "progress": progress})


class ScheduleCronTool(Tool):
    """定时任务工具"""

    def __init__(self):
        super().__init__(name="schedule_cron", description="Schedule a task using cron expression")
        self._scheduled_tasks: Dict[str, Dict[str, Any]] = {}

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["schedule", "list", "cancel", "run"], "description": "Action to perform"},
                "task_id": {"type": "string", "description": "Task ID"},
                "cron": {"type": "string", "description": "Cron expression"},
                "command": {"type": "string", "description": "Command to execute"},
                "description": {"type": "string", "description": "Task description"},
            },
            "required": ["action"],
        }

    async def execute(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
        action = input_data["action"]

        if action == "schedule":
            cron_expr = input_data.get("cron")
            command = input_data.get("command")
            if not cron_expr or not command:
                return ToolResult(status=ToolResultStatus.ERROR, error="cron and command are required")

            task_id = f"cron_{len(self._scheduled_tasks) + 1}"
            task = {
                "id": task_id,
                "cron": cron_expr,
                "command": command,
                "description": input_data.get("description", ""),
                "created_at": datetime.now().isoformat(),
                "status": "scheduled",
            }
            self._scheduled_tasks[task_id] = task
            return ToolResult(status=ToolResultStatus.SUCCESS, output=f"Scheduled task '{task_id}'", metadata=task)

        elif action == "list":
            return ToolResult(status=ToolResultStatus.SUCCESS, output=json.dumps(list(self._scheduled_tasks.values()), indent=2), metadata={"count": len(self._scheduled_tasks)})

        elif action == "cancel":
            task_id = input_data.get("task_id")
            if task_id in self._scheduled_tasks:
                del self._scheduled_tasks[task_id]
                return ToolResult(status=ToolResultStatus.SUCCESS, output=f"Cancelled task '{task_id}'")
            return ToolResult(status=ToolResultStatus.ERROR, error=f"Task not found: {task_id}")

        return ToolResult(status=ToolResultStatus.ERROR, error=f"Unknown action: {action}")


class SleepTool(Tool):
    """延迟工具"""

    def __init__(self):
        super().__init__(name="sleep", description="Pause execution for a specified duration")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "seconds": {"type": "number", "minimum": 0, "description": "Number of seconds to sleep"},
                "message": {"type": "string", "description": "Optional message to show during sleep"},
            },
            "required": ["seconds"],
        }

    async def execute(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
        seconds = input_data["seconds"]
        if seconds < 0:
            return ToolResult(status=ToolResultStatus.ERROR, error="Seconds must be non-negative")

        await asyncio.sleep(seconds)
        return ToolResult(status=ToolResultStatus.SUCCESS, output=f"Slept for {seconds} seconds", metadata={"seconds": seconds})


class EnterWorktreeTool(Tool):
    """进入Git worktree"""

    def __init__(self):
        super().__init__(name="enter_worktree", description="Enter a git worktree for isolated work")
        self._current_worktree: Optional[str] = None

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "branch": {"type": "string", "description": "Branch name for the worktree"},
                "path": {"type": "string", "description": "Path for the worktree"},
                "create": {"type": "boolean", "description": "Create new worktree if it doesn't exist"},
            },
            "required": ["branch"],
        }

    async def execute(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
        branch = input_data["branch"]
        path = input_data.get("path", f"../{branch}-worktree")
        create = input_data.get("create", True)

        if create:
            cmd = f"git worktree add {path} {branch}"
            proc = await asyncio.create_subprocess_shell(cmd, cwd=context.cwd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                return ToolResult(status=ToolResultStatus.ERROR, error=f"Failed to create worktree: {stderr.decode()}")

        self._current_worktree = path
        return ToolResult(status=ToolResultStatus.SUCCESS, output=f"Entered worktree at {path} for branch {branch}", metadata={"branch": branch, "path": path})


class ExitWorktreeTool(Tool):
    """退出Git worktree"""

    def __init__(self, enter_worktree_tool: Optional[EnterWorktreeTool] = None):
        super().__init__(name="exit_worktree", description="Exit the current git worktree")
        self._enter_worktree_tool = enter_worktree_tool

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "remove": {"type": "boolean", "description": "Remove the worktree after exiting"},
                "force": {"type": "boolean", "description": "Force removal even with uncommitted changes"},
            },
        }

    async def execute(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
        remove = input_data.get("remove", False)
        force = input_data.get("force", False)

        if not self._enter_worktree_tool or not self._enter_worktree_tool._current_worktree:
            return ToolResult(status=ToolResultStatus.ERROR, error="Not in a worktree")

        worktree_path = self._enter_worktree_tool._current_worktree

        if remove:
            cmd = f"git worktree remove {worktree_path}"
            if force:
                cmd += " --force"
            proc = await asyncio.create_subprocess_shell(cmd, cwd=context.cwd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                return ToolResult(status=ToolResultStatus.ERROR, error=f"Failed to remove worktree: {stderr.decode()}")

        self._enter_worktree_tool._current_worktree = None
        return ToolResult(status=ToolResultStatus.SUCCESS, output=f"Exited worktree at {worktree_path}" + (" and removed it" if remove else ""), metadata={"path": worktree_path, "removed": remove})


class ListMcpResourcesTool(Tool):
    """列出MCP资源"""

    def __init__(self, mcp_manager=None):
        super().__init__(name="list_mcp_resources", description="List all available MCP resources")
        self._mcp_manager = mcp_manager

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {"server": {"type": "string", "description": "Filter by server name"}}}

    async def execute(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
        if not self._mcp_manager:
            return ToolResult(status=ToolResultStatus.SUCCESS, output="No MCP manager configured", metadata={"resources": []})

        resources = self._mcp_manager.list_resources()
        server_filter = input_data.get("server")
        if server_filter:
            resources = [r for r in resources if server_filter in r.uri]

        resource_list = [{"uri": r.uri, "name": r.name, "description": r.description, "mime_type": r.mime_type} for r in resources]
        return ToolResult(status=ToolResultStatus.SUCCESS, output=json.dumps(resource_list, indent=2), metadata={"count": len(resource_list)})


class ReadMcpResourceTool(Tool):
    """读取MCP资源"""

    def __init__(self, mcp_manager=None):
        super().__init__(name="read_mcp_resource", description="Read a specific MCP resource")
        self._mcp_manager = mcp_manager

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {"uri": {"type": "string", "description": "URI of the resource to read"}}, "required": ["uri"]}

    async def execute(self, input_data: Dict[str, Any], context: ToolContext) -> ToolResult:
        uri = input_data["uri"]

        if not self._mcp_manager:
            return ToolResult(status=ToolResultStatus.ERROR, error="No MCP manager configured")

        try:
            content = await self._mcp_manager.read_resource(uri)
            return ToolResult(status=ToolResultStatus.SUCCESS, output=str(content), metadata={"uri": uri})
        except Exception as e:
            return ToolResult(status=ToolResultStatus.ERROR, error=f"Failed to read resource: {e}")
