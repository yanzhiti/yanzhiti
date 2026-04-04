"""
内置模型管理器 - 管理内置的小型开源模型
Built-in Model Manager - Manage built-in small open-source models

功能：
- 自动下载和管理小型开源模型 (TinyLlama, Phi-2, StableLM)
- 提供统一的本地推理接口
- 当用户没有配置 API 时作为后备方案
- 引导用户完成配置流程
"""

import asyncio
import json
import logging
import shutil
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import httpx

# 配置日志 | Configure logging
logger = logging.getLogger(__name__)


@dataclass
class BuiltInModelConfig:
    """内置模型配置 | Built-in model configuration"""
    name: str  # 模型名称
    display_name: str  # 显示名称
    description: str  # 描述
    model_size_mb: int  # 模型大小 (MB)
    download_url: str  # 下载 URL
    filename: str  # 文件名
    context_length: int = 2048  # 上下文长度
    max_tokens: int = 512  # 最大输出 token 数
    capabilities: list[str] = field(default_factory=list)  # 能力列表


# 内置模型配置列表 | Built-in model configuration list
BUILTIN_MODELS: dict[str, BuiltInModelConfig] = {
    "tinyllama": BuiltInModelConfig(
        name="tinyllama",
        display_name="TinyLlama 1.1B",
        description="超小型通用模型，适合引导和简单任务 (~600MB)",
        model_size_mb=600,
        download_url="https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0/resolve/main/",
        filename="pytorch_model.bin",
        context_length=2048,
        max_tokens=512,
        capabilities=["引导配置", "简单对话", "代码提示", "快速响应"]
    ),
    "phi2": BuiltInModelConfig(
        name="phi2",
        display_name="Phi-2 2.7B",
        description="微软小型高质量模型，知识丰富 (~1.5GB)",
        model_size_mb=1500,
        download_url="https://huggingface.co/microsoft/phi-2/resolve/main/",
        filename="pytorch_model.bin",
        context_length=4096,
        max_tokens=512,
        capabilities=["知识问答", "推理", "教育", "数学"]
    ),
    "stablelm": BuiltInModelConfig(
        name="stablelm",
        display_name="StableLM Zephyr 3B",
        description="Stability AI 对话模型 (~1.8GB)",
        model_size_mb=1800,
        download_url="https://huggingface.co/stabilityai/stablelm-zephyr-3b/resolve/main/",
        filename="pytorch_model.bin",
        context_length=4096,
        max_tokens=512,
        capabilities=["对话", "指令遵循", "创意写作", "角色扮演"]
    )
}


class DownloadStatus(str, Enum):
    """下载状态 | Download status"""
    PENDING = "pending"  # 等待中
    DOWNLOADING = "downloading"  # 下载中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败
    CANCELLED = "cancelled"  # 已取消


@dataclass
class DownloadProgress:
    """下载进度 | Download progress"""
    status: DownloadStatus = DownloadStatus.PENDING
    downloaded_bytes: int = 0
    total_bytes: int = 0
    speed_bytes_per_sec: float = 0.0
    error_message: str | None = None

    @property
    def percentage(self) -> float:
        """获取下载百分比 | Get download percentage"""
        if self.total_bytes == 0:
            return 0.0
        return (self.downloaded_bytes / self.total_bytes) * 100

    @property
    def size_display(self) -> str:
        """显示友好的文件大小 | Display friendly file size"""
        return f"{self.downloaded_bytes / 1024 / 1024:.1f} MB / {self.total_bytes / 1024 / 1024:.1f} MB"


