"""
配置向导 CLI - 引导用户完成初始配置
Configuration Wizard - Guide users through initial setup
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, List

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import httpx

console = Console()

# 预定义的 AI 提供商列表 | Predefined AI providers list
AI_PROVIDERS = [
    {
        "name": "OpenRouter",
        "description": "Access 100+ AI models with one API",
        "url": "https://openrouter.ai/api/v1",
        "models": ["openai/gpt-3.5-turbo", "anthropic/claude-3-5-sonnet", "deepseek/deepseek-chat"],
        "free_tier": True,
        "signup_url": "https://openrouter.ai/keys"
    },
    {
        "name": "OpenAI",
        "description": "Official OpenAI API",
        "url": "https://api.openai.com/v1",
        "models": ["gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o"],
        "free_tier": False,
        "signup_url": "https://platform.openai.com/api-keys"
    },
    {
        "name": "Anthropic",
        "description": "Claude AI models",
        "url": "https://api.anthropic.com",
        "models": ["claude-3-5-sonnet", "claude-3-opus", "claude-3-haiku"],
        "free_tier": False,
        "signup_url": "https://console.anthropic.com/settings/keys"
    },
    {
        "name": "DeepSeek",
        "description": "Free Chinese AI models",
        "url": "https://api.deepseek.com",
        "models": ["deepseek-chat", "deepseek-coder"],
        "free_tier": True,
        "signup_url": "https://platform.deepseek.com/api_keys"
    },
    {
        "name": "Ollama (Local)",
        "description": "Run models locally",
        "url": "http://localhost:11434",
        "models": ["llama2", "codellama", "mistral"],
        "free_tier": True,
        "signup_url": None
    }
]


def display_welcome():
    """显示欢迎信息 | Display welcome message"""
    welcome_text = """
# 🚀 欢迎使用衍智体 (YANZHITI)

## 配置向导 | Configuration Wizard

本向导将帮助您完成初始设置：
This wizard will help you complete the initial setup:

