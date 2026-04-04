"""
AI 提供商配置 - 包含所有主流和免费供应商
AI Provider Configuration - Including all mainstream and free providers
"""

from dataclasses import dataclass, field
from enum import Enum


class ProviderType(str, Enum):
    """供应商类型 | Provider type"""

    CLOUD = "cloud"  # 云端 API
    LOCAL = "local"  # 本地模型
    BUILTIN = "builtin"  # 内置模型


@dataclass
class ModelInfo:
    """模型信息 | Model information"""

    name: str  # 模型名称
    display_name: str  # 显示名称
    description: str  # 描述
    context_window: int = 4096  # 上下文窗口大小
    max_output: int = 2048  # 最大输出长度
    is_free: bool = False  # 是否免费
    requires_api_key: bool = True  # 是否需要 API Key
    input_price: float = 0.0  # 输入价格 (每百万token)
    output_price: float = 0.0  # 输出价格 (每百万token)
    capabilities: list[str] = field(default_factory=list)  # 能力列表


@dataclass
class AIProvider:
    """AI 提供商 | AI provider"""

    name: str  # 名称
    display_name: str  # 显示名称
    description: str  # 描述
    provider_type: ProviderType  # 类型
    base_url: str  # API 基础 URL
    signup_url: str  # 注册 URL
    docs_url: str  # 文档 URL
    models: list[ModelInfo] = field(default_factory=list)  # 模型列表
    features: list[str] = field(default_factory=list)  # 特性列表
    has_free_tier: bool = False  # 是否有免费层
    recommended: bool = False  # 是否推荐给新手


# ============================================================
# 🌐 云端 API 供应商 | Cloud API Providers
# ============================================================

# OpenRouter - 统一 API 接口（推荐）
OPENROUTER = AIProvider(
    name="openrouter",
    display_name="OpenRouter",
    description="统一访问 100+ AI 模型的 API 聚合平台",
    provider_type=ProviderType.CLOUD,
    base_url="https://openrouter.ai/api/v1",
    signup_url="https://openrouter.ai/keys",
    docs_url="https://openrouter.ai/docs",
    has_free_tier=True,
    recommended=True,
    features=["100+ 模型支持", "统一 API 格式", "按量付费", "免费额度", "无速率限制"],
    models=[
        ModelInfo(
            name="anthropic/claude-3.5-sonnet",
            display_name="Claude 3.5 Sonnet",
            description="Anthropic 最新旗舰模型，推理能力强",
            context_window=200000,
            max_output=8192,
            is_free=False,
            input_price=3.0,
            output_price=15.0,
            capabilities=["代码生成", "推理", "长文本"],
        ),
        ModelInfo(
            name="openai/gpt-4o",
            display_name="GPT-4o",
            description="OpenAI 多模态旗舰模型",
            context_window=128000,
            max_output=4096,
            is_free=False,
            input_price=2.5,
            output_price=10.0,
            capabilities=["多模态", "代码", "推理"],
        ),
        ModelInfo(
            name="deepseek/deepseek-chat-v3-0324",
            display_name="DeepSeek V3",
            description="DeepSeek 开源旗舰模型，性价比极高",
            context_window=65536,
            max_output=8192,
            is_free=True,
            input_price=0.14,
            output_price=0.28,
            capabilities=["中文优化", "代码", "数学"],
        ),
        ModelInfo(
            name="google/gemini-pro-1.5",
            display_name="Gemini Pro 1.5",
            description="Google 最新多模态模型",
            context_window=2800000,
            max_output=8192,
            is_free=True,
            input_price=0.0,
            output_price=0.0,
            capabilities=["超长上下文", "多模态", "免费"],
        ),
        ModelInfo(
            name="meta-llama/llama-3.1-70b-instruct",
            display_name="Llama 3.1 70B",
            description="Meta 开源大模型，本地部署友好",
            context_window=131072,
            max_output=2048,
            is_free=False,
            input_price=0.52,
            output_price=0.75,
            capabilities=["开源", "多语言", "长文本"],
        ),
        ModelInfo(
            name="qwen/qwen-2.5-72b-instruct",
            display_name="Qwen 2.5 72B",
            description="阿里通义千问最新版本",
            context_window=131072,
            max_output=2048,
            is_free=False,
            input_price=0.36,
            output_price=0.72,
            capabilities=["中文优化", "数学", "代码"],
        ),
        ModelInfo(
            name="mistralai/mistral-large-2407",
            display_name="Mistral Large 2407",
            description="Mistral AI 最新旗舰模型",
            context_window=131072,
            max_output=8192,
            is_free=False,
            input_price=2.0,
            output_price=6.0,
            capabilities=["多语言", "代码", "推理"],
        ),
    ],
)

