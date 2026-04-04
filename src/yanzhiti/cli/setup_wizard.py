"""
增强版配置向导 - 支持所有供应商和本地模型
Enhanced Configuration Wizard - Support all providers and local models

功能：
- 支持 20+ 云端 AI 供应商
- 支持本地模型（Ollama, LM Studio, MLX, llama.cpp）
- 内置小型开源模型作为后备
- 智能推荐最佳选项
"""

import sys
from pathlib import Path

import click
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table

# 导入新的提供商配置 | Import new provider configuration
from yanzhiti.core.providers import (
    ALL_PROVIDERS,
    ProviderType,
    get_cloud_providers,
    get_local_providers,
    get_recommended_providers,
    get_free_providers,
)
from yanzhiti.core.builtin_models import BUILTIN_MODELS, BuiltInModelManager

console = Console()


def display_welcome():
    """显示欢迎信息 | Display welcome message"""
    welcome_text = """
# 🚀 欢迎使用衍智体 (YANZHITI) v2.0

## 增强版配置向导 | Enhanced Configuration Wizard

本向导将帮助您完成初始设置：
This wizard will help you complete the initial setup:

1. 选择 AI 服务类型 (云端/本地/内置)
2. 选择具体供应商和模型
3. 配置连接参数
4. 测试连接
5. 保存并开始使用

✨ 新功能：支持 20+ 供应商、本地模型、内置后备模型
"""
    console.print(Panel(welcome_text, style="bold magenta", border_style="green"))


