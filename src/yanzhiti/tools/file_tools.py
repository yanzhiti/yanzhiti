"""
File operation tools
"""

import asyncio
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiofiles

from yanzhiti.core.tool import Tool, ToolContext, ToolInputSchema, ToolResult
from yanzhiti.types import PermissionResult, ToolResultStatus


class FileReadTool(Tool):
    """Tool for reading file contents"""

    def __init__(self):
        super().__init__(
            name="file_read",
            description="Read the contents of a file from the local filesystem",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "file_path": {
                    "type": "string",
                    "description": "The absolute path to the file to read",
                },
                "offset": {
                    "type": "integer",
                    "description": "Line number to start reading from (optional)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of lines to read (optional)",
                },
            },
            required=["file_path"],
        )

    async def check_permission(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> PermissionResult:
        file_path = input_data["file_path"]
        # Check if file is within allowed directories
        # For now, allow all - implement proper permission checks later
        return PermissionResult(granted=True)

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        file_path = input_data["file_path"]
        offset = input_data.get("offset", 0)
        limit = input_data.get("limit")

        try:
            path = Path(file_path)
            if not path.exists():
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"File not found: {file_path}",
                )

            if not path.is_file():
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Not a file: {file_path}",
                )

            async with aiofiles.open(file_path, mode="r") as f:
                lines = await f.readlines()

            # Apply offset and limit
            if offset > 0:
                lines = lines[offset:]
            if limit:
                lines = lines[:limit]

            # Format with line numbers
            output = []
            start_line = offset + 1
            for i, line in enumerate(lines):
                output.append(f"{start_line + i}->{line}")

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output="".join(output),
                metadata={"file_path": file_path, "lines_read": len(lines)},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error reading file: {str(e)}",
            )


class FileWriteTool(Tool):
    """Tool for writing file contents"""

    def __init__(self):
        super().__init__(
            name="file_write",
            description="Write content to a file on the local filesystem",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "file_path": {
                    "type": "string",
                    "description": "The absolute path to the file to write",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file",
                },
            },
            required=["file_path", "content"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        file_path = input_data["file_path"]
        content = input_data["content"]

        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            async with aiofiles.open(file_path, mode="w") as f:
                await f.write(content)

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=f"Successfully wrote to {file_path}",
                metadata={"file_path": file_path, "bytes_written": len(content)},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error writing file: {str(e)}",
            )


class FileEditTool(Tool):
    """Tool for editing file contents"""

    def __init__(self):
        super().__init__(
            name="file_edit",
            description="Edit a file by replacing specific text",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "file_path": {
                    "type": "string",
                    "description": "The absolute path to the file to edit",
                },
                "old_string": {
                    "type": "string",
                    "description": "The text to search for",
                },
                "new_string": {
                    "type": "string",
                    "description": "The text to replace it with",
                },
                "replace_all": {
                    "type": "boolean",
                    "description": "Replace all occurrences (default: false)",
                },
            },
            required=["file_path", "old_string", "new_string"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        file_path = input_data["file_path"]
        old_string = input_data["old_string"]
        new_string = input_data["new_string"]
        replace_all = input_data.get("replace_all", False)

        try:
            path = Path(file_path)
            if not path.exists():
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"File not found: {file_path}",
                )

            async with aiofiles.open(file_path, mode="r") as f:
                content = await f.read()

            if old_string not in content:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Text not found in file: {old_string[:50]}...",
                )

            if replace_all:
                new_content = content.replace(old_string, new_string)
            else:
                new_content = content.replace(old_string, new_string, 1)

            async with aiofiles.open(file_path, mode="w") as f:
                await f.write(new_content)

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=f"Successfully edited {file_path}",
                metadata={"file_path": file_path},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error editing file: {str(e)}",
            )


class GlobTool(Tool):
    """Tool for finding files by pattern"""

    def __init__(self):
        super().__init__(
            name="glob",
            description="Find files matching a pattern",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern to match files",
                },
                "path": {
                    "type": "string",
                    "description": "Directory to search in (default: current directory)",
                },
            },
            required=["pattern"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        pattern = input_data["pattern"]
        search_path = input_data.get("path", context.cwd)

        try:
            path = Path(search_path)
            matches = list(path.glob(pattern))

            # Sort by modification time
            matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)

            output = "\n".join(str(m) for m in matches)

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=output,
                metadata={"pattern": pattern, "matches": len(matches)},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error finding files: {str(e)}",
            )


class GrepTool(Tool):
    """Tool for searching file contents"""

    def __init__(self):
        super().__init__(
            name="grep",
            description="Search for text patterns in files",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "pattern": {
                    "type": "string",
                    "description": "Regular expression pattern to search for",
                },
                "path": {
                    "type": "string",
                    "description": "File or directory to search in",
                },
                "glob": {
                    "type": "string",
                    "description": "File pattern to filter (e.g., '*.py')",
                },
            },
            required=["pattern"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        import re

        pattern = input_data["pattern"]
        search_path = input_data.get("path", context.cwd)
        file_pattern = input_data.get("glob", "*")

        try:
            path = Path(search_path)
            regex = re.compile(pattern)

            results = []
            files_to_search = []

            if path.is_file():
                files_to_search = [path]
            else:
                files_to_search = list(path.rglob(file_pattern))

            for file_path in files_to_search:
                if not file_path.is_file():
                    continue

                try:
                    async with aiofiles.open(file_path, mode="r") as f:
                        lines = await f.readlines()

                    for i, line in enumerate(lines):
                        if regex.search(line):
                            results.append(f"{file_path}:{i+1}: {line.rstrip()}")

                except Exception:
                    continue

            output = "\n".join(results)

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=output,
                metadata={"pattern": pattern, "matches": len(results)},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error searching: {str(e)}",
            )
