"""
Claude Code - Python Implementation
A comprehensive AI-powered coding assistant
"""

__version__ = "2.1.88"
__author__ = "Claude Code Python Team"

from claude_code.core.query_engine import QueryEngine
from claude_code.core.tool import Tool, ToolResult

__all__ = [
    "__version__",
    "__author__",
    "QueryEngine",
    "Tool",
    "ToolResult",
]