# OpenAI 官方
OPENAI = AIProvider(
    name="openai",
    display_name="OpenAI",
    description="GPT 系列模型的官方提供者",
    provider_type=ProviderType.CLOUD,
    base_url="https://api.openai.com/v1",
    signup_url="https://platform.openai.com/api-keys",
    docs_url="https://platform.openai.com/docs",
    has_free_tier=False,
    recommended=True,
    features=[
        "GPT-4o / GPT-4 Turbo",
        "DALL-E 图像生成",
        "Whisper 语音识别",
        "TTS 文字转语音",
        "Function Calling",
    ],
    models=[
        ModelInfo(
            name="gpt-4o",
            display_name="GPT-4o",
            description="最先进的多模态模型",
            context_window=128000,
            max_output=16384,
            is_free=False,
            input_price=2.5,
            output_price=10.0,
        ),
        ModelInfo(
            name="gpt-4-turbo",
            display_name="GPT-4 Turbo",
            description="高性能 GPT-4 版本",
            context_window=128000,
            max_output=4096,
            is_free=False,
            input_price=1.0,
            output_price=3.0,
        ),
        ModelInfo(
            name="gpt-3.5-turbo",
            display_name="GPT-3.5 Turbo",
            description="高性价比的快速响应模型",
            context_window=16385,
            max_output=4096,
            is_free=False,
            input_price=0.35,
            output_price=1.05,
        ),
        ModelInfo(
            name="o1-mini",
            display_name="o1 Mini",
            description="OpenAI 推理模型",
            context_window=200000,
            max_output=100000,
            is_free=False,
            input_price=1.1,
            output_price=4.4,
            capabilities=["推理", "数学", "编程"],
        ),
    ],
)

# Anthropic 官方
ANTHROPIC = AIProvider(
    name="anthropic",
    display_name="Anthropic",
    description="Claude 系列模型，以安全和长文本著称",
    provider_type=ProviderType.CLOUD,
    base_url="https://api.anthropic.com",
    signup_url="https://console.anthropic.com/settings/keys",
    docs_url="https://docs.anthropic.com",
    has_free_tier=True,
    recommended=True,
    features=[
        "Claude 3.5 Sonnet (推荐)",
        "Claude 3 Opus/Haiku",
        "200K 上下文窗口",
        "安全对齐",
        "工具使用能力",
    ],
    models=[
        ModelInfo(
            name="claude-3-5-sonnet-20241022",
            display_name="Claude 3.5 Sonnet",
            description="当前最强开源级别模型",
            context_window=200000,
            max_output=8192,
            is_free=False,
            input_price=3.0,
            output_price=15.0,
        ),
        ModelInfo(
            name="claude-3-opus-20240229",
            display_name="Claude 3 Opus",
            description="最强大的 Claude 模型",
            context_window=200000,
            max_output=4096,
            is_free=False,
            input_price=15.0,
            output_price=75.0,
        ),
        ModelInfo(
            name="claude-3-haiku-20240307",
            display_name="Claude 3 Haiku",
            description="快速且经济的 Claude 模型",
            context_window=200000,
            max_output=4096,
            is_free=True,
            input_price=0.25,
            output_price=1.25,
        ),
    ],
)

