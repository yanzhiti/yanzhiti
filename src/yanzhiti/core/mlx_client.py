"""
MLX Local Model Client for Mac
Supports running LLMs locally using Apple's MLX framework
"""

import asyncio
import subprocess
from collections.abc import AsyncIterator
from typing import Any

from pydantic import BaseModel


class MLXModelConfig(BaseModel):
    """Configuration for MLX model"""
    model_path: str
    model_name: str = "mlx-community/Llama-3.2-3B-Instruct-4bit"
    max_tokens: int = 4096
    temperature: float = 0.7
    top_p: float = 0.9
    use_cache: bool = True


class MLXMessage(BaseModel):
    """Message for MLX model"""
    role: str  # system, user, assistant
    content: str


class MLXClient:
    """
    Client for running MLX models locally on Mac
    Uses mlx-lm for inference
    """

    def __init__(self, config: MLXModelConfig | None = None):
        self.config = config or MLXModelConfig()
        self._check_mlx_installed()

    def _check_mlx_installed(self):
        """Check if MLX is installed"""
        try:
            result = subprocess.run(
                ["python3", "-c", "import mlx_lm"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print("⚠️  MLX not found. Installing...")
                subprocess.run(
                    ["pip", "install", "mlx-lm"],
                    check=True
                )
        except Exception as e:
            raise RuntimeError(f"Failed to check/install MLX: {e}") from e

    async def generate(
        self,
        messages: list[MLXMessage],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Generate response from MLX model

        Args:
            messages: List of messages
            tools: Optional tool definitions

        Returns:
            Response dict with content and metadata
        """
        # Build prompt from messages
        prompt = self._build_prompt(messages, tools)

        # Run MLX inference
        try:
            # Use mlx-lm generate command
            cmd = [
                "python3", "-m", "mlx_lm.generate",
                "--model", self.config.model_name,
                "--prompt", prompt,
                "--max-tokens", str(self.config.max_tokens),
                "--temp", str(self.config.temperature),
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise RuntimeError(f"MLX inference failed: {stderr.decode()}") from None

            output = stdout.decode()

            # Parse response
            return {
                "content": output,
                "model": self.config.model_name,
                "usage": {
                    "prompt_tokens": len(prompt.split()),
                    "completion_tokens": len(output.split()),
                    "total_tokens": len(prompt.split()) + len(output.split()),
                }
            }

        except Exception as e:
            raise RuntimeError(f"MLX generation error: {e}") from e

    def _build_prompt(
        self,
        messages: list[MLXMessage],
        tools: list[dict[str, Any]] | None = None,
    ) -> str:
        """Build prompt from messages"""
        parts = []

        # Add system message
        system_msgs = [m for m in messages if m.role == "system"]
        if system_msgs:
            parts.append(f"System: {system_msgs[0].content}\n\n")

        # Add tool definitions if provided
        if tools:
            parts.append("Available Tools:\n")
            for tool in tools:
                parts.append(f"- {tool['name']}: {tool['description']}\n")
            parts.append("\n")

        # Add conversation
        for msg in messages:
            if msg.role == "user":
                parts.append(f"User: {msg.content}\n")
            elif msg.role == "assistant":
                parts.append(f"Assistant: {msg.content}\n")

        parts.append("Assistant: ")

        return "".join(parts)

    async def stream_generate(
        self,
        messages: list[MLXMessage],
        tools: list[dict[str, Any]] | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream generate response (for interactive use)
        """
        # For now, use non-streaming
        # MLX streaming would require more complex implementation
        response = await self.generate(messages, tools)
        yield response["content"]


class SimpleMLXClient:
    """
    Simplified MLX client using direct Python API
    More efficient than subprocess approach
    """

    def __init__(self, model_name: str = "mlx-community/Llama-3.2-3B-Instruct-4bit"):
        self.model_name = model_name
        self._model = None
        self._tokenizer = None

    def _load_model(self):
        """Load model and tokenizer"""
        if self._model is None:
            try:
                from mlx_lm import load

                print(f"Loading MLX model: {self.model_name}")
                self._model, self._tokenizer = load(self.model_name)
                print("✅ Model loaded successfully")

            except ImportError:
                raise RuntimeError(
                    "mlx-lm not installed. Run: pip install mlx-lm"
                ) from None

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate response"""
        self._load_model()

        from mlx_lm import generate

        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: generate(
                self._model,
                self._tokenizer,
                prompt=prompt,
                max_tokens=max_tokens,
                temp=temperature,
            )
        )

        return response

    async def chat(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Chat with the model"""
        # Build prompt from messages
        prompt_parts = []

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                prompt_parts.append(f"System: {content}\n\n")
            elif role == "user":
                prompt_parts.append(f"User: {content}\n")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}\n")

        prompt_parts.append("Assistant: ")
        prompt = "".join(prompt_parts)

        return await self.generate(prompt, max_tokens, temperature)
