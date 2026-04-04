"""
Type definitions for 衍智体 (YANZHITI)
"""

from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class PermissionMode(str, Enum):
    """Permission modes for tool execution"""

    DEFAULT = "default"
    AUTO = "auto"
    PLAN = "plan"
    BYPASS = "bypass"


class MessageRole(str, Enum):
    """Message roles in conversation"""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ToolResultStatus(str, Enum):
    """Status of tool execution result"""

    SUCCESS = "success"
    ERROR = "error"
    PERMISSION_DENIED = "permission_denied"


class Message(BaseModel):
    """Base message type"""

    role: MessageRole
    content: str | list[dict[str, Any]]
    metadata: dict[str, Any] | None = None


class UserMessage(Message):
    """User message"""

    role: MessageRole = MessageRole.USER


class AssistantMessage(Message):
    """Assistant message"""

    role: MessageRole = MessageRole.ASSISTANT


class SystemMessage(Message):
    """System message"""

    role: MessageRole = MessageRole.SYSTEM


class ToolUseBlock(BaseModel):
    """Tool use block in assistant message"""

    type: str = "tool_use"
    id: str
    name: str
    input: dict[str, Any]


class ToolResultBlock(BaseModel):
    """Tool result block"""

    type: str = "tool_result"
    tool_use_id: str
    content: str | dict[str, Any]
    is_error: bool = False


class PermissionResult(BaseModel):
    """Result of permission check"""

    granted: bool
    reason: str | None = None
    mode: PermissionMode = PermissionMode.DEFAULT


class ValidationResult(BaseModel):
    """Result of input validation"""

    valid: bool
    message: str | None = None
    error_code: int | None = None


class ToolProgress(BaseModel):
    """Progress information for tool execution"""

    tool_name: str
    tool_use_id: str
    status: str
    message: str | None = None
    percentage: float | None = None


class Usage(BaseModel):
    """API usage statistics"""

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0


class SessionInfo(BaseModel):
    """Session information"""

    session_id: UUID
    created_at: float
    updated_at: float
    message_count: int = 0
    total_usage: Usage = Field(default_factory=Usage)


class AppState(BaseModel):
    """Application state"""

    session_id: UUID | None = None
    cwd: str = "."
    messages: list[Message] = Field(default_factory=list)
    usage: Usage = Field(default_factory=Usage)
    permission_mode: PermissionMode = PermissionMode.DEFAULT
    is_active: bool = True


class Config(BaseModel):
    """Application configuration"""

    api_key: str | None = None
    model: str = "default-model"
    max_tokens: int = 4096
    temperature: float = 1.0
    timeout: int = 120
    max_retries: int = 3
    verbose: bool = False
    debug: bool = False