# Google (Gemini)
GOOGLE = AIProvider(
    name="google",
    display_name="Google (Gemini)",
    description="Google Gemini 系列模型，支持超长上下文",
    provider_type=ProviderType.CLOUD,
    base_url="https://generativelanguage.googleapis.com/v1beta",
    signup_url="https://aistudio.google.com/app/apikey",
    docs_url="https://ai.google.dev/docs",
    has_free_tier=True,
    recommended=True,
    features=[
        "Gemini 1.5 Pro/Flash",
        "280万 token 超长上下文",
        "完全免费使用",
        "原生多模态",
        "Grounding 功能",
    ],
    models=[
        ModelInfo(
            name="gemini-1.5-pro",
            display_name="Gemini 1.5 Pro",
            description="Google 最强模型，支持 280 万 token",
            context_window=2800000,
            max_output=8192,
            is_free=True,
            input_price=0.0,
            output_price=0.0,
        ),
        ModelInfo(
            name="gemini-1.5-flash",
            display_name="Gemini 1.5 Flash",
            description="快速响应的轻量级模型",
            context_window=1048576,
            max_output=8192,
            is_free=True,
            input_price=0.0,
            output_price=0.0,
        ),
        ModelInfo(
            name="gemini-2.0-flash-exp",
            display_name="Gemini 2.0 Flash (实验)",
            description="下一代 Gemini 模型",
            context_window=1048576,
            max_output=8192,
            is_free=True,
            input_price=0.0,
            output_price=0.0,
        ),
    ],
)

# DeepSeek (深度求索)
DEEPSEEK = AIProvider(
    name="deepseek",
    display_name="DeepSeek",
    description="中国领先的开源 AI 公司，专注推理和代码",
    provider_type=ProviderType.CLOUD,
    base_url="https://api.deepseek.com",
    signup_url="https://platform.deepseek.com/",
    docs_url="https://platform.deepseek.com/api-docs",
    has_free_tier=True,
    recommended=True,
    features=[
        "DeepSeek V3/R1 系列",
        "极低价格 ($0.14/M tokens)",
        "中文理解优秀",
        "数学/代码能力强",
        "开源可商用",
    ],
    models=[
        ModelInfo(
            name="deepseek-chat",
            display_name="DeepSeek V3",
            description="主流对话模型，性价比极高",
            context_window=65536,
            max_output=8192,
            is_free=True,
            input_price=0.14,
            output_price=0.28,
        ),
        ModelInfo(
            name="deepseek-reasoner",
            display_name="DeepSeek R1",
            description="推理专用模型，思维链输出",
            context_window=65536,
            max_output=8192,
            is_free=True,
            input_price=0.55,
            output_price=2.19,
            capabilities=["推理", "思维链", "数学证明"],
        ),
    ],
)

# 阿里通义千问 (Qwen)
QWEN = AIProvider(
    name="qwen",
    display_name="通义千问 (Qwen)",
    description="阿里云 AI 平台，中文优化",
    provider_type=ProviderType.CLOUD,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    signup_url="https://dashscope.console.aliyun.com/apiKey",
    docs_url="https://help.aliyun.com/zh/dashscope/",
    has_free_tier=True,
    features=["Qwen 2.5 系列", "中文理解顶级", "视觉理解", "语音合成", "国产合规"],
    models=[
        ModelInfo(
            name="qwen-max",
            display_name="Qwen Max",
            description="阿里最强模型",
            context_window=32768,
            max_output=8192,
            is_free=True,
            input_price=0.36,
            output_price=0.72,
        ),
        ModelInfo(
            name="qwen-plus",
            display_name="Qwen Plus",
            description="均衡性能与成本",
            context_window=131072,
            max_output=8192,
            is_free=True,
            input_price=0.24,
            output_price=0.48,
        ),
        ModelInfo(
            name="qwen-turbo",
            display_name="Qwen Turbo",
            description="快速响应模型",
            context_window=131072,
            max_output=8192,
            is_free=True,
            input_price=0.12,
            output_price=0.24,
        ),
    ],
)

