"""
衍智体 (YANZHITI) - Python Implementation
A comprehensive AI-powered coding assistant
"""

__version__ = "2.2.0"
__author__ = "衍智体 (YANZHITI) Python Team"

from yanzhiti.core.query_engine import QueryEngine
from yanzhiti.core.tool import Tool, ToolResult

__all__ = [
    "__version__",
    "__author__",
    "QueryEngine",
    "Tool",
    "ToolResult",
]
