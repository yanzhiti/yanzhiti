"""
Core Tool system for 衍智体 (YANZHITI)
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from uuid import uuid4

from pydantic import BaseModel, Field

from yanzhiti.types import (
    PermissionResult,
    ToolProgress,
    ToolResultBlock,
    ToolResultStatus,
    ValidationResult,
)


class ToolInputSchema(BaseModel):
    """JSON schema for tool input"""
    type: str = "object"
    properties: Dict[str, Any] = Field(default_factory=dict)
    required: List[str] = Field(default_factory=list)


class ToolResult(BaseModel):
    """Result of tool execution"""
    status: ToolResultStatus = ToolResultStatus.SUCCESS
    output: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_block(self, tool_use_id: str) -> ToolResultBlock:
        """Convert to tool result block"""
        return ToolResultBlock(
            tool_use_id=tool_use_id,
            content=self.output or self.error or "",
            is_error=self.status == ToolResultStatus.ERROR,
        )


class ToolContext(BaseModel):
    """Context passed to tool during execution"""
    tool_use_id: str = Field(default_factory=lambda: str(uuid4()))
    cwd: str = "."
    permission_mode: str = "default"
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


class Tool(ABC):
    """
    Base class for all tools

    Tools are the primary way Claude interacts with the environment.
    Each tool defines its schema, validation, and execution logic.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._input_schema: Optional[ToolInputSchema] = None

    @property
    @abstractmethod
    def input_schema(self) -> ToolInputSchema:
        """Get the input schema for this tool"""
        pass

    @abstractmethod
    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        """
        Execute the tool with given input

        Args:
            input_data: Tool input parameters
            context: Execution context

        Returns:
            ToolResult with output or error
        """
        pass

    def validate_input(self, input_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate tool input against schema

        Args:
            input_data: Input to validate

        Returns:
            ValidationResult indicating success or failure
        """
        try:
            # Basic validation - can be overridden for custom validation
            if self.input_schema.required:
                for field in self.input_schema.required:
                    if field not in input_data:
                        return ValidationResult(
                            valid=False,
                            message=f"Missing required field: {field}",
                            error_code=400,
                        )
            return ValidationResult(valid=True)
        except Exception as e:
            return ValidationResult(
                valid=False,
                message=str(e),
                error_code=400,
            )

    async def check_permission(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> PermissionResult:
        """
        Check if tool execution is permitted

        Args:
            input_data: Tool input
            context: Execution context

        Returns:
            PermissionResult indicating if execution is allowed
        """
        # Default: always allow
        # Override in subclasses for permission checks
        return PermissionResult(granted=True)

    def to_anthropic_format(self) -> Dict[str, Any]:
        """
        Convert tool to Anthropic API format

        Returns:
            Dictionary in Anthropic tool format
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema.model_dump(exclude_none=True),
        }


class ToolRegistry:
    """Registry for managing available tools"""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool"""
        self._tools[tool.name] = tool

    def unregister(self, name: str) -> None:
        """Unregister a tool"""
        self._tools.pop(name, None)

    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self._tools.get(name)

    def list_tools(self) -> List[Tool]:
        """List all registered tools"""
        return list(self._tools.values())

    def to_anthropic_format(self) -> List[Dict[str, Any]]:
        """Convert all tools to Anthropic API format"""
        return [tool.to_anthropic_format() for tool in self._tools.values()]

    def __contains__(self, name: str) -> bool:
        return name in self._tools

    def __len__(self) -> int:
        return len(self._tools)