1. 选择 AI 提供商 | Select AI provider
2. 配置 API 密钥 | Configure API key
3. 选择模型 | Choose model
4. 测试连接 | Test connection
5. 保存配置 | Save configuration
"""
    console.print(Panel(welcome_text, style="bold magenta", border_style="green"))


def select_provider() -> Dict:
    """让用户选择 AI 提供商 | Let user select AI provider"""
    console.print("\n[bold cyan]步骤 1/5: 选择 AI 提供商 | Step 1/5: Select AI Provider[/bold cyan]\n")
    
    # 创建提供商列表 | Create provider table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Provider", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Free Tier", justify="center")
    table.add_column("Models", style="yellow")
    
    for i, provider in enumerate(AI_PROVIDERS, 1):
        free_tier = "✅" if provider["free_tier"] else "❌"
        models_count = len(provider["models"])
        table.add_row(
            str(i),
            provider["name"],
            provider["description"],
            free_tier,
            f"{models_count} models"
        )
    
    console.print(table)
    
    # 获取用户选择 | Get user selection
    while True:
        choice = Prompt.ask(
            "\n选择提供商编号 (1-5)",
            choices=[str(i) for i in range(1, len(AI_PROVIDERS) + 1)],
            default="1"
        )
        
        try:
            provider_idx = int(choice) - 1
            if 0 <= provider_idx < len(AI_PROVIDERS):
                selected = AI_PROVIDERS[provider_idx]
                console.print(f"\n[green]✓ 已选择 | Selected: {selected['name']}[/green]\n")
                return selected
        except ValueError:
            pass
        
        console.print("[red]无效选择，请重新输入 | Invalid selection, please try again[/red]")


def get_api_key(provider: Dict) -> str:
    """获取 API 密钥 | Get API key"""
    console.print(f"\n[bold cyan]步骤 2/5: 配置 API 密钥 | Step 2/5: Configure API Key[/bold cyan]\n")
    
    if provider["signup_url"]:
        console.print(f"提供商：{provider['name']}")
        console.print(f"描述：{provider['description']}")
        console.print(f"\n[yellow]如果没有 API 密钥，请访问 | If you don't have an API key, visit:[/yellow]")
        console.print(f"[link={provider['signup_url']}]{provider['signup_url']}[/link]\n")
    
    while True:
        api_key = Prompt.ask(
            "输入 API 密钥 (留空跳过)",
            password=True
        )
        
        if not api_key:
            if Confirm.ask("\n确定要跳过吗？配置将不会保存", default=False):
                console.print("[yellow]已跳过 | Skipped[/yellow]")
                return ""
            continue
        
        # 简单验证 API 密钥格式 | Simple API key format validation
        if len(api_key) < 10:
            console.print("[red]API 密钥太短，请检查 | API key too short, please check[/red]")
            continue
        
        console.print(f"\n[green]✓ API 密钥已输入 | API key entered (****{api_key[-4:]})[/green]\n")
        return api_key


def select_model(provider: Dict) -> str:
    """选择模型 | Select model"""
    console.print(f"\n[bold cyan]步骤 3/5: 选择模型 | Step 3/5: Select Model[/bold cyan]\n")
    
    console.print(f"可用模型 | Available models for {provider['name']}:")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Model Name", style="cyan")
    
    for i, model in enumerate(provider["models"], 1):
        table.add_row(str(i), model)
    
    console.print(table)
    
    while True:
        choice = Prompt.ask(
            "\n选择模型编号",
            choices=[str(i) for i in range(1, len(provider["models"]) + 1)],
            default="1"
        )
        
        try:
            model_idx = int(choice) - 1
            if 0 <= model_idx < len(provider["models"]):
                selected_model = provider["models"][model_idx]
                console.print(f"\n[green]✓ 已选择 | Selected: {selected_model}[/green]\n")
                return selected_model
        except ValueError:
            pass
        
        console.print("[red]无效选择，请重新输入 | Invalid selection, please try again[/red]")


async def test_connection(provider: Dict, api_key: str, model: str) -> bool:
    """测试 API 连接 | Test API connection"""
    console.print(f"\n[bold cyan]步骤 4/5: 测试连接 | Step 4/5: Test Connection[/bold cyan]\n")
    
    if not api_key:
        console.print("[yellow]跳过测试 (未配置 API 密钥) | Skip test (no API key)[/yellow]\n")
        return True
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]正在测试连接... | Testing connection...", total=None)
        
        try:
            # 测试连接 (简单 HTTP 请求) | Test connection (simple HTTP request)
            async with httpx.AsyncClient(timeout=10.0) as client:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                # 不同提供商的测试端点 | Test endpoints for different providers
                if "openrouter" in provider["url"].lower():
                    test_url = f"{provider['url']}/models"
                elif "openai" in provider["url"].lower():
                    test_url = f"{provider['url']}/models"
                elif "anthropic" in provider["url"].lower():
                    test_url = f"{provider['url']}/v1/models"
                else:
                    test_url = provider["url"]
                
                response = await client.get(test_url, headers=headers)
                
                if response.status_code in [200, 401, 403]:
                    # 200 = 成功，401/403 = API 密钥有效但可能有权限问题
                    # 200 = Success, 401/403 = Valid key but possible permission issues
                    progress.update(task, description=f"[green]✓ 连接成功！| Connection successful![/green]")
                    console.print(f"\n[green]✓ API 密钥有效 | API key is valid[/green]")
                    console.print(f"[green]✓ 端点可达 | Endpoint is reachable[/green]\n")
                    return True
                else:
                    progress.update(task, description=f"[red]✗ 连接失败 | Connection failed[/red]")
                    console.print(f"\n[red]✗ HTTP {response.status_code}[/red]\n")
                    return False
                    
        except httpx.ConnectError as e:
            progress.update(task, description=f"[red]✗ 无法连接到服务器 | Cannot connect to server[/red]")
            console.print(f"\n[red]错误 | Error: {str(e)}[/red]\n")
            return False
        except Exception as e:
            progress.update(task, description=f"[red]✗ 测试失败 | Test failed[/red]")
            console.print(f"\n[red]错误 | Error: {str(e)}[/red]\n")
            return False


def save_config(provider: Dict, api_key: str, model: str) -> bool:
    """保存配置到 .env 文件 | Save config to .env file"""
    console.print(f"\n[bold cyan]步骤 5/5: 保存配置 | Step 5/5: Save Configuration[/bold cyan]\n")
    
    # 创建 .env 文件内容 | Create .env file content
    env_content = f"""# YANZHITI Configuration
