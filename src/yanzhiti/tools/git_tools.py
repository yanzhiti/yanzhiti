"""
Git operation tools
"""

import asyncio
from typing import Any

from yanzhiti.core.tool import Tool, ToolContext, ToolInputSchema, ToolResult
from yanzhiti.types import ToolResultStatus


class GitTool(Tool):
    """Tool for Git operations"""

    def __init__(self):
        super().__init__(
            name="git",
            description="Execute Git commands",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "command": {
                    "type": "string",
                    "description": "Git command to execute (e.g., 'status', 'commit', 'push')",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Additional arguments",
                },
                "cwd": {
                    "type": "string",
                    "description": "Working directory (default: current directory)",
                },
            },
            required=["command"],
        )

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        command = input_data["command"]
        args = input_data.get("args", [])
        cwd = input_data.get("cwd", context.cwd)

        # Build git command
        cmd = ["git", command] + args

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )

            stdout, stderr = await process.communicate()

            output = []
            if stdout:
                output.append(stdout.decode("utf-8", errors="replace"))
            if stderr:
                output.append(stderr.decode("utf-8", errors="replace"))

            return ToolResult(
                status=ToolResultStatus.SUCCESS if process.returncode == 0 else ToolResultStatus.ERROR,
                output="\n".join(output),
                metadata={
                    "command": f"git {command}",
                    "exit_code": process.returncode,
                },
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Git command failed: {str(e)}",
            )


class GitStatusTool(Tool):
    """Tool for checking Git status"""

    def __init__(self):
        super().__init__(
            name="git_status",
            description="Get Git repository status",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "cwd": {
                    "type": "string",
                    "description": "Working directory",
                },
            },
            required=[],
        )

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        cwd = input_data.get("cwd", context.cwd)

        try:
            # Check if it's a git repository
            process = await asyncio.create_subprocess_exec(
                "git",
                "rev-parse",
                "--git-dir",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error="Not a Git repository",
                )

            # Get status
            process = await asyncio.create_subprocess_exec(
                "git",
                "status",
                "--porcelain",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )
            stdout, stderr = await process.communicate()

            status_output = stdout.decode("utf-8", errors="replace")

            # Parse status
            modified = []
            added = []
            deleted = []
            untracked = []

            for line in status_output.split("\n"):
                if not line:
                    continue
                status = line[:2]
                file = line[3:]

                if status.strip() == "M":
                    modified.append(file)
                elif status.strip() == "A":
                    added.append(file)
                elif status.strip() == "D":
                    deleted.append(file)
                elif status == "??":
                    untracked.append(file)

            output = [
                "Git Status:",
                f"  Modified: {len(modified)}",
                f"  Added: {len(added)}",
                f"  Deleted: {len(deleted)}",
                f"  Untracked: {len(untracked)}",
            ]

            if modified:
                output.append("\nModified files:")
                output.extend(f"  - {f}" for f in modified)
            if added:
                output.append("\nAdded files:")
                output.extend(f"  - {f}" for f in added)
            if deleted:
                output.append("\nDeleted files:")
                output.extend(f"  - {f}" for f in deleted)
            if untracked:
                output.append("\nUntracked files:")
                output.extend(f"  - {f}" for f in untracked[:10])
                if len(untracked) > 10:
                    output.append(f"  ... and {len(untracked) - 10} more")

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output="\n".join(output),
                metadata={
                    "modified": len(modified),
                    "added": len(added),
                    "deleted": len(deleted),
                    "untracked": len(untracked),
                },
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Failed to get Git status: {str(e)}",
            )


class GitDiffTool(Tool):
    """Tool for viewing Git diff"""

    def __init__(self):
        super().__init__(
            name="git_diff",
            description="View Git diff",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "file": {
                    "type": "string",
                    "description": "File to diff (optional)",
                },
                "staged": {
                    "type": "boolean",
                    "description": "Show staged changes",
                },
                "cwd": {
                    "type": "string",
                    "description": "Working directory",
                },
            },
            required=[],
        )

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        file = input_data.get("file")
        staged = input_data.get("staged", False)
        cwd = input_data.get("cwd", context.cwd)

        try:
            cmd = ["git", "diff"]
            if staged:
                cmd.append("--staged")
            if file:
                cmd.append(file)

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )

            stdout, stderr = await process.communicate()

            diff = stdout.decode("utf-8", errors="replace")

            if not diff:
                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output="No changes",
                )

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=diff,
                metadata={"file": file, "staged": staged},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Failed to get Git diff: {str(e)}",
            )


class GitLogTool(Tool):
    """Tool for viewing Git log"""

    def __init__(self):
        super().__init__(
            name="git_log",
            description="View Git commit history",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "count": {
                    "type": "integer",
                    "description": "Number of commits to show (default: 10)",
                },
                "oneline": {
                    "type": "boolean",
                    "description": "Show one line per commit",
                },
                "file": {
                    "type": "string",
                    "description": "Show commits for specific file",
                },
                "cwd": {
                    "type": "string",
                    "description": "Working directory",
                },
            },
            required=[],
        )

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        count = input_data.get("count", 10)
        oneline = input_data.get("oneline", True)
        file = input_data.get("file")
        cwd = input_data.get("cwd", context.cwd)

        try:
            cmd = ["git", "log", f"-{count}"]
            if oneline:
                cmd.append("--oneline")
            if file:
                cmd.extend(["--", file])

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )

            stdout, stderr = await process.communicate()

            log = stdout.decode("utf-8", errors="replace")

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=log,
                metadata={"count": count, "file": file},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Failed to get Git log: {str(e)}",
            )


class GitBranchTool(Tool):
    """Tool for Git branch operations"""

    def __init__(self):
        super().__init__(
            name="git_branch",
            description="Manage Git branches",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "action": {
                    "type": "string",
                    "enum": ["list", "create", "delete", "switch"],
                    "description": "Branch action",
                },
                "branch": {
                    "type": "string",
                    "description": "Branch name",
                },
                "cwd": {
                    "type": "string",
                    "description": "Working directory",
                },
            },
            required=["action"],
        )

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        action = input_data["action"]
        branch = input_data.get("branch")
        cwd = input_data.get("cwd", context.cwd)

        try:
            if action == "list":
                cmd = ["git", "branch", "-a"]
            elif action == "create":
                if not branch:
                    return ToolResult(
                        status=ToolResultStatus.ERROR,
                        error="Branch name required for create action",
                    )
                cmd = ["git", "branch", branch]
            elif action == "delete":
                if not branch:
                    return ToolResult(
                        status=ToolResultStatus.ERROR,
                        error="Branch name required for delete action",
                    )
                cmd = ["git", "branch", "-d", branch]
            elif action == "switch":
                if not branch:
                    return ToolResult(
                        status=ToolResultStatus.ERROR,
                        error="Branch name required for switch action",
                    )
                cmd = ["git", "checkout", branch]
            else:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Unknown action: {action}",
                )

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )

            stdout, stderr = await process.communicate()

            output = []
            if stdout:
                output.append(stdout.decode("utf-8", errors="replace"))
            if stderr:
                output.append(stderr.decode("utf-8", errors="replace"))

            return ToolResult(
                status=ToolResultStatus.SUCCESS if process.returncode == 0 else ToolResultStatus.ERROR,
                output="\n".join(output),
                metadata={"action": action, "branch": branch},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Git branch operation failed: {str(e)}",
            )
