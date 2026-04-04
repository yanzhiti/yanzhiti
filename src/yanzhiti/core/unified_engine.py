"""
统一 AI 引擎 - 支持所有供应商和本地模型
Unified AI Engine - Support all providers and local models

功能：
- 统一调用云端 API 和本地模型
- 自动选择最佳后端
- 智能降级（API 不可用时使用本地模型）
- 内置模型作为后备方案
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from yanzhiti.core.builtin_models import (
    BuiltInModelManager,
    LocalInferenceEngine,
)

# 导入供应商配置 | Import provider configuration
from yanzhiti.core.providers import (
    ALL_PROVIDERS,
    ProviderType,
    get_provider,
)

# 配置日志 | Configure logging
logger = logging.getLogger(__name__)


class BackendPriority(str, Enum):
    """后端优先级 | Backend priority"""

    CLOUD = "cloud"  # 云端 API 优先
    LOCAL = "local"  # 本地模型优先
    BUILTIN = "builtin"  # 仅使用内置模型
    AUTO = "auto"  # 自动选择


@dataclass
class EngineConfig:
    """引擎配置 | Engine configuration"""

    primary_backend: str = "openrouter"  # 主后端 (provider ID)
    fallback_backends: list[str] = field(default_factory=lambda: ["builtin"])  # 后备后端
    api_key: str | None = None  # API 密钥
    base_url: str | None = None  # 自定义基础 URL
    model: str | None = None  # 模型名称
    temperature: float = 0.7  # 温度参数
    max_tokens: int = 4096  # 最大 token 数
    priority: BackendPriority = BackendPriority.AUTO  # 后端优先级


class UnifiedAIEngine:
    """
    统一 AI 引擎 | Unified AI engine

    特点：
    - 统一调用接口，支持所有供应商和本地模型
    - 自动故障转移（failover）
    - 内置模型作为最终后备
    - 配置简单，开箱即用
    """

    def __init__(self, config: EngineConfig | None = None):
        """初始化引擎 | Initialize engine"""
        self.config = config or EngineConfig()
        self._local_engine = LocalInferenceEngine()
        self._builtin_manager = BuiltInModelManager()

        # 可用的后端状态 | Available backend status
        self._backend_status: dict[str, bool] = {}

    async def initialize(self) -> bool:
        """
        初始化引擎 | Initialize engine

        尝试初始化配置的后端，并检查可用性。
        Try to initialize configured backends and check availability.
        """
        logger.info("正在初始化统一 AI 引擎...")

        # 初始化本地推理引擎 | Initialize local inference engine
        try:
            await self._local_engine.initialize(backend="builtin", model_name="tinyllama")
            self._backend_status["builtin"] = True
            logger.info("✅ 内置模型就绪")
        except Exception as e:
            logger.warning(f"⚠️ 内置模型初始化失败: {e}")
            self._backend_status["builtin"] = False

        # 检查 Ollama 是否可用 | Check if Ollama is available
        try:
            ollama_available = await self._check_ollama()
            self._backend_status["ollama"] = ollama_available
            if ollama_available:
                logger.info("✅ Ollama 就绪")
        except Exception as e:
            logger.warning(f"⚠️ Ollama 检查失败: {e}")
            self._backend_status["ollama"] = False

        # 检查 LM Studio 是否可用 | Check if LM Studio is available
        try:
            lmstudio_available = await self._check_lmstudio()
            self._backend_status["lmstudio"] = lmstudio_available
            if lmstudio_available:
                logger.info("✅ LM Studio 就绪")
        except Exception as e:
            logger.warning(f"⚠️ LM Studio 检查失败: {e}")
            self._backend_status["lmstudio"] = False

        # 检查云端 API 配置 | Check cloud API configuration
        if self.config.api_key and self.config.primary_backend != "builtin":
            provider = get_provider(self.config.primary_backend)
            if provider and provider.provider_type == ProviderType.CLOUD:
                self._backend_status[self.config.primary_backend] = True
                logger.info(f"✅ {provider.display_name} 已配置")

        logger.info("AI 引擎初始化完成")
        return True

    async def _check_ollama(self) -> bool:
        """检查 Ollama 是否可用 | Check if Ollama is available"""
        import httpx

        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get("http://localhost:11434/api/tags")
                return response.status_code == 200
        except Exception:
            return False

    async def _check_lmstudio(self) -> bool:
        """检查 LM Studio 是否可用 | Check if LM Studio is available"""
        import httpx

        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get("http://localhost:1234/v1/models")
                return response.status_code == 200
        except Exception:
            return False

    def get_available_backends(self) -> dict[str, bool]:
        """获取可用后端列表 | Get available backends list"""
        return self._backend_status.copy()

    async def query(
        self,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        preferred_backend: str | None = None,
    ) -> str:
        """
        执行查询 | Execute query

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            max_tokens: 最大输出 token 数
            temperature: 温度参数
            preferred_backend: 首选后端

        Returns:
            生成的回复文本
        """
        # 使用配置的默认值或传入的值 | Use config defaults or passed values
        max_tokens = max_tokens or self.config.max_tokens
        temperature = temperature or self.config.temperature

        # 确定后端顺序 | Determine backend order
        backends_to_try = self._get_backend_order(preferred_backend)

        errors = []

        for backend_name in backends_to_try:
            try:
                logger.info(f"尝试使用后端: {backend_name}")

                result = await self._query_with_backend(
                    backend_name, prompt, system_prompt, max_tokens, temperature
                )

                return result

            except Exception as e:
                error_msg = f"{backend_name}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"后端 {backend_name} 失败: {e}")
                continue

        # 所有后端都失败 | All backends failed
        error_summary = "\n".join([f"  ❌ {err}" for err in errors])
        raise RuntimeError(
            f"所有 AI 后端都不可用：\n{error_summary}\n\n"
            f"建议：\n"
            f"  1. 运行 `yzt --setup` 配置 API\n"
            f"  2. 安装 Ollama 或 LM Studio\n"
            f"  3. 检查网络连接"
        )

    def _get_backend_order(self, preferred: str | None) -> list[str]:
        """获取后端尝试顺序 | Get backend trial order"""
        order = [preferred] if preferred else []

        # 根据优先级模式添加后端 | Add backends based on priority mode
        if self.config.priority == BackendPriority.CLOUD:
            # 云端优先 | Cloud first
            if self.config.primary_backend not in order:
                order.append(self.config.primary_backend)
            order.extend(["ollama", "lmstudio", "builtin"])

        elif self.config.priority == BackendPriority.LOCAL:
            # 本地优先 | Local first
            order.extend(["ollama", "lmstudio"])
            if self.config.primary_backend not in order:
                order.append(self.config.primary_backend)
            order.append("builtin")

        elif self.config.priority == BackendPriority.BUILTIN:
            # 仅内置模型 | Built-in only
            order = ["builtin"]

        else:  # AUTO
            # 自动选择 | Auto select
            # 有 API Key 时优先云端 | Prefer cloud when has API key
            if (
                self.config.api_key
                and self.config.primary_backend != "builtin"
                and self.config.primary_backend not in order
            ):
                order.append(self.config.primary_backend)

            # 然后尝试本地 | Then try local
            for local_backend in ["ollama", "lmstudio"]:
                if local_backend not in order and self._backend_status.get(local_backend, False):
                    order.append(local_backend)

            # 最后使用内置模型 | Finally use built-in
            if "builtin" not in order:
                order.append("builtin")

        return order

    async def _query_with_backend(
        self,
        backend_name: str,
        prompt: str,
        system_prompt: str | None,
        max_tokens: int,
        temperature: float,
    ) -> str:
        """使用指定后端执行查询 | Execute query with specified backend"""

        if backend_name == "builtin":
            return await self._query_builtin(prompt, system_prompt, max_tokens)

        elif backend_name == "ollama":
            return await self._query_ollama(prompt, system_prompt, max_tokens, temperature)

        elif backend_name == "lmstudio":
            return await self._query_lmstudio(prompt, system_prompt, max_tokens, temperature)

        elif backend_name in ALL_PROVIDERS:
            return await self._query_cloud_api(
                backend_name, prompt, system_prompt, max_tokens, temperature
            )

        else:
            raise ValueError(f"未知的后端: {backend_name}")

    async def _query_builtin(self, prompt: str, system_prompt: str | None, max_tokens: int) -> str:
        """内置模型查询 | Built-in model query"""
        return await self._local_engine.generate(
            prompt=prompt, system_prompt=system_prompt, max_tokens=max_tokens
        )

    async def _query_ollama(
        self, prompt: str, system_prompt: str | None, max_tokens: int, temperature: float
    ) -> str:
        """Ollama 查询 | Ollama query"""
        import httpx

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.config.model or "llama3.1:8b",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": min(max_tokens, 8192)},
        }

        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")

    async def _query_lmstudio(
        self, prompt: str, system_prompt: str | None, max_tokens: int, temperature: float
    ) -> str:
        """LM Studio 查询 | LM Studio query"""
        import httpx

        url = "http://localhost:1234/v1/chat/completions"
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.config.model or "local-model",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

    async def _query_cloud_api(
        self,
        provider_id: str,
        prompt: str,
        system_prompt: str | None,
        max_tokens: int,
        temperature: float,
    ) -> str:
        """云端 API 查询 | Cloud API query"""
        import httpx

        provider = get_provider(provider_id)
        if not provider:
            raise ValueError(f"未知供应商: {provider_id}")

        base_url = self.config.base_url or provider.base_url

        # 构建请求 | Build request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.config.model or provider.models[0].name if provider.models else "default",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        # 根据供应商调整 URL | Adjust URL based on provider
        if provider_id == "anthropic":
            # Anthropic 使用不同的 API 格式 | Anthropic uses different API format
            url = f"{base_url}/v1/messages"
            payload["max_tokens"] = min(max_tokens, 4096)
        else:
            # OpenAI 兼容格式 | OpenAI compatible format
            url = f"{base_url}/chat/completions"

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # 解析响应 | Parse response
            if provider_id == "anthropic":
                return result.get("content", [{}])[0].get("text", "")
            else:
                return result["choices"][0]["message"]["content"]

    async def stream_query(self, prompt: str, system_prompt: str | None = None, **kwargs) -> Any:
        """
        流式查询 | Streaming query

        生成器形式返回文本块。
        Returns text chunks in generator form.
        """
        # TODO: 实现流式输出
        # TODO: Implement streaming output
        result = await self.query(prompt, system_prompt, **kwargs)
        yield result

    def get_info(self) -> dict[str, Any]:
        """获取引擎信息 | Get engine information"""
        return {
            "version": "2.0.0",
            "config": {
                "primary_backend": self.config.primary_backend,
                "model": self.config.model,
                "priority": self.config.priority.value,
            },
            "backends": self._backend_status,
            "available_providers": len(ALL_PROVIDERS),
            "builtin_models_downloaded": [
                name
                for name, status in self._builtin_manager.get_all_status().items()
                if status.value == "completed"
            ],
        }


# 工厂函数 | Factory function
def create_engine(**kwargs) -> UnifiedAIEngine:
    """创建统一 AI 引擎 | Create unified AI engine"""
    config = EngineConfig(**kwargs)
    return UnifiedAIEngine(config)


async def quick_test() -> None:
    """快速测试 | Quick test"""
    print("=" * 60)
    print("🤖 衍智体 (YANZHITI) - 统一 AI 引擎测试")
    print("=" * 60)

    engine = create_engine()

    # 初始化 | Initialize
    print("\n📦 正在初始化引擎...")
    await engine.initialize()

    # 显示信息 | Show info
    info = engine.get_info()
    print(f"\n🔧 引擎版本: {info['version']}")
    print("\n🌐 可用后端:")
    for backend, available in info["backends"].items():
        status = "✅" if available else "❌"
        print(f"  {status} {backend}")

    # 测试查询 | Test query
    print("\n💬 测试查询:")
    try:
        response = await engine.query("你好，请简短介绍你自己")
        print(f"\n🤖 回复:\n{response[:200]}...\n")
    except Exception as e:
        print(f"\n❌ 查询失败: {e}")


if __name__ == "__main__":
    asyncio.run(quick_test())
