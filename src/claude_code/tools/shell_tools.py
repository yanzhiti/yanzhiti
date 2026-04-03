"""
Shell execution tools
"""

import asyncio
import os
import subprocess
from typing import Any, Dict, Optional

from claude_code.core.tool import Tool, ToolContext, ToolInputSchema, ToolResult
from claude_code.types import PermissionResult, ToolResultStatus


class BashTool(Tool):
    """Tool for executing shell commands"""

    def __init__(self):
        super().__init__(
            name="bash",
            description="Execute a bash shell command",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "command": {
                    "type": "string",
                    "description": "The bash command to execute",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in milliseconds (default: 120000)",
                },
                "cwd": {
                    "type": "string",
                    "description": "Working directory for command execution",
                },
            },
            required=["command"],
        )

    async def check_permission(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> PermissionResult:
        # TODO: Implement proper permission checks
        # Check against allowed commands, dangerous patterns, etc.
        return PermissionResult(granted=True)

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        command = input_data["command"]
        timeout = input_data.get("timeout", 120000) / 1000  # Convert to seconds
        cwd = input_data.get("cwd", context.cwd)

        try:
            # Execute command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                process.kill()
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Command timed out after {timeout} seconds",
                )

            output = []
            if stdout:
                output.append(f"stdout:\n{stdout.decode('utf-8', errors='replace')}")
            if stderr:
                output.append(f"stderr:\n{stderr.decode('utf-8', errors='replace')}")

            output.append(f"exit code: {process.returncode}")

            return ToolResult(
                status=ToolResultStatus.SUCCESS if process.returncode == 0 else ToolResultStatus.ERROR,
                output="\n".join(output),
                metadata={
                    "command": command,
                    "exit_code": process.returncode,
                    "timeout": timeout,
                },
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error executing command: {str(e)}",
            )


class PowerShellTool(Tool):
    """Tool for executing PowerShell commands (Windows)"""

    def __init__(self):
        super().__init__(
            name="powershell",
            description="Execute a PowerShell command (Windows only)",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "command": {
                    "type": "string",
                    "description": "The PowerShell command to execute",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in milliseconds",
                },
            },
            required=["command"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        if os.name != "nt":
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error="PowerShell is only available on Windows",
            )

        command = input_data["command"]
        timeout = input_data.get("timeout", 120000) / 1000

        try:
            process = await asyncio.create_subprocess_exec(
                "powershell",
                "-Command",
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=context.cwd,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                process.kill()
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Command timed out after {timeout} seconds",
                )

            output = []
            if stdout:
                output.append(stdout.decode("utf-8", errors="replace"))
            if stderr:
                output.append(stderr.decode("utf-8", errors="replace"))

            return ToolResult(
                status=ToolResultStatus.SUCCESS if process.returncode == 0 else ToolResultStatus.ERROR,
                output="\n".join(output),
                metadata={"command": command, "exit_code": process.returncode},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error executing PowerShell command: {str(e)}",
            )


class TaskTool(Tool):
    """Tool for managing async tasks"""

    def __init__(self):
        super().__init__(
            name="task",
            description="Create and manage background tasks",
        )
        self._tasks: Dict[str, asyncio.Task] = {}

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "action": {
                    "type": "string",
                    "enum": ["create", "list", "stop", "output"],
                    "description": "Task action to perform",
                },
                "task_id": {
                    "type": "string",
                    "description": "Task ID for stop/output actions",
                },
                "command": {
                    "type": "string",
                    "description": "Command to run for create action",
                },
            },
            required=["action"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        action = input_data["action"]

        if action == "create":
            command = input_data.get("command")
            if not command:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error="Command required for create action",
                )

            # Create background task
            task_id = f"task_{len(self._tasks) + 1}"

            async def run_command():
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=context.cwd,
                )
                stdout, stderr = await process.communicate()
                return {
                    "stdout": stdout.decode("utf-8", errors="replace"),
                    "stderr": stderr.decode("utf-8", errors="replace"),
                    "exit_code": process.returncode,
                }

            task = asyncio.create_task(run_command())
            self._tasks[task_id] = task

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=f"Created task {task_id}",
                metadata={"task_id": task_id},
            )

        elif action == "list":
            task_list = []
            for task_id, task in self._tasks.items():
                status = "running" if not task.done() else "completed"
                task_list.append(f"{task_id}: {status}")

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output="\n".join(task_list) if task_list else "No tasks",
                metadata={"task_count": len(self._tasks)},
            )

        elif action == "stop":
            task_id = input_data.get("task_id")
            if not task_id or task_id not in self._tasks:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Task not found: {task_id}",
                )

            task = self._tasks[task_id]
            task.cancel()

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=f"Stopped task {task_id}",
            )

        elif action == "output":
            task_id = input_data.get("task_id")
            if not task_id or task_id not in self._tasks:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Task not found: {task_id}",
                )

            task = self._tasks[task_id]
            if not task.done():
                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=f"Task {task_id} is still running",
                )

            try:
                result = task.result()
                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=f"stdout:\n{result['stdout']}\nstderr:\n{result['stderr']}\nexit code: {result['exit_code']}",
                )
            except Exception as e:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Task error: {str(e)}",
                )

        return ToolResult(
            status=ToolResultStatus.ERROR,
            error=f"Unknown action: {action}",
        )