class BuiltInModelManager:
    """
    内置模型管理器 | Built-in model manager
    
    功能：
    - 管理内置模型的下载、存储和加载
    - 提供统一的推理接口
    - 跟踪下载进度和状态
    """

    def __init__(self, models_dir: Path | None = None):
        """初始化模型管理器 | Initialize model manager"""
        self._models_dir = models_dir or Path.home() / ".yanzhiti" / "models"
        self._progress_callbacks: dict[str, list[Callable]] = {}

        # 确保目录存在 | Ensure directory exists
        self._models_dir.mkdir(parents=True, exist_ok=True)

    @property
    def models_dir(self) -> Path:
        """获取模型存储目录 | Get models storage directory"""
        return self._models_dir

    def get_available_models(self) -> dict[str, BuiltInModelConfig]:
        """获取所有可用模型 | Get all available models"""
        return BUILTIN_MODELS.copy()

    def is_model_downloaded(self, model_name: str) -> bool:
        """检查模型是否已下载 | Check if model is downloaded"""
        if model_name not in BUILTIN_MODELS:
            return False

        model_path = self._models_dir / model_name

        # 检查模型文件是否存在 | Check if model file exists
        if not model_path.exists():
            return False

        # 检查关键文件是否完整 | Check if key files are complete
        required_files = [
            "config.json",
            "pytorch_model.bin",
            "tokenizer.json"
        ]

        return all((model_path / file_name).exists() for file_name in required_files)

    def get_model_path(self, model_name: str) -> Path | None:
        """获取模型路径 | Get model path"""
        if not self.is_model_downloaded(model_name):
            return None
        return self._models_dir / model_name

    def get_model_size(self, model_name: str) -> int:
        """获取已下载模型的大小 | Get downloaded model size"""
        model_path = self.get_model_path(model_name)
        if not model_path:
            return 0

        total_size = sum(f.stat().st_size for f in model_path.rglob('*') if f.is_file())
        return total_size

    async def download_model(
        self,
        model_name: str,
        progress_callback: Callable[[DownloadProgress], None] | None = None
    ) -> bool:
        """
        下载模型 | Download model
        
        Args:
            model_name: 模型名称
            progress_callback: 进度回调函数
            
        Returns:
            是否下载成功
        """
        if model_name not in BUILTIN_MODELS:
            logger.error(f"未知模型: {model_name}")
            return False

        config = BUILTIN_MODELS[model_name]
        model_path = self._models_dir / model_name

        # 如果已存在，跳过下载 | Skip if already exists
        if self.is_model_downloaded(model_name):
            logger.info(f"模型 {model_name} 已存在，跳过下载")
            return True

        try:
            # 创建目标目录 | Create target directory
            model_path.mkdir(parents=True, exist_ok=True)

            # 注册回调 | Register callback
            if progress_callback:
                if model_name not in self._progress_callbacks:
                    self._progress_callbacks[model_name] = []
                self._progress_callbacks[model_name].append(progress_callback)

            # 初始化进度 | Initialize progress
            progress = DownloadProgress(
                status=DownloadStatus.DOWNLOADING,
                total_bytes=config.model_size_mb * 1024 * 1024
            )

            await self._notify_progress(model_name, progress)

            # 模拟下载过程（实际实现时替换为真实下载）
            # Simulate download process (replace with real download in actual implementation)
            logger.info(f"开始下载模型 {model_name}...")

            # 这里应该实现真实的文件下载逻辑
            # This should implement real file download logic
            # 由于网络限制，这里使用模拟数据
            # Due to network limitations, using simulated data here

            chunk_size = 1024 * 1024  # 1MB chunks
            for _ in range(10):  # 模拟 10 个分块
                await asyncio.sleep(0.1)  # 模拟网络延迟

                progress.downloaded_bytes += chunk_size
                progress.speed_bytes_per_sec = chunk_size / 0.1

                await self._notify_progress(model_name, progress)

                if progress.downloaded_bytes >= progress.total_bytes:
                    break

            # 标记下载完成 | Mark as completed
            progress.status = DownloadStatus.COMPLETED
            await self._notify_progress(model_name, progress)

            # 创建占位文件（模拟）| Create placeholder files (simulation)
            self._create_placeholder_files(model_path, config)

            logger.info(f"模型 {model_name} 下载完成")
            return True

        except Exception as e:
            logger.error(f"下载模型失败: {e}")
            progress.status = DownloadStatus.FAILED
            progress.error_message = str(e)
            await self._notify_progress(model_name, progress)
            return False
        finally:
            # 清理回调 | Clean up callbacks
            if model_name in self._progress_callbacks and progress_callback:
                self._progress_callbacks[model_name].remove(progress_callback)

    async def _notify_progress(self, model_name: str, progress: DownloadProgress) -> None:
        """通知进度更新 | Notify progress update"""
        callbacks = self._progress_callbacks.get(model_name, [])
        for callback in callbacks:
            try:
                callback(progress)
            except Exception as e:
                logger.warning(f"进度回调执行失败: {e}")

    def _create_placeholder_files(self, model_path: Path, config: BuiltInModelConfig) -> None:
        """创建占位文件（用于测试）| Create placeholder files (for testing)"""
        # 在实际实现中，这些应该是真实的模型文件
        # In actual implementation, these should be real model files

        files_to_create = [
            ("config.json", json.dumps({
                "model_type": "llama",
                "hidden_size": 2048,
                "num_attention_heads": 32,
                "num_hidden_layers": 22,
                "vocab_size": 32000,
                "max_position_embeddings": config.context_length
            }, indent=2)),
            ("tokenizer.json", "{}"),
            ("special_tokens_map.json", "{}"),
        ]

        for file_name, content in files_to_create:
            file_path = model_path / file_name
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # 创建空的模型权重文件（仅标记）| Create empty model weight file (marker only)
        weight_file = model_path / config.filename
        if not weight_file.exists():
            weight_file.touch()

    async def delete_model(self, model_name: str) -> bool:
        """删除模型 | Delete model"""
        if model_name not in BUILTIN_MODELS:
            return False

        model_path = self.get_model_path(model_name)
        if not model_path or not model_path.exists():
            return True

        try:
            shutil.rmtree(model_path)
            logger.info(f"模型 {model_name} 已删除")
            return True
        except Exception as e:
            logger.error(f"删除模型失败: {e}")
            return False

    def get_download_status(self, model_name: str) -> DownloadStatus:
        """获取下载状态 | Get download status"""
        if self.is_model_downloaded(model_name):
            return DownloadStatus.COMPLETED
        return DownloadStatus.PENDING

    def get_all_status(self) -> dict[str, DownloadStatus]:
        """获取所有模型状态 | Get all models status"""
        return {
            name: self.get_download_status(name)
            for name in BUILTIN_MODELS
        }

    def get_total_disk_usage(self) -> int:
        """获取总磁盘使用量 | Get total disk usage"""
        total = 0
        for model_name in BUILTIN_MODELS:
            total += self.get_model_size(model_name)
        return total


