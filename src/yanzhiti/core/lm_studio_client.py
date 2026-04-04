"""
LM Studio Client - Use local LM Studio server
LM Studio provides an OpenAI-compatible API server
"""

from collections.abc import AsyncIterator
from typing import Any

import httpx
from pydantic import BaseModel


class LMStudioConfig(BaseModel):
    """Configuration for LM Studio"""
    base_url: str = "http://localhost:1234/v1"  # LM Studio default port
    model: str = "local-model"  # LM Studio uses this as placeholder
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: float = 60.0


class LMStudioClient:
    """
    Client for LM Studio local server
    LM Studio provides OpenAI-compatible API
    """

    def __init__(self, config: LMStudioConfig | None = None):
        self.config = config or LMStudioConfig()
        self.client = httpx.AsyncClient(timeout=self.config.timeout)

    async def check_server(self) -> bool:
        """Check if LM Studio server is running"""
        try:
            response = await self.client.get(
                f"{self.config.base_url}/models"
            )
            return response.status_code == 200
        except Exception:
            return False

    async def chat(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> dict[str, Any]:
        """
        Chat completion with LM Studio

        Args:
            messages: List of message dicts with role and content
            tools: Optional tool definitions (OpenAI format)
            max_tokens: Override default max_tokens
            temperature: Override default temperature

        Returns:
            Response dict with content and metadata
        """
        # Get available models and use first one if model not specified
        models = await self.get_models()
        if models and self.config.model == "local-model":
            # Use first available model
            actual_model = models[0]["id"]
        else:
            actual_model = self.config.model

        # Build request
        request_body = {
            "model": actual_model,
            "messages": messages,
            "max_tokens": max_tokens or self.config.max_tokens,
            "temperature": temperature or self.config.temperature,
        }

        # Add tools if provided
        if tools:
            request_body["tools"] = tools

        try:
            response = await self.client.post(
                f"{self.config.base_url}/chat/completions",
                json=request_body,
            )
            response.raise_for_status()

            data = response.json()

            # Extract response
            choice = data["choices"][0]
            message = choice["message"]

            return {
                "content": message.get("content", ""),
                "tool_calls": message.get("tool_calls", []),
                "role": message.get("role", "assistant"),
                "usage": data.get("usage", {}),
                "model": data.get("model", actual_model),
            }

        except httpx.HTTPError as e:
            raise RuntimeError(f"LM Studio API error: {e}") from e

    async def stream_chat(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream chat completion
        """
        request_body = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": max_tokens or self.config.max_tokens,
            "temperature": temperature or self.config.temperature,
            "stream": True,
        }

        if tools:
            request_body["tools"] = tools

        try:
            async with self.client.stream(
                "POST",
                f"{self.config.base_url}/chat/completions",
                json=request_body,
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            import json
                            data = json.loads(data_str)
                            delta = data["choices"][0]["delta"]
                            if "content" in delta:
                                yield delta["content"]
                        except Exception:
                            continue

        except httpx.HTTPError as e:
            raise RuntimeError(f"LM Studio streaming error: {e}") from e

    async def get_models(self) -> list[dict[str, Any]]:
        """Get available models"""
        try:
            response = await self.client.get(
                f"{self.config.base_url}/models"
            )
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception:
            return []

    async def close(self):
        """Close the client"""
        await self.client.aclose()


class SimpleLMStudioClient:
    """
    Simplified LM Studio client for easy use
    """

    def __init__(
        self,
        base_url: str = "http://localhost:1234/v1",
        model: str = "local-model",
    ):
        self.config = LMStudioConfig(base_url=base_url, model=model)
        self.client = LMStudioClient(self.config)

    async def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs
    ) -> str:
        """Simple chat - returns just the content"""
        response = await self.client.chat(messages, **kwargs)
        return response["content"]

    async def generate(
        self,
        prompt: str,
        **kwargs
    ) -> str:
        """Generate from a single prompt"""
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages, **kwargs)

    async def check_server(self) -> bool:
        """Check if server is running"""
        return await self.client.check_server()

    async def close(self):
        """Close the client"""
        await self.client.close()