# 百度文心一言 (ERNIE)
BAIDU = AIProvider(
    name="baidu",
    display_name="百度文心一言 (ERNIE)",
    description="百度 AI 平台，中文场景优化",
    provider_type=ProviderType.CLOUD,
    base_url="https://qianfan.baidubce.com/v2",
    signup_url="https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application",
    docs_url="https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html",
    has_free_tier=True,
    features=["ERNIE 4.0 系列", "中文理解强", "知识增强", "搜索集成", "国产合规"],
    models=[
        ModelInfo(
            name="ernie-4.0-8k",
            display_name="ERNIE 4.0 8K",
            description="百度最新旗舰模型",
            context_window=8192,
            max_output=2048,
            is_free=True,
            input_price=0.24,
            output_price=0.96,
        ),
        ModelInfo(
            name="ernie-speed-8k",
            display_name="ERNIE Speed 8K",
            description="快速响应模型",
            context_window=8192,
            max_output=2048,
            is_free=True,
            input_price=0.08,
            output_price=0.32,
        ),
    ],
)

# Mistral AI
MISTRAL = AIProvider(
    name="mistral",
    display_name="Mistral AI",
    description="欧洲 AI 独角兽，高效能模型",
    provider_type=ProviderType.CLOUD,
    base_url="https://api.mistral.ai/v1",
    signup_url="https://console.mistral.ai/api-keys/",
    docs_url="https://docs.mistral.ai/",
    has_free_tier=True,
    features=["Mistral Large 2407", "Mixtral MoE 架构", "Codestral 代码模型", "欧洲数据合规"],
    models=[
        ModelInfo(
            name="mistral-large-latest",
            display_name="Mistral Large",
            description="最新旗舰模型",
            context_window=131072,
            max_output=8192,
            is_free=False,
            input_price=2.0,
            output_price=6.0,
        ),
        ModelInfo(
            name="codestral-latest",
            display_name="Codestral",
            description="代码专用模型",
            context_window=32768,
            max_output=8192,
            is_free=False,
            input_price=1.0,
            output_price=3.0,
            capabilities=["80+ 语言", "代码补全", "Fill-Middle"],
        ),
    ],
)

# Groq (超快推理)
GROQ = AIProvider(
    name="groq",
    display_name="Groq",
    description="超高速 AI 推理芯片，免费使用",
    provider_type=ProviderType.CLOUD,
    base_url="https://api.groq.com/openai/v1",
    signup_url="https://console.groq.com/keys",
    docs_url="https://groq.com/docs",
    has_free_tier=True,
    recommended=True,
    features=[
        "超快推理速度 (500+ tok/s)",
        "完全免费使用",
        "Llama 3.1/Mixtral",
        "实时流式输出",
        "低延迟 API",
    ],
    models=[
        ModelInfo(
            name="llama-3.1-70b-versatile",
            display_name="Llama 3.1 70B (Groq)",
            description="在 Groq 上运行的超快 Llama",
            context_window=131072,
            max_output=8192,
            is_free=True,
            input_price=0.0,
            output_price=0.0,
        ),
        ModelInfo(
            name="mixtral-8x7b-32768",
            display_name="Mixtral 8x7B (Groq)",
            description="MoE 架构，多专家协作",
            context_window=32768,
            max_output=8192,
            is_free=True,
            input_price=0.0,
            output_price=0.0,
        ),
    ],
)

# Together AI
TOGETHER = AIProvider(
    name="together",
    display_name="Together AI",
    description="开源模型云端推理服务",
    provider_type=ProviderType.CLOUD,
    base_url="https://api.together.xyz/v1",
    signup_url="https://api.together.xyz/settings/api-keys",
    docs_url="https://docs.together.xyz/",
    has_free_tier=True,
    features=["开源模型托管", "按量付费", "GPU 加速推理", "企业级可靠性"],
    models=[
        ModelInfo(
            name="meta-llama/Llama-V3-Free-Instruct-80B",
            display_name="Llama V3 Free 80B",
            description="Meta Llama 3 免费版",
            context_window=131072,
            max_output=8192,
            is_free=True,
            input_price=0.0,
            output_price=0.0,
        )
    ],
)

