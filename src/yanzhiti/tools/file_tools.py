"""
File operation tools
"""

from pathlib import Path
from typing import Any

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
        self._binary_extensions = {
            ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp",
            ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
            ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
            ".mp3", ".mp4", ".avi", ".mov", ".mkv", ".wav", ".flac",
            ".exe", ".dll", ".so", ".dylib", ".app",
            ".ttf", ".otf", ".woff", ".woff2", ".eot",
            ".pyc", ".pyo", ".class", ".o", ".obj",
        }

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
                "encoding": {
                    "type": "string",
                    "description": "File encoding (default: auto-detect)",
                },
            },
            required=["file_path"],
        )

    def _is_binary_file(self, path: Path) -> bool:
        """Check if file is likely binary based on extension or content"""
        if path.suffix.lower() in self._binary_extensions:
            return True
        try:
            with open(path, "rb") as f:
                chunk = f.read(8192)
                return b"\x00" in chunk
        except Exception:
            return False

    def _detect_encoding(self, path: Path) -> str:
        """Detect file encoding"""
        try:
            import chardet
            with open(path, "rb") as f:
                raw_data = f.read(32768)
            result = chardet.detect(raw_data)
            return result.get("encoding", "utf-8") or "utf-8"
        except ImportError:
            return "utf-8"
        except Exception:
            return "utf-8"

    async def check_permission(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> PermissionResult:
        return PermissionResult(granted=True)

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        file_path = input_data["file_path"]
        offset = input_data.get("offset", 0)
        limit = input_data.get("limit")
        encoding = input_data.get("encoding")

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

            if self._is_binary_file(path):
                file_size = path.stat().st_size
                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=f"[Binary file: {path.suffix or 'unknown type'}, {file_size} bytes]",
                    metadata={"file_path": file_path, "binary": True, "size": file_size},
                )

            detected_encoding = encoding or self._detect_encoding(path)

            async with aiofiles.open(file_path, encoding=detected_encoding) as f:
                lines = await f.readlines()

            if offset > 0:
                lines = lines[offset:]
            if limit:
                lines = lines[:limit]

            output = []
            start_line = offset + 1
            for i, line in enumerate(lines):
                output.append(f"{start_line + i}->{line}")

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output="".join(output),
                metadata={"file_path": file_path, "lines_read": len(lines), "encoding": detected_encoding},
            )

        except UnicodeDecodeError as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Encoding error reading file: {str(e)}. Try specifying encoding.",
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
        input_data: dict[str, Any],
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
        input_data: dict[str, Any],
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

            async with aiofiles.open(file_path) as f:
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
        input_data: dict[str, Any],
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
        self._default_ignore_patterns = {
            ".git", ".svn", "__pycache__", "node_modules",
            ".venv", "venv", ".tox", ".eggs", "*.egg-info",
            ".pytest_cache", ".mypy_cache", ".ruff_cache",
            "dist", "build", ".tox", ".hypothesis",
        }

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
                "ignore": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Patterns to ignore (e.g., ['*.pyc', 'node_modules'])",
                },
                "case_sensitive": {
                    "type": "boolean",
                    "description": "Case sensitive search (default: true)",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 1000)",
                },
                "line_number": {
                    "type": "boolean",
                    "description": "Include line numbers in output (default: true)",
                },
            },
            required=["pattern"],
        )

    def _should_ignore(self, path: Path, ignore_patterns: set[str]) -> bool:
        """Check if path matches any ignore pattern"""
        path_str = str(path)
        for pattern in ignore_patterns:
            if pattern in path_str or path.match(pattern):
                return True
        return False

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        import re

        pattern = input_data["pattern"]
        search_path = input_data.get("path", context.cwd)
        file_pattern = input_data.get("glob", "*")
        ignore_patterns = set(input_data.get("ignore", []))
        ignore_patterns.update(self._default_ignore_patterns)
        case_sensitive = input_data.get("case_sensitive", True)
        max_results = input_data.get("max_results", 1000)
        show_line_number = input_data.get("line_number", True)

        try:
            path = Path(search_path)
            regex_flags = 0 if case_sensitive else re.IGNORECASE
            regex = re.compile(pattern, regex_flags)

            results = []
            files_to_search = [path] if path.is_file() else list(path.rglob(file_pattern))

            for file_path in files_to_search:
                if not file_path.is_file():
                    continue
                if self._should_ignore(file_path, ignore_patterns):
                    continue
                try:
                    async with aiofiles.open(file_path) as f:
                        lines = await f.readlines()

                    for i, line in enumerate(lines):
                        if regex.search(line):
                            line_prefix = f"{file_path}:{i + 1}: " if show_line_number else ""
                            results.append(f"{line_prefix}{line.rstrip()}")
                            if len(results) >= max_results:
                                break
                except (UnicodeDecodeError, PermissionError, OSError):
                    continue

                if len(results) >= max_results:
                    break

            output = "\n".join(results)
            if len(results) >= max_results:
                output += f"\n... (truncated at {max_results} results)"

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=output,
                metadata={"pattern": pattern, "matches": len(results), "truncated": len(results) >= max_results},
            )

        except re.error as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Invalid regex pattern: {str(e)}",
            )
        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error searching: {str(e)}",
            )
