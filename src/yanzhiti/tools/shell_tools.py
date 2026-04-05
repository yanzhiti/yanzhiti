"""
Shell execution tools
"""

import asyncio
import contextlib
import os
from datetime import datetime
from typing import Any

from yanzhiti.core.tool import Tool, ToolContext, ToolInputSchema, ToolResult
from yanzhiti.types import PermissionResult, ToolResultStatus


class BashTool(Tool):
    """Tool for executing shell commands"""

    def __init__(self):
        super().__init__(
            name="bash",
            description="Execute a bash shell command",
        )
        self._dangerous_patterns = [
            "rm -rf /", "rm -rf /*", ":(){:|:&};:",
            "mkfs", "dd if=", "> /dev/sd",
            "chmod -R 777 /", "chmod 000 /",
        ]

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
                "env": {
                    "type": "object",
                    "description": "Environment variables to set",
                },
            },
            required=["command"],
        )

    async def check_permission(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> PermissionResult:
        command = input_data.get("command", "")
        for pattern in self._dangerous_patterns:
            if pattern in command:
                return PermissionResult(
                    granted=False,
                    reason=f"Command contains dangerous pattern: {pattern}",
                )
        return PermissionResult(granted=True)

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        command = input_data["command"]
        timeout = input_data.get("timeout", 120000) / 1000
        cwd = input_data.get("cwd", context.cwd)
        env_overrides = input_data.get("env", {})

        try:
            env = os.environ.copy()
            env.update(env_overrides)

            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env=env,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                process.kill()
                with contextlib.suppress(Exception):
                    await process.wait()
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Command timed out after {timeout} seconds",
                    metadata={"command": command, "timeout": timeout},
                )

            output = []
            if stdout:
                output.append(f"stdout:\n{stdout.decode('utf-8', errors='replace')}")
            if stderr:
                output.append(f"stderr:\n{stderr.decode('utf-8', errors='replace')}")

            output.append(f"exit code: {process.returncode}")

            return ToolResult(
                status=ToolResultStatus.SUCCESS
                if process.returncode == 0
                else ToolResultStatus.ERROR,
                output="\n".join(output),
                metadata={
                    "command": command,
                    "exit_code": process.returncode,
                    "timeout": timeout,
                    "cwd": cwd,
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
        input_data: dict[str, Any],
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
                status=ToolResultStatus.SUCCESS
                if process.returncode == 0
                else ToolResultStatus.ERROR,
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
        self._tasks: dict[str, asyncio.Task] = {}
        self._task_results: dict[str, dict] = {}
        self._task_timestamps: dict[str, datetime] = {}

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "action": {
                    "type": "string",
                    "enum": ["create", "list", "stop", "output", "cleanup"],
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
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds for task execution (default: no timeout)",
                },
                "auto_cleanup": {
                    "type": "boolean",
                    "description": "Auto cleanup completed tasks after retrieval (default: true)",
                },
            },
            required=["action"],
        )

    def _generate_task_id(self) -> str:
        """Generate unique task ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"task_{timestamp}"

    async def execute(
        self,
        input_data: dict[str, Any],
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

            timeout = input_data.get("timeout")
            task_id = self._generate_task_id()

            async def run_command():
                try:
                    process = await asyncio.create_subprocess_shell(
                        command,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        cwd=context.cwd,
                    )

                    if timeout:
                        try:
                            stdout, stderr = await asyncio.wait_for(
                                process.communicate(),
                                timeout=timeout,
                            )
                            result = {
                                "stdout": stdout.decode("utf-8", errors="replace"),
                                "stderr": stderr.decode("utf-8", errors="replace"),
                                "exit_code": process.returncode,
                                "status": "completed",
                            }
                        except asyncio.TimeoutError:
                            process.kill()
                            with contextlib.suppress(Exception):
                                await process.wait()
                            result = {
                                "stdout": "",
                                "stderr": f"Task timed out after {timeout} seconds",
                                "exit_code": -1,
                                "status": "timeout",
                            }
                    else:
                        stdout, stderr = await process.communicate()
                        result = {
                            "stdout": stdout.decode("utf-8", errors="replace"),
                            "stderr": stderr.decode("utf-8", errors="replace"),
                            "exit_code": process.returncode,
                            "status": "completed",
                        }
                except Exception as e:
                    result = {
                        "stdout": "",
                        "stderr": str(e),
                        "exit_code": -1,
                        "status": "error",
                    }

                self._task_results[task_id] = result
                return result

            task = asyncio.create_task(run_command())
            self._tasks[task_id] = task
            self._task_timestamps[task_id] = datetime.now()

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=f"Created task {task_id}",
                metadata={"task_id": task_id, "timeout": timeout},
            )

        elif action == "list":
            task_list = []
            for task_id, task in self._tasks.items():
                status = "running" if not task.done() else "completed"
                start_time = self._task_timestamps.get(task_id)
                if start_time:
                    duration = (datetime.now() - start_time).total_seconds()
                    task_list.append(f"{task_id}: {status} (running for {duration:.1f}s)")
                else:
                    task_list.append(f"{task_id}: {status}")

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output="\n".join(task_list) if task_list else "No tasks",
                metadata={"task_count": len(self._tasks), "running": sum(1 for t in self._tasks.values() if not t.done())},
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

            if task_id in self._task_results:
                self._task_results[task_id]["status"] = "stopped"
            else:
                self._task_results[task_id] = {"status": "stopped"}

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=f"Stopped task {task_id}",
            )

        elif action == "output":
            task_id = input_data.get("task_id")
            auto_cleanup = input_data.get("auto_cleanup", True)

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
                status = result.get("status", "unknown")

                if auto_cleanup:
                    del self._tasks[task_id]
                    if task_id in self._task_results:
                        del self._task_results[task_id]
                    if task_id in self._task_timestamps:
                        del self._task_timestamps[task_id]

                output = f"Status: {status}\nstdout:\n{result.get('stdout', '')}\nstderr:\n{result.get('stderr', '')}\nexit code: {result.get('exit_code', 'N/A')}"
                return ToolResult(
                    status=ToolResultStatus.SUCCESS if status == "completed" else ToolResultStatus.ERROR,
                    output=output,
                    metadata={"task_id": task_id, "status": status, "cleaned_up": auto_cleanup},
                )
            except Exception as e:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Task error: {str(e)}",
                )

        elif action == "cleanup":
            completed_ids = [tid for tid, t in self._tasks.items() if t.done()]
            for tid in completed_ids:
                del self._tasks[tid]
                if tid in self._task_results:
                    del self._task_results[tid]
                if tid in self._task_timestamps:
                    del self._task_timestamps[tid]

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=f"Cleaned up {len(completed_ids)} completed tasks",
                metadata={"cleaned_count": len(completed_ids)},
            )

        return ToolResult(
            status=ToolResultStatus.ERROR,
            error=f"Unknown action: {action}",
        )