# Fireworks AI
FIREWORKS = AIProvider(
    name="fireworks",
    display_name="Fireworks AI",
    description="高速推理服务，专注生产环境",
    provider_type=ProviderType.CLOUD,
    base_url="https://api.fireworks.ai/inference/v1",
    signup_url="https://fireworks.ai/account/api-keys",
    docs_url="https://fireworks.ai/docs",
    has_free_tier=True,
    features=["超低延迟", "微批处理优化", "函数调用加速", "企业 SLA"],
    models=[
        ModelInfo(
            name="accounts/fireworks/models/llama-v3p1-70b-instruct",
            display_name="Llama 3.1 70B",
            description="优化的 Llama 3.1",
            context_window=131072,
            max_output=8192,
            is_free=True,
            input_price=0.0,
            output_price=0.0,
        )
    ],
)


# ============================================================
# 🏠 本地模型供应商 | Local Model Providers
# ============================================================

# Ollama (本地运行)
OLLAMA = AIProvider(
    name="ollama",
    display_name="Ollama (本地)",
    description="在本地运行开源大模型",
    provider_type=ProviderType.LOCAL,
    base_url="http://localhost:11434",
    signup_url="https://ollama.ai/download",
    docs_url="https://github.com/ollama/ollama",
    has_free_tier=True,
    recommended=True,
    features=["完全离线运行", "隐私保护", "无 API 费用", "一键安装", "100+ 模型库"],
    models=[
        ModelInfo(
            name="llama3.1:70b",
            display_name="Llama 3.1 70B",
            description="Meta 最新 Llama 模型",
            context_window=131072,
            max_output=2048,
            is_free=True,
            requires_api_key=False,
        ),
        ModelInfo(
            name="llama3.1:8b",
            display_name="Llama 3.1 8B",
            description="轻量级 Llama 模型",
            context_window=131072,
            max_output=2048,
            is_free=True,
            requires_api_key=False,
        ),
        ModelInfo(
            name="qwen2.5:72b",
            display_name="Qwen 2.5 72B",
            description="阿里通义千问模型",
            context_window=131072,
            max_output=2048,
            is_free=True,
            requires_api_key=False,
        ),
        ModelInfo(
            name="deepseek-r1:32b",
            display_name="DeepSeek R1 32B",
            description="深度求索推理模型",
            context_window=65536,
            max_output=8192,
            is_free=True,
            requires_api_key=False,
            capabilities=["推理", "思维链"],
        ),
        ModelInfo(
            name="codellama:34b",
            display_name="Code Llama 34B",
            description="代码专用模型",
            context_window=16384,
            max_output=4096,
            is_free=True,
            requires_api_key=False,
            capabilities=["代码", "补全"],
        ),
        ModelInfo(
            name="mistral:7b",
            display_name="Mistral 7B",
            description="高效能法语模型",
            context_window=32768,
            max_output=4096,
            is_free=True,
            requires_api_key=False,
        ),
        ModelInfo(
            name="phi3:14b",
            display_name="Phi-3 14B",
            description="微软小型高质量模型",
            context_window=127072,
            max_output=2048,
            is_free=True,
            requires_api_key=False,
        ),
        ModelInfo(
            name="gemma2:27b",
            display_name="Gemma 2 27B",
            description="Google 开源模型",
            context_window=9216,
            max_output=8192,
            is_free=True,
            requires_api_key=False,
        ),
        ModelInfo(
            name="yi:34b",
            display_name="Yi 34B",
            description="零一万物中文模型",
            context_window=200000,
            max_output=4096,
            is_free=True,
            requires_api_key=False,
            capabilities=["中文", "长文本"],
        ),
    ],
)

# LM Studio
LM_STUDIO = AIProvider(
    name="lmstudio",
    display_name="LM Studio (本地)",
    description="桌面端本地模型运行器，带 GUI",
    provider_type=ProviderType.LOCAL,
    base_url="http://localhost:1234/v1",
    signup_url="https://lmstudio.ai/",
    docs_url="https://lmstudio.ai/docs",
    has_free_tier=True,
    features=["图形化界面", "GGUF 模型支持", "自动下载模型", "聊天界面内置", "兼容 OpenAI API"],
    models=[
        ModelInfo(
            name="lm-studio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
            display_name="Llama 3.1 8B GGUF",
            description="量化版 Llama 模型",
            context_window=131072,
            max_output=2048,
            is_free=True,
            requires_api_key=False,
        )
    ],
)