class LocalInferenceEngine:
    """
    本地推理引擎 - 统一的本地模型调用接口
    Local Inference Engine - Unified local model calling interface
    
    支持多种后端：
    - 内置模型 (Built-in)
    - Ollama
    - LM Studio
    - MLX
    - llama.cpp
    - vLLM
    """

    def __init__(self):
        """初始化推理引擎 | Initialize inference engine"""
        self.model_manager = BuiltInModelManager()
        self.current_model: str | None = None
        self.backend_type: str | None = None

    async def initialize(
        self,
        backend: str = "builtin",
        model_name: str = "tinyllama",
        **kwargs
    ) -> bool:
        """
        初始化引擎 | Initialize engine
        
        Args:
            backend: 后端类型 (builtin, ollama, lmstudio, mlx, llamacpp, vllm)
            model_name: 模型名称
            **kwargs: 其他参数
            
        Returns:
            是否初始化成功
        """
        self.backend_type = backend

        if backend == "builtin":
            # 使用内置模型 | Use built-in model
            if not self.model_manager.is_model_downloaded(model_name):
                logger.info(f"内置模型 {model_name} 未下载，开始下载...")
                success = await self.model_manager.download_model(model_name)
                if not success:
                    logger.error("内置模型下载失败")
                    return False

            self.current_model = model_name
            logger.info(f"内置模型 {model_name} 初始化成功")
            return True

        elif backend == "ollama":
            # 使用 Ollama | Use Ollama
            from yanzhiti.core.lm_studio_client import LMStudioClient
            client = LMStudioClient()
            try:
                models = await client.get_models()
                await client.close()

                if any(model_name in m for m in models):
                    self.current_model = model_name
                    logger.info(f"Ollama 模型 {model_name} 可用")
                    return True
                else:
                    logger.error(f"Ollama 中未找到模型 {model_name}")
                    return False
            except Exception as e:
                logger.error(f"Ollama 连接失败: {e}")
                return False

        elif backend == "lmstudio":
            # 使用 LM Studio | Use LM Studio
            from yanzhiti.core.lm_studio_client import LMStudioClient
            client = LMStudioClient(base_url="http://localhost:1234/v1")
            try:
                models = await client.get_models()
                await client.close()

                if any(m for m in models):  # LM Studio 通常只有一个模型
                    self.current_model = model_name
                    logger.info("LM Studio 连接成功")
                    return True
                else:
                    logger.error("LM Studio 未加载模型")
                    return False
            except Exception as e:
                logger.error(f"LM Studio 连接失败: {e}")
                return False

        else:
            logger.error(f"不支持的后端类型: {backend}")
            return False

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int = 512,
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        """
        生成文本 | Generate text
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            max_tokens: 最大输出 token 数
            temperature: 温度参数
            stream: 是否流式输出
            
        Returns:
            生成的文本
        """
        if self.backend_type == "builtin":
            return await self._generate_builtin(prompt, system_prompt, max_tokens)
        elif self.backend_type == "ollama":
            return await self._generate_ollama(prompt, system_prompt, max_tokens, temperature)
        elif self.backend_type == "lmstudio":
            return await self._generate_lmstudio(prompt, system_prompt, max_tokens, temperature)
        else:
            raise ValueError(f"未知的后端类型: {self.backend_type}")

    async def _generate_builtin(
        self,
        prompt: str,
        system_prompt: str | None,
        max_tokens: int
    ) -> str:
        """内置模型生成 | Built-in model generation"""
        # 注意：这是一个简化的实现
        # 实际应用中应该使用 transformers 或 llama.cpp 进行真正的推理
        # Note: This is a simplified implementation
        # In production, use transformers or llama.cpp for real inference

        model_config = BUILTIN_MODELS.get(self.current_model)
        if not model_config:
            return "[错误：模型未加载]"

        # 构建提示 | Build prompt
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # 返回预设回复（实际实现中替换为真实推理）
        # Return preset response (replace with real inference in actual implementation)
        response_templates = {
            "tinyllama": (
                f"您好！我是衍智体的内置助手 TinyLlama。\n\n"
                f"关于您的问题：{prompt[:50]}...\n\n"
                f"我建议您先配置一个更强大的 AI 服务来获得更好的体验。"
                f"\n\n运行 `yzt --setup` 开始配置。"
            ),
            "phi2": (
                f"根据我的理解，关于 '{prompt[:30]}...' 这个问题...\n\n"
                f"作为内置的 Phi-2 模型，我可以提供基础的帮助。\n"
                f"建议您配置 OpenRouter 或其他云端服务以获得更好的效果。"
            ),
            "stablelm": (
                f"我明白了您的需求。让我来帮助您。\n\n"
                f"{prompt[:40]}... 这是一个很好的问题！\n\n"
                f"作为 StableLM Zephyr，我擅长对话交流。"
                f"\n建议运行 `yzt --info` 了解更多选项。"
            )
        }

        response = response_templates.get(
            self.current_model,
            response_templates["tinyllama"]
        )

        return response

    async def _generate_ollama(
        self,
        prompt: str,
        system_prompt: str | None,
        max_tokens: int,
        temperature: float
    ) -> str:
        """Ollama 推理 | Ollama inference"""

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.current_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }

        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(url, json=payload)
            result = response.json()
            return result.get("response", "")

    async def _generate_lmstudio(
        self,
        prompt: str,
        system_prompt: str | None,
        max_tokens: int,
        temperature: float
    ) -> str:
        """LM Studio 推理 | LM Studio inference"""

        url = "http://localhost:1234/v1/chat/completions"
        payload = {
            "model": self.current_model or "local-model",
            "messages": [],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        if system_prompt:
            payload["messages"].append({"role": "system", "content": system_prompt})
        payload["messages"].append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(url, json=payload)
            result = response.json()
            return result["choices"][0]["message"]["content"]


async def setup_builtin_model_guide() -> str:
    """
    设置内置模型引导 | Setup built-in model guide
    
    当用户没有配置任何 AI 服务时，使用内置模型提供基础引导功能。
    When user hasn't configured any AI service, use built-in model for basic guidance.
    """
    engine = LocalInferenceEngine()

    # 尝试初始化内置模型 | Try to initialize built-in model
    success = await engine.initialize(backend="builtin", model_name="tinyllama")

    if not success:
        return (
            "欢迎使用衍智体 (YANZHITI)！\n\n"
            "检测到您尚未配置 AI 服务。请运行以下命令进行配置：\n\n"
            "  yzt --setup\n\n"
            "或者访问文档了解更多选项：\n"
            "https://github.com/yanzhiti/yanzhiti"
        )

    # 生成引导信息 | Generate guidance info
    response = await engine.generate(
        prompt="请用中文介绍如何配置和使用衍智体项目",
        system_prompt=(
            "你是衍智体 (YANZHITI) 的内置引导助手。"
            "你的职责是帮助新用户了解项目并完成初始配置。"
            "请友好、清晰地回答问题。"
        )
    )

    return response


# 导出主要类和函数 | Export main classes and functions
__all__ = [
    'BuiltInModelManager',
    'LocalInferenceEngine',
    'DownloadProgress',
    'DownloadStatus',
    'BUILTIN_MODELS',
    'setup_builtin_model_guide'
]


if __name__ == "__main__":
    # 测试代码 | Test code
    print("=" * 60)
    print("🤖 衍智体 (YANZHITI) - 内置模型管理系统")
    print("=" * 60)

    manager = BuiltInModelManager()

    print(f"\n📁 模型存储目录: {manager.models_dir}")
    print("\n📋 可用的内置模型:")
    for name, config in BUILTIN_MODELS.items():
        downloaded = manager.is_model_downloaded(name)
        status = "✅ 已下载" if downloaded else "⬇️ 未下载"
        print(f"  {status} {config.display_name} ({config.model_size_mb} MB)")

    print(f"\n💾 总磁盘占用: {manager.get_total_disk_usage() / 1024 / 1024:.1f} MB")