def select_service_type() -> str:
    """选择服务类型 | Select service type"""
    console.print("\n[bold cyan]步骤 1/6: 选择服务类型 | Step 1/6: Select Service Type[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("类型", style="cyan", width=15)
    table.add_column("描述", style="green")
    table.add_column("特点", style="yellow")
    
    table.add_row(
        "☁️  云端 API",
        "使用在线 AI 服务",
        "强大、快速、需网络"
    )
    table.add_row(
        "🏠 本地模型",
        "在电脑上运行模型",
        "隐私、离线、免费"
    )
    table.add_row(
        "🔧 内置模型",
        "使用项目自带的小模型",
        "开箱即用、无需配置"
    )
    
    console.print(table)
    
    choice = Prompt.ask(
        "\n请选择服务类型 (cloud/local/builtin)",
        choices=["cloud", "local", "builtin"],
        default="cloud"
    )
    
    return choice


def select_cloud_provider() -> dict:
    """选择云端供应商 | Select cloud provider"""
    console.print("\n[bold cyan]步骤 2/6: 选择云端 AI 供应商 | Step 2/6: Select Cloud AI Provider[/bold cyan]\n")
    
    # 分类显示 | Display by category
    console.print("[bold]⭐ 推荐给新手 (Recommended for beginners):[/bold]")
    
    recommended = get_recommended_providers()
    rec_table = Table(show_header=True, header_style="bold green")
    rec_table.add_column("#", style="dim", width=4)
    rec_table.add_column("供应商", style="cyan")
    rec_table.add_column("描述", style="green")
    rec_table.add_column("免费", justify="center", width=6)
    rec_table.add_column("注册链接", style="dim")
    
    for i, provider in enumerate(recommended, 1):
        free_marker = "🆓" if provider.has_free_tier else "💰"
        rec_table.add_row(
            str(i),
            provider.display_name,
            provider.description[:40],
            free_marker,
            provider.signup_url[:35] + "..." if len(provider.signup_url) > 35 else provider.signup_url
        )
    
    console.print(rec_table)
    
    console.print("\n[bold]💰 所有免费/有免费额度的供应商:[/bold]")
    
    free_providers = [p for p in get_free_providers() if p not in recommended]
    if free_providers:
        free_table = Table(show_header=False)
        free_table.add_column("名称", style="cyan", width=20)
        free_table.add_column("描述", style="green")
        
        for provider in free_providers:
            free_table.add_row(provider.display_name, provider.description[:50])
        
        console.print(free_table)
    
    # 让用户选择 | Let user choose
    all_cloud = get_cloud_providers()
    options = {str(i): p.name for i, p in enumerate(all_cloud, 1)}
    options_display = {i: p.display_name for i, p in enumerate(all_cloud, 1)}
    
    option_str = ", ".join([f"{k}={v}" for k, v in options_display.items()])
    choice = Prompt.ask(f"\n请选择供应商编号 ({option_str})", choices=list(options.keys()))
    
    selected_provider = all_cloud[int(choice) - 1]
    
    console.print(f"\n✅ 已选择: [bold]{selected_provider.display_name}[/bold]")
    
    return {
        "provider_id": selected_provider.name,
        "provider": selected_provider
    }


def select_local_provider() -> dict:
    """选择本地模型供应商 | Select local model provider"""
    console.print("\n[bold cyan]步骤 2/6: 选择本地模型运行器 | Step 2/6: Select Local Model Runner[/bold cyan]\n")
    
    local_providers = get_local_providers()
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("运行器", style="cyan")
    table.add_column("描述", style="green")
    table.add_column("下载地址", style="dim")
    
    for i, provider in enumerate(local_providers, 1):
        table.add_row(
            str(i),
            provider.display_name,
            provider.description[:45],
            provider.signup_url[:30] + "..." if len(provider.signup_url) > 30 else provider.signup_url
        )
    
    console.print(table)
    
    console.print("\n[yellow]提示: 请确保已安装所选的本地模型运行器[/yellow]")
    
    options = {str(i): p.name for i, p in enumerate(local_providers, 1)}
    choice = Prompt.ask("\n请选择运行器编号", choices=list(options.keys()))
    
    selected = local_providers[int(choice) - 1]
    
    return {
        "provider_id": selected.name,
        "provider": selected
    }


def select_builtin_model() -> dict:
    """选择内置模型 | Select built-in model"""
    console.print("\n[bold cyan]步骤 2/6: 选择内置模型 | Step 2/6: Select Built-in Model[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("模型", style="cyan")
    table.add_column("大小", style="green")
    table.add_column("能力", style="yellow")
    
    for i, (name, config) in enumerate(BUILTIN_MODELS.items(), 1):
        capabilities = ", ".join(config.capabilities[:3])
        table.add_row(
            str(i),
            config.display_name,
            f"{config.model_size_mb} MB",
            capabilities
        )
    
    console.print(table)
    
    options = list(BUILTIN_MODELS.keys())
    choice = Prompt.ask(
        "\n请选择模型",
        choices=[str(i + 1) for i in range(len(options))],
        default="1"
    )
    
    selected_name = options[int(choice) - 1]
    selected_config = BUILTIN_MODELS[selected_name]
    
    console.print(f"\n✅ 已选择: [bold]{selected_config.display_name}[/bold]")
    
    return {
        "model_name": selected_name,
        "config": selected_config
    }


def configure_api_key(provider_info: dict) -> str:
    """配置 API 密钥 | Configure API key"""
    console.print("\n[bold cyan]步骤 3/6: 配置 API 密钥 | Step 3/6: Configure API Key[/bold cyan]\n")
    
    provider = provider_info["provider"]
    
    if provider.provider_type == ProviderType.LOCAL:
        console.print("[green]本地模型不需要 API 密钥！| Local models don't need API key![/green]")
        return ""
    
    console.print(f"[dim]获取 API Key: {provider.signup_url}[/dim]")
    
    api_key = Prompt.ask("请输入您的 API Key (输入 skip 跳过)", password=True)
    
    if api_key.lower() == "skip":
        console.print("[yellow]已跳过 API Key 配置[/yellow]")
        return ""
    
    # 显示密钥格式验证 | Show key format validation
    if len(api_key) < 10:
        console.print("[red]警告: API Key 似乎太短！| Warning: API key seems too short![/red]")
        if not Confirm.ask("是否继续？"):
            return configure_api_key(provider_info)
    
    masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
    console.print(f"\n✅ API Key 已设置: {masked_key}")
    
    return api_key


def select_model(provider_info: dict) -> str:
    """选择具体模型 | Select specific model"""
    console.print("\n[bold cyan]步骤 4/6: 选择模型 | Step 4/6: Select Model[/bold cyan]\n")
    
    provider = provider_info["provider"]
    
    if not provider.models:
        console.print("[yellow]该供应商没有预定义模型，将使用默认设置[/yellow]")
        return "default"
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("模型名称", style="cyan")
    table.add_column("描述", style="green")
    table.add_column("上下文", style="yellow", width=8)
    table.add_column("免费", justify="center", width=6)
    
    for i, model in enumerate(provider.models[:10], 1):  # 最多显示 10 个
        free_marker = "🆓" if model.is_free else "💰"
        table.add_row(
            str(i),
            model.display_name,
            model.description[:35],
            str(model.context_window),
            free_marker
        )
    
    console.print(table)
    
    if len(provider.models) > 10:
        console.print(f"[dim]... 还有 {len(provider.models) - 10} 个模型可用[/dim]")
    
    options = [m.name for m in provider.models[:10]]
    choice = Prompt.ask(
        "\n请选择模型编号 (直接回车选默认)",
        default="1",
        choices=[str(i + 1) for i in range(min(len(options), 10))]
    )
    
    selected_model = options[int(choice) - 1]
    console.print(f"\n✅ 已选择模型: [bold]{selected_model}[/bold]")
    
    return selected_model


async def test_connection(config: dict) -> bool:
    """测试连接 | Test connection"""
    console.print("\n[bold cyan]步骤 5/6: 测试连接 | Step 5/6: Test Connection[/bold cyan]\n")
    
    service_type = config.get("service_type", "cloud")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("正在测试连接...", total=None)
        
        try:
            if service_type == "builtin":
                # 测试内置模型 | Test built-in model
                from yanzhiti.core.builtin_models import LocalInferenceEngine
                
                engine = LocalInferenceEngine()
                success = await engine.initialize(
                    backend="builtin",
                    model_name=config.get("model_name", "tinyllama")
                )
                
                if success:
                    response = await engine.generate("测试消息")
                    progress.update(task, completed=True)
                    console.print("\n[green]✅ 内置模型连接成功！[/green]")
                    console.print(f"[dim]回复预览: {response[:100]}...[/dim]")
                    return True
            
            elif service_type == "local":
                # 测试本地模型 | Test local model
                provider_id = config.get("provider_id", "")
                
                if provider_id == "ollama":
                    async with httpx.AsyncClient(timeout=10) as client:
                        resp = await client.get("http://localhost:11434/api/tags")
                        if resp.status_code == 200:
                            progress.update(task, completed=True)
                            console.print("\n[green]✅ Ollama 连接成功！[/green]")
                            models = resp.json().get("models", [])
                            console.print(f"[dim]可用模型: {[m['name'] for m in models]}[/dim]")
                            return True
                
                elif provider_id == "lmstudio":
                    async with httpx.AsyncClient(timeout=10) as client:
                        resp = await client.get("http://localhost:1234/v1/models")
                        if resp.status_code == 200:
                            progress.update(task, completed=True)
                            console.print("\n[green]✅ LM Studio 连接成功！[/green]")
                            return True
                
                else:
                    console.print(f"[yellow]⚠️ 无法自动检测 {provider_id}，请手动确认[/yellow]")
                    return True
            
            else:
                # 测试云端 API | Test cloud API
                base_url = config.get("base_url", "")
                api_key = config.get("api_key", "")
                
                if not api_key:
                    console.print("[yellow]⚠️ 未设置 API Key，跳过测试[/yellow]")
                    return True
                
                headers = {"Authorization": f"Bearer {api_key}"}
                
                # 根据供应商调整端点 | Adjust endpoint based on provider
                provider_id = config.get("provider_id", "")
                
                if provider_id == "anthropic":
                    test_url = f"{base_url}/v1/messages"
                else:
                    test_url = f"{base_url}/models"
                
                async with httpx.AsyncClient(timeout=15) as client:
                    resp = await client.get(test_url, headers=headers)
                    
                    if resp.status_code == 200:
                        progress.update(task, completed=True)
                        console.print("\n[green]✅ API 连接成功！[/green]")
                        return True
                    else:
                        console.print(f"\n[red]❌ 连接失败 (HTTP {resp.status_code})[/red]")
                        console.print(f"[dim]{resp.text[:200]}[/dim]")
                        return False
        
        except httpx.ConnectError:
            console.print("\n[red]❌ 无法连接到服务器 | Cannot connect to server[/red]")
            console.print("[yellow]可能的原因:[/yellow]")
            console.print("  • 网络未连接或防火墙阻止")
            console.print("  • 服务未启动 (本地模型)")
            console.print("  • URL 或端口错误")
            return False
        
        except Exception as e:
            console.print(f"\n[red]❌ 测试失败: {e}[/red]")
            return False
    
    return False


def save_configuration(config: dict) -> Path:
    """保存配置 | Save configuration"""
    console.print("\n[bold cyan]步骤 6/6: 保存配置 | Step 6/6: Save Configuration[/bold cyan]\n")
    
    config_dir = Path.home() / ".yanzhiti"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_file = config_dir / "config.toml"
    
    # 构建 TOML 内容 | Build TOML content
    toml_content = f"""# 衍智体 (YANZHITI) 配置文件
# Generated by setup wizard on {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

[api]
provider = "{config.get('provider_id', 'openrouter')}"
model = "{config.get('model', 'default')}"
api_key = "{config.get('api_key', '')}"
base_url = "{config.get('base_url', '')}"

[general]
max_tokens = {config.get('max_tokens', 4096)}
temperature = {config.get('temperature', 0.7)}
verbose = false

[builtin]
enabled = {str(config.get('service_type', '') == 'builtin').lower()}
model = "{config.get('model_name', 'tinyllama')}"

[local]
enabled = {str(config.get('service_type', '') == 'local').lower()}
provider = "{config.get('local_provider', 'ollama')}"

[features]
auto_fallback = true
stream_output = true
save_history = true
"""
    
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(toml_content)
    
    console.print(f"\n✅ 配置已保存到: [cyan]{config_file}[/cyan]")
    
    return config_file


def display_success(config: dict):
    """显示成功信息 | Display success message"""
    service_type = config.get("service_type", "cloud")
    
    if service_type == "builtin":
        next_steps = """
## 🎉 配置完成！

您现在可以使用衍智体的内置模型了。

### 下一步操作：

```bash
# 启动衍智体
yzt

# 或者单次查询
yzt "帮我写一个 Python 函数"
```

### 提示：
- 内置模型适合简单任务和引导
- 建议后续配置更强大的云端服务
- 运行 `yzt --setup` 可重新配置
"""
    elif service_type == "local":
        next_steps = """
## 🎉 本地模型配置完成！

### 下一步操作：

```bash
# 确保本地模型运行器已启动
# Ollama: ollama serve
# LM Studio: 打开应用程序

# 启动衍智体
yzt
```

### 提示：
- 确保本地模型运行器在后台运行
- 可以随时切换到其他后端
- 运行 `yzt --diagnose` 检查状态
"""
    else:
        next_steps = f"""
## 🎉 配置完成！

### 下一步操作：

```bash
# 启动衍智体
yzt

# 或者单次查询
yzt "你好，介绍一下你自己"
```

### 有用的命令：

```bash
yzt --info      # 查看项目信息
yzt --tools     # 查看可用工具
yzt --examples  # 查看示例库
yzt --update    # 检查更新
yzt --diagnose  # 运行诊断工具
```
"""
    
    console.print(Panel(next_steps, title="✅ 成功", border_style="green", style="bold"))


@click.command()
@click.option("--quick", "-q", is_flag=True, help="Quick setup with defaults")
@click.option("--type", "-t", type=click.Choice(['cloud', 'local', 'builtin']), help="Skip type selection")
def main(quick: bool = False, type: str | None = None):
    """运行配置向导 | Run configuration wizard"""
    display_welcome()
    
    config = {}
    
    # 步骤 1: 选择服务类型 | Step 1: Select service type
    if type:
        config["service_type"] = type
        console.print(f"\n[cyan]已选择服务类型: {type}[/cyan]")
    else:
        config["service_type"] = select_service_type()
    
    # 根据类型进行不同配置 | Different configuration based on type
    if config["service_type"] == "cloud":
        # 云端 API 配置 | Cloud API configuration
        provider_info = select_cloud_provider()
        config["provider_id"] = provider_info["provider_id"]
        config["base_url"] = provider_info["provider"].base_url
        
        api_key = configure_api_key(provider_info)
        config["api_key"] = api_key
        
        if not quick:
            model = select_model(provider_info)
            config["model"] = model
        else:
            config["model"] = provider_info["provider"].models[0].name if provider_info["provider"].models else "default"
        
    elif config["service_type"] == "local":
        # 本地模型配置 | Local model configuration
        local_info = select_local_provider()
        config["provider_id"] = local_info["provider_id"]
        config["local_provider"] = local_info["provider_id"]
        config["base_url"] = local_info["provider"].base_url
        
        if not quick and local_info["provider"].models:
            model = select_model(local_info)
            config["model"] = model
        else:
            config["model"] = local_info["provider"].models[0].name if local_info["provider"].models else "default"
    
    else:  # builtin
        # 内置模型配置 | Built-in model configuration
        builtin_info = select_builtin_model()
        config["model_name"] = builtin_info["model_name"]
        config["model"] = builtin_info["model_name"]
    
    # 通用配置 | General configuration
    config["max_tokens"] = 4096
    config["temperature"] = 0.7
    
    # 测试连接 | Test connection
    if not quick:
        asyncio = __import__('asyncio')
        success = asyncio.run(test_connection(config))
        
        if not success and not Confirm.ask("\n是否继续保存配置？"):
            console.print("\n[yellow]配置已取消。您可以稍后重试。[/yellow]")
            return
    
    # 保存配置 | Save configuration
    save_configuration(config)
    
    # 显示成功信息 | Display success message
    display_success(config)


if __name__ == "__main__":
    main()