# MLX (Apple Silicon)
MLX_PROVIDER = AIProvider(
    name="mlx",
    display_name="MLX (Apple Silicon)",
    description="苹果 Silicon 优化的本地推理框架",
    provider_type=ProviderType.LOCAL,
    base_url="http://localhost:8080/v1",
    signup_url="https://github.com/ml-explore/mlx",
    docs_url="https://ml-explore.github.io/mlx/",
    has_free_tier=True,
    features=["Metal GPU 加速", "内存映射加载", "统一内存架构", "Mac 原生性能", "Python API 友好"],
    models=[
        ModelInfo(
            name="mlx-community/Meta-Llama-3.1-8B-Instruct-4bit",
            display_name="Llama 3.1 8B (MLX 4-bit)",
            description="针对 Apple Silicon 优化",
            context_window=131072,
            max_output=2048,
            is_free=True,
            requires_api_key=False,
        )
    ],
)

# llama.cpp
LLAMA_CPP = AIProvider(
    name="llamacpp",
    display_name="llama.cpp (本地)",
    description="C++ 实现的高效 Llama 推理引擎",
    provider_type=ProviderType.LOCAL,
    base_url="http://localhost:8080/v1",
    signup_url="https://github.com/ggerganov/llama.cpp",
    docs_url="https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README",
    has_free_tier=True,
    features=["纯 C++ 实现", "CPU/GPU 支持", "量化模型支持", "服务器模式", "极端轻量"],
    models=[
        ModelInfo(
            name="llama-3-8b-q4_0.gguf",
            display_name="Llama 3 8B Q4",
            description="4-bit 量化模型",
            context_window=8192,
            max_output=1024,
            is_free=True,
            requires_api_key=False,
        )
    ],
)

# vLLM (高性能推理)
VLLM = AIProvider(
    name="vllm",
    display_name="vLLM (本地服务器)",
    description="大规模并行推理引擎",
    provider_type=ProviderType.LOCAL,
    base_url="http://localhost:8000/v1",
    signup_url="https://github.com/vllm-project/vllm",
    docs_url="https://docs.vllm.ai/",
    has_free_tier=True,
    features=["PagedAttention 技术", "多 GPU 并行", "高吞吐量", "连续批处理", "生产级部署"],
    models=[
        ModelInfo(
            name="meta-llama/Llama-3.1-8B-Instruct",
            display_name="Llama 3.1 8B (vLLM)",
            description="vLLM 优化部署",
            context_window=131072,
            max_output=2048,
            is_free=True,
            requires_api_key=False,
        )
    ],
)


# ============================================================
# 🔧 内置模型供应商 | Built-in Model Providers
# ============================================================

# 内置小型模型 (用于引导配置)
BUILTIN_MODEL = AIProvider(
    name="builtin",
    display_name="内置模型 (Built-in)",
    description="项目内置的小型开源模型，无需额外下载即可使用",
    provider_type=ProviderType.BUILTIN,
    base_url="",  # 本地运行
    signup_url="",
    docs_url="",
    has_free_tier=True,
    recommended=True,
    features=["开箱即用", "无需配置", "隐私保护", "引导用户配置", "基础对话功能"],
    models=[
        ModelInfo(
            name="tinyllama-1.1b",
            display_name="TinyLlama 1.1B",
            description="超小型通用模型 (~600MB)，适合引导和简单任务",
            context_window=2048,
            max_output=512,
            is_free=True,
            requires_api_key=False,
            capabilities=["引导配置", "简单对话", "代码提示"],
        ),
        ModelInfo(
            name="phi-2:2.7b",
            display_name="Phi-2 2.7B",
            description="微软小型高质量模型 (~1.5GB)，知识丰富",
            context_window=4096,
            max_output=512,
            is_free=True,
            requires_api_key=False,
            capabilities=["知识问答", "推理", "教育"],
        ),
        ModelInfo(
            name="stablelm-zephyr-3b",
            display_name="StableLM Zephyr 3B",
            description="Stability AI 对话模型 (~1.8GB)",
            context_window=4096,
            max_output=512,
            is_free=True,
            requires_api_key=False,
            capabilities=["对话", "指令遵循", "创意写作"],
        ),
    ],
)