# Generated by Configuration Wizard on {Path.cwd()}

# API Settings
YANZHITI_API_KEY={api_key}
YANZHITI_BASE_URL={provider['url']}
YANZHITI_MODEL={model}

# Model Parameters
YANZHITI_MAX_TOKENS=4096
YANZHITI_TEMPERATURE=1.0

# Execution Settings
YANZHITI_TIMEOUT=120
YANZHITI_MAX_RETRIES=3
YANZHITI_MAX_TURNS=100

# UI Settings
YANZHITI_VERBOSE=false
YANZHITI_DEBUG=false
YANZHITI_COLOR=true
"""
    
    # 写入 .env 文件 | Write to .env file
    env_file = Path.cwd() / ".env"
    
    try:
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)
        
        console.print(f"[green]✓ 配置已保存到 | Configuration saved to:[/green]")
        console.print(f"[bold]{env_file}[/bold]\n")
        
        # 显示配置摘要 | Show config summary
        summary_table = Table(title="配置摘要 | Configuration Summary", show_header=False)
        summary_table.add_column("Key", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Provider", provider["name"])
        summary_table.add_row("Model", model)
        summary_table.add_row("Base URL", provider["url"])
        summary_table.add_row("API Key", f"****{api_key[-4:]}" if api_key else "Not set")
        summary_table.add_row("Config File", str(env_file))
        
        console.print(summary_table)
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ 保存失败 | Save failed: {str(e)}[/red]\n")
        return False


def display_completion():
    """显示完成信息 | Display completion message"""
    completion_text = """
# 🎉 配置完成！| Configuration Complete!

## 下一步 | Next Steps:

1. **运行衍智体 | Run YANZHITI**:
   ```bash
   yanzhiti
   # 或 | or
   yzt
   ```

2. **查看文档 | View Documentation**:
   ```bash
   # 打开 README
   # Open README
   ```

3. **开始使用 | Start Using**:
   - 尝试简单的代码生成任务
   - Try simple code generation tasks
   - 使用文件操作工具
   - Use file operation tools
   - 探索 Git 集成功能
   - Explore Git integration features

## 需要帮助？| Need Help?

- 📖 [文档 | Documentation](docs/README.md)
- 🐛 [报告问题 | Report Issues](https://github.com/yanzhiti/yanzhiti/issues)
- 💬 [社区讨论 | Community](https://github.com/yanzhiti/yanzhiti/discussions)

祝您使用愉快！| Happy coding!
"""
    console.print(Panel(completion_text, style="bold green", border_style="green"))


@click.command()
@click.option('--skip-welcome', is_flag=True, help='跳过欢迎信息 | Skip welcome message')
@click.option('--lang', type=click.Choice(['zh', 'en']), default='zh', help='语言 | Language')
def main(skip_welcome: bool, lang: str):
    """
    配置向导 - 引导您完成初始设置
    Configuration Wizard - Guide you through initial setup
    """
    try:
        # 显示欢迎信息 | Display welcome
        if not skip_welcome:
            display_welcome()
        
        # 执行配置步骤 | Execute configuration steps
        import asyncio
        
        # 1. 选择提供商 | Select provider
        provider = select_provider()
        
        # 2. 获取 API 密钥 | Get API key
        api_key = get_api_key(provider)
        
        # 3. 选择模型 | Select model
        model = select_model(provider)
        
        # 4. 测试连接 | Test connection
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        connection_ok = loop.run_until_complete(
            test_connection(provider, api_key, model)
        )
        
        if not connection_ok:
            console.print("\n[yellow]⚠️  连接测试失败，但您可以继续配置并稍后修复[/yellow]")
            if not Confirm.ask("是否继续保存配置？| Continue saving config?", default=True):
                console.print("[yellow]已取消配置 | Configuration cancelled[/yellow]")
                return
        
        # 5. 保存配置 | Save config
        if save_config(provider, api_key, model):
            display_completion()
        else:
            console.print("[red]配置保存失败 | Failed to save configuration[/red]")
            
    except KeyboardInterrupt:
        console.print("\n\n[yellow]配置已取消 | Configuration cancelled[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]发生错误 | An error occurred: {str(e)}[/red]")
        console.print("[yellow]请重试或手动配置 .env 文件 | Please retry or manually configure .env file[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()
