"""
Query Engine - The heart of 衍智体 (YANZHITI)
"""

from typing import Any
from uuid import uuid4

# Note: This project uses the Anthropic SDK for AI model integration
# The SDK is used as a dependency, but this is an independent implementation
from anthropic import AsyncAnthropic
from anthropic.types import Message as AIMessage
from pydantic import BaseModel, Field

from yanzhiti.core.tool import Tool, ToolContext, ToolRegistry
from yanzhiti.types import (
    AssistantMessage,
    Message,
    Usage,
    UserMessage,
)


class QueryEngineConfig(BaseModel):
    """Configuration for QueryEngine"""
    cwd: str = "."
    model: str = "default-model"
    max_tokens: int = 4096
    temperature: float = 1.0
    system_prompt: str | None = None
    tools: list[Tool] = Field(default_factory=list)
    max_turns: int = 100
    verbose: bool = False

    class Config:
        arbitrary_types_allowed = True


class QueryEngine:
    """
    Query Engine processes queries and orchestrates tool execution

    This is the core component that:
    1. Processes user queries
    2. Calls the AI API
    3. Executes tools
    4. Manages conversation state
    """

    def __init__(
        self,
        config: QueryEngineConfig,
        api_key: str | None = None,
        base_url: str | None = None,
    ):
        self.config = config
        self.api_key = api_key
        self.base_url = base_url
        # 支持自定义 API 端点 (如 OpenRouter)
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        self.client = AsyncAnthropic(**client_kwargs)
        self.tool_registry = ToolRegistry()

        # Register tools
        for tool in config.tools:
            self.tool_registry.register(tool)

        # State
        self.messages: list[Message] = []
        self.usage = Usage()
        self.session_id = uuid4()
        self._turn_count = 0

    async def query(
        self,
        user_input: str,
        attachments: list[dict[str, Any]] | None = None,
    ) -> AssistantMessage:
        """
        Process a user query

        Args:
            user_input: User's text input
            attachments: Optional file attachments

        Returns:
            AssistantMessage with the response
        """
        # Create user message
        content = user_input
        if attachments:
            content = [{"type": "text", "text": user_input}]
            content.extend(attachments)

        user_message = UserMessage(content=content)
        self.messages.append(user_message)

        # Process query in a loop
        while self._turn_count < self.config.max_turns:
            self._turn_count += 1

            # Call AI API
            response = await self._call_api()

            # Process response
            assistant_message = await self._process_response(response)

            # Check if we're done (no more tool uses)
            if not self._has_tool_uses(response):
                return assistant_message

        # Max turns reached
        return AssistantMessage(
            content="Maximum turns reached. Please start a new query.",
        )

    async def _call_api(self) -> AIMessage:
        """Call the AI API"""
        # Convert messages to API format
        messages = self._convert_messages()

        # Build request
        request_params = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "messages": messages,
        }

        # Add system prompt if provided
        if self.config.system_prompt:
            request_params["system"] = self.config.system_prompt

        # Add tools if available
        if len(self.tool_registry) > 0:
            request_params["tools"] = self.tool_registry.to_api_format()

        # Make API call
        response = await self.client.messages.create(**request_params)

        # Update usage
        self.usage.input_tokens += response.usage.input_tokens
        self.usage.output_tokens += response.usage.output_tokens
        self.usage.total_tokens = self.usage.input_tokens + self.usage.output_tokens

        return response

    async def _process_response(
        self,
        response: AIMessage,
    ) -> AssistantMessage:
        """Process API response and execute any tools"""
        # Extract content blocks
        content_blocks = []
        tool_results = []

        for block in response.content:
            if block.type == "text":
                content_blocks.append({
                    "type": "text",
                    "text": block.text,
                })
            elif block.type == "tool_use":
                # Execute tool
                tool_result = await self._execute_tool(
                    block.id,
                    block.name,
                    block.input,
                )
                tool_results.append(tool_result)

        # Create assistant message
        assistant_content = content_blocks.copy()
        for block in response.content:
            if block.type == "tool_use":
                assistant_content.append({
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                })

        assistant_message = AssistantMessage(content=assistant_content)
        self.messages.append(assistant_message)

        # Add tool results as user message
        if tool_results:
            user_content = [
                {
                    "type": "tool_result",
                    "tool_use_id": result.tool_use_id,
                    "content": result.content,
                    "is_error": result.is_error,
                }
                for result in tool_results
            ]
            tool_message = UserMessage(content=user_content)
            self.messages.append(tool_message)

        return assistant_message

    async def _execute_tool(
        self,
        tool_id: str,
        tool_name: str,
        tool_input: dict[str, Any],
    ) -> Any:
        """Execute a tool and return result"""
        tool = self.tool_registry.get(tool_name)
        if not tool:
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": f"Unknown tool: {tool_name}",
                "is_error": True,
            }

        # Create context
        context = ToolContext(
            tool_use_id=tool_id,
            cwd=self.config.cwd,
        )

        # Validate input
        validation = tool.validate_input(tool_input)
        if not validation.valid:
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": validation.message or "Invalid input",
                "is_error": True,
            }

        # Check permission
        permission = await tool.check_permission(tool_input, context)
        if not permission.granted:
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": permission.reason or "Permission denied",
                "is_error": True,
            }

        # Execute tool
        try:
            result = await tool.execute(tool_input, context)
            return result.to_block(tool_id).model_dump()
        except Exception as e:
            return {
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": f"Tool execution error: {str(e)}",
                "is_error": True,
            }

    def _convert_messages(self) -> list[dict[str, Any]]:
        """Convert internal messages to API format"""
        api_messages = []

        for msg in self.messages:
            if isinstance(msg.content, str):
                api_messages.append({
                    "role": msg.role.value,
                    "content": msg.content,
                })
            else:
                api_messages.append({
                    "role": msg.role.value,
                    "content": msg.content,
                })

        return api_messages

    def _has_tool_uses(self, response: AIMessage) -> bool:
        """Check if response contains tool uses"""
        return any(block.type == "tool_use" for block in response.content)

    def reset(self) -> None:
        """Reset the engine state"""
        self.messages = []
        self.usage = Usage()
        self.session_id = uuid4()
        self._turn_count = 0

    def get_stats(self) -> dict[str, Any]:
        """Get engine statistics"""
        return {
            "session_id": str(self.session_id),
            "message_count": len(self.messages),
            "turn_count": self._turn_count,
            "usage": self.usage.model_dump(),
            "tool_count": len(self.tool_registry),
        }