# ============================================================
# 📋 所有供应商注册表 | All Providers Registry
# ============================================================

ALL_PROVIDERS: dict[str, AIProvider] = {
    # 云端 API 供应商 | Cloud API providers
    "openrouter": OPENROUTER,
    "openai": OPENAI,
    "anthropic": ANTHROPIC,
    "google": GOOGLE,
    "deepseek": DEEPSEEK,
    "qwen": QWEN,
    "baidu": BAIDU,
    "mistral": MISTRAL,
    "groq": GROQ,
    "together": TOGETHER,
    "fireworks": FIREWORKS,
    # 本地模型供应商 | Local model providers
    "ollama": OLLAMA,
    "lmstudio": LM_STUDIO,
    "mlx": MLX_PROVIDER,
    "llamacpp": LLAMA_CPP,
    "vllm": VLLM,
    # 内置模型 | Built-in model
    "builtin": BUILTIN_MODEL,
}


def get_provider(provider_id: str) -> AIProvider | None:
    """获取供应商信息 | Get provider information"""
    return ALL_PROVIDERS.get(provider_id.lower())


def get_all_providers() -> list[AIProvider]:
    """获取所有供应商 | Get all providers"""
    return list(ALL_PROVIDERS.values())


def get_cloud_providers() -> list[AIProvider]:
    """获取所有云端供应商 | Get cloud providers"""
    return [p for p in ALL_PROVIDERS.values() if p.provider_type == ProviderType.CLOUD]


def get_local_providers() -> list[AIProvider]:
    """获取所有本地供应商 | Get local providers"""
    return [p for p in ALL_PROVIDERS.values() if p.provider_type == ProviderType.LOCAL]


def get_recommended_providers() -> list[AIProvider]:
    """获取推荐的供应商 | Get recommended providers for beginners"""
    return [p for p in ALL_PROVIDERS.values() if p.recommended]


def get_free_providers() -> list[AIProvider]:
    """获取有免费层的供应商 | Get providers with free tier"""
    return [p for p in ALL_PROVIDERS.values() if p.has_free_tier]


def search_models(query: str) -> list[tuple[AIProvider, ModelInfo]]:
    """搜索模型 | Search models by keyword"""
    results = []
    query_lower = query.lower()

    for provider in ALL_PROVIDERS.values():
        for model in provider.models:
            if (
                query_lower in model.name.lower()
                or query_lower in model.display_name.lower()
                or query_lower in model.description.lower()
            ):
                results.append((provider, model))

    return results


if __name__ == "__main__":
    # 测试代码 | Test code
    print("=" * 60)
    print("🤖 衍智体 (YANZHITI) - AI 提供商配置")
    print("=" * 60)

    print(f"\n📊 总计供应商数: {len(ALL_PROVIDERS)}")
    print(f"☁️  云端供应商: {len(get_cloud_providers())}")
    print(f"🏠 本地供应商: {len(get_local_providers())}")
    print(f"⭐ 推荐供应商: {len(get_recommended_providers())}")
    print(f"💰 免费供应商: {len(get_free_providers())}")

    print("\n🌟 推荐给新手的供应商:")
    for provider in get_recommended_providers():
        print(f"  ✅ {provider.display_name} ({provider.name})")

    print("\n💰 有免费额度的供应商:")
    for provider in get_free_providers():
        free_marker = (
            "🆓"
            if not any(not m.is_free and m.requires_api_key for m in provider.models[:3])
            else "💵"
        )
        print(f"  {free_marker} {provider.display_name} ({provider.name})")
