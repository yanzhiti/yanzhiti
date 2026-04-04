"""
Local Query Engine using local models (LM Studio or MLX)
No API required - runs completely on your Mac
"""

import json
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from yanzhiti.core.tool import Tool, ToolContext, ToolRegistry
from yanzhiti.types import (
    AssistantMessage,
    Message,
    Usage,
    UserMessage,
)


class LocalQueryEngineConfig(BaseModel):
    """Configuration for Local QueryEngine"""

    cwd: str = "."
    model_name: str = "local-model"
    backend: str = "lm_studio"  # "lm_studio" or "mlx"
    base_url: str = "http://localhost:1234/v1"  # LM Studio default
    max_tokens: int = 2048
    temperature: float = 0.7
    system_prompt: str | None = None
    tools: list[Tool] = Field(default_factory=list)
    max_turns: int = 50
    verbose: bool = False

    class Config:
        arbitrary_types_allowed = True


class LocalQueryEngine:
    """
    Local Query Engine using local models
    Supports LM Studio (OpenAI-compatible) or MLX
    Runs completely on your Mac without API calls
    """

    def __init__(self, config: LocalQueryEngineConfig):
        self.config = config

        # Initialize client based on backend
        if config.backend == "lm_studio":
            from yanzhiti.core.lm_studio_client import SimpleLMStudioClient

            print(f"🚀 Initializing LM Studio client: {config.base_url}")
            self.client = SimpleLMStudioClient(base_url=config.base_url, model=config.model_name)
            self._backend_type = "lm_studio"
        else:
            from yanzhiti.core.mlx_client import SimpleMLXClient

            print(f"🚀 Initializing MLX model: {config.model_name}")
            self.client = SimpleMLXClient(model_name=config.model_name)
            self._backend_type = "mlx"

        # Tool registry
        self.tool_registry = ToolRegistry()
        for tool in config.tools:
            self.tool_registry.register(tool)

        # State
        self.messages: list[Message] = []
        self.usage = Usage()
        self.session_id = uuid4()
        self._turn_count = 0

        print("✅ Local QueryEngine ready!")

    async def query(
        self,
        user_input: str,
    ) -> AssistantMessage:
        """
        Process a user query using local MLX model
        """
        # Create user message
        user_message = UserMessage(content=user_input)
        self.messages.append(user_message)

        # Process in loop
        while self._turn_count < self.config.max_turns:
            self._turn_count += 1

            # Generate response from local model
            response = await self._generate_response()

            # Create assistant message
            assistant_message = AssistantMessage(content=response)
            self.messages.append(assistant_message)

            # Check for tool calls in response
            tool_calls = self._extract_tool_calls(response)

            if tool_calls:
                # Execute tools
                tool_results = []
                for tool_call in tool_calls:
                    result = await self._execute_tool(tool_call)
                    tool_results.append(result)

                # Add tool results to messages
                result_msg = UserMessage(content=f"Tool results:\n{tool_results}")
                self.messages.append(result_msg)

                # Continue loop to get next response
                continue

            # No tool calls, we're done
            return assistant_message

        # Max turns reached
        return AssistantMessage(content="Maximum turns reached. Please start a new query.")

    async def _generate_response(self) -> str:
        """Generate response from local model"""
        # Build messages for MLX
        mlx_messages = []

        # Add system prompt
        if self.config.system_prompt:
            mlx_messages.append({"role": "system", "content": self._build_system_prompt()})

        # Add conversation history
        for msg in self.messages[-10:]:  # Keep last 10 messages for context
            mlx_messages.append(
                {
                    "role": msg.role.value,
                    "content": msg.content if isinstance(msg.content, str) else str(msg.content),
                }
            )

        # Generate response
        response = await self.client.chat(
            messages=mlx_messages,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
        )

        # Update usage
        self.usage.total_tokens += len(response.split())

        return response

    def _build_system_prompt(self) -> str:
        """Build system prompt with tool definitions"""
        parts = [self.config.system_prompt or "You are a helpful AI assistant."]

        # Add tool definitions
        if len(self.tool_registry) > 0:
            parts.append("\n\nYou have access to the following tools:")
            for tool in self.tool_registry.list_tools():
                parts.append(f"\n- {tool.name}: {tool.description}")

            parts.append("\n\nTo use a tool, format your response like:")
            parts.append("\nTOOL_USE: <tool_name>")
            parts.append("\nPARAMS: <json_parameters>")
            parts.append("\nEND_TOOL")

        return "\n".join(parts)

    def _extract_tool_calls(self, response: str) -> list[dict[str, Any]]:
        """Extract tool calls from response"""
        tool_calls = []

        # Simple pattern matching for tool calls
        if "TOOL_USE:" in response:
            lines = response.split("\n")
            i = 0
            while i < len(lines):
                if lines[i].strip().startswith("TOOL_USE:"):
                    tool_name = lines[i].split("TOOL_USE:")[1].strip()

                    # Look for params
                    params = {}
                    if i + 1 < len(lines) and lines[i + 1].strip().startswith("PARAMS:"):
                        try:
                            params_str = lines[i + 1].split("PARAMS:")[1].strip()
                            params = json.loads(params_str)
                        except Exception:
                            pass

                    tool_calls.append({"name": tool_name, "parameters": params})

                    # Skip to END_TOOL
                    while i < len(lines) and "END_TOOL" not in lines[i]:
                        i += 1

                i += 1

        return tool_calls

    async def _execute_tool(self, tool_call: dict[str, Any]) -> str:
        """Execute a tool"""
        tool_name = tool_call["name"]
        params = tool_call.get("parameters", {})

        tool = self.tool_registry.get(tool_name)
        if not tool:
            return f"Error: Unknown tool '{tool_name}'"

        # Create context
        context = ToolContext(
            tool_use_id=str(uuid4()),
            cwd=self.config.cwd,
        )

        # Validate
        validation = tool.validate_input(params)
        if not validation.valid:
            return f"Error: {validation.message}"

        # Execute
        try:
            result = await tool.execute(params, context)
            return result.output or result.error or "Tool executed successfully"
        except Exception as e:
            return f"Error executing tool: {str(e)}"

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
            "model": self.config.model_name,
        }
