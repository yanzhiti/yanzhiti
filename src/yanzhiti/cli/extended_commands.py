"""
扩展 CLI 命令 - 提供更多实用功能
Extended CLI Commands - Provide more useful features
"""

import json
import platform
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from yanzhiti import __version__

console = Console()


def show_info() -> None:
    """显示项目信息 | Show project information"""
    # 项目基本信息 | Project basic info
    info_table = Table(title="衍智体 (YANZHITI) 项目信息", show_header=False)
    info_table.add_column("属性", style="cyan")
    info_table.add_column("值", style="green")

    info_table.add_row("版本", __version__)
    info_table.add_row("Python 版本", f"{sys.version}")
    info_table.add_row("操作系统", f"{platform.system()} {platform.release()}")
    info_table.add_row("架构", f"{platform.machine()}")

    # 获取 Python 路径 | Get Python path
    info_table.add_row("Python 路径", sys.executable)

    # 检测虚拟环境 | Detect virtual environment
    venv = "是" if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else "否"
    info_table.add_row("虚拟环境", venv)

    # 工具统计 | Tool statistics
    from yanzhiti.core import ToolRegistry
    registry = ToolRegistry()
    tool_count = len(registry.list_tools())
    info_table.add_row("可用工具数", str(tool_count))

    console.print(info_table)

    # 功能特性 | Features
    features_text = """
## 核心功能 | Core Features

- 🤖 **AI 对话** - 与 AI 助手进行自然语言对话
- 📁 **文件操作** - 读取、写入、编辑文件
- 🔍 **代码搜索** - 全文搜索和模式匹配
- 💻 **Shell 执行** - 运行 Bash 和 PowerShell 命令
- 🌐 **Web 工具** - 网页抓取、搜索、API 测试
- 📊 **Git 集成** - 完整的 Git 操作支持
- ✅ **任务管理** - 创建和管理待办事项
- 🔧 **配置向导** - 引导式初始设置
- 🏥 **诊断工具** - 自动检测和修复问题
"""
    console.print(Panel(Markdown(features_text), title="功能特性", border_style="blue"))

    # 快速开始指南 | Quick start guide
    quick_start = """
## 快速开始 | Quick Start

### 基本用法 | Basic Usage

```bash
# 启动交互模式
yzt

# 单次查询
yzt "帮我写一个快速排序算法"

# 使用配置向导
yzt --setup

# 运行诊断工具
yzt --diagnose
```

### 高级选项 | Advanced Options

```bash
# 指定 API 密钥
yzt --api-key YOUR_API_KEY

# 选择模型
yzt --model gpt-4-turbo

# 设置工作目录
yzt --cwd /path/to/project

# 详细输出
yzt --verbose
```
"""
    console.print(Panel(Markdown(quick_start), title="快速开始", border_style="green"))


def show_tools() -> None:
    """显示可用工具列表 | Show available tools list"""
    from yanzhiti.core import ToolRegistry
    from yanzhiti.tools import (
        APITestTool,
        BashTool,
        FileEditTool,
        FileReadTool,
        FileWriteTool,
        GitBranchTool,
        GitDiffTool,
        GitLogTool,
        GitStatusTool,
        GitTool,
        GlobTool,
        GrepTool,
        PowerShellTool,
        TaskCreateTool,
        TaskDeleteTool,
        TaskGetTool,
        TaskListTool,
        TaskTask,
        TaskUpdateTool,
        TodoWriteTool,
        WebFetchTool,
        WebScrapeTool,
        WebSearchTool,
    )

    console.print("\n[bold cyan]可用工具列表 | Available Tools[/bold cyan]\n")

    # 创建工具分类表 | Create tool category table
    tools_by_category = {
        "📁 文件操作 (File Operations)": [
            ("file_read", "读取文件内容", FileReadTool),
            ("file_write", "写入文件", FileWriteTool),
            ("file_edit", "编辑文件 (搜索替换)", FileEditTool),
            ("glob", "文件名模式匹配", GlobTool),
            ("grep", "文件内容搜索", GrepTool),
        ],
        "💻 Shell 命令 (Shell Commands)": [
            ("bash", "执行 Bash 命令", BashTool),
            ("powershell", "执行 PowerShell 命令", PowerShellTool),
        ],
        "🌐 Web 工具 (Web Tools)": [
            ("web_fetch", "获取网页内容", WebFetchTool),
            ("web_search", "网络搜索", WebSearchTool),
            ("web_scrape", "网页数据抓取", WebScrapeTool),
            ("api_test", "API 接口测试", APITestTool),
        ],
        "📊 Git 操作 (Git Operations)": [
            ("git", "执行 Git 命令", GitTool),
            ("git_status", "查看 Git 状态", GitStatusTool),
            ("git_diff", "查看差异", GitDiffTool),
            ("git_log", "查看提交历史", GitLogTool),
            ("git_branch", "分支管理", GitBranchTool),
        ],
        "✅ 任务管理 (Task Management)": [
            ("task", "任务管理器", TaskTask),
            ("task_create", "创建任务", TaskCreateTool),
            ("task_list", "列出任务", TaskListTool),
            ("task_get", "获取任务详情", TaskGetTool),
            ("task_update", "更新任务", TaskUpdateTool),
            ("task_delete", "删除任务", TaskDeleteTool),
            ("todo_write", "批量更新待办", TodoWriteTool),
        ],
    }

    for category, tools in tools_by_category.items():
        table = Table(title=category, show_header=True, header_style="bold magenta")
        table.add_column("名称", style="cyan", width=15)
        table.add_column("描述", style="green")

        for name, desc, _ in tools:
            table.add_row(name, desc)

        console.print(table)
        console.print()

    # 使用示例 | Usage examples
    usage_examples = """
## 工具使用示例 | Tool Usage Examples

### 文件操作 | File Operations
```
"读取 README.md 文件"
"在 src 目录下查找所有 .py 文件"
"在所有 Python 文件中搜索 'TODO'"
```

### Shell 命令 | Shell Commands
```
"运行 npm test 并显示结果"
"列出当前目录的所有文件"
"检查 Python 版本"
```

### Web 工具 | Web Tools
```
"获取 https://example.com 的内容"
"搜索 Python 最佳实践"
"测试 API 接口 /api/users"
```

### Git 操作 | Git Operations
```
"查看当前 Git 状态"
"显示最近的提交记录"
"创建新分支 feature/login"
```

### 任务管理 | Task Management
```
"创建一个任务：完成用户认证功能"
"列出所有待办事项"
"将任务 #1 标记为已完成"
```
"""
    console.print(Panel(Markdown(usage_examples), title="使用示例", border_style="yellow"))


def show_examples() -> None:
    """显示示例库 | Show example library"""
    examples_dir = Path(__file__).parent.parent.parent / "examples"

    console.print("\n[bold cyan]示例库 | Example Library[/bold cyan]\n")

    if not examples_dir.exists():
        console.print("[yellow]示例目录不存在 | Example directory not found[/yellow]")
        return

    # 遍历示例目录 | Iterate through example directory
    for category_dir in sorted(examples_dir.iterdir()):
        if category_dir.is_dir():
            readme_file = category_dir / "README.md"

            if readme_file.exists():
                console.print(f"\n[bold magenta]📂 {category_dir.name}[/bold magenta]")

                try:
                    content = readme_file.read_text(encoding='utf-8')
                    console.print(Markdown(content))
                except Exception as e:
                    console.print(f"[red]读取失败: {e}[/red]")


def check_update() -> None:
    """检查更新 | Check for updates"""
    console.print("\n[cyan]检查更新... | Checking for updates...[/cyan]\n")

    try:
        import httpx
        import asyncio

        async def get_latest_version():
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    "https://pypi.org/pypi/yanzhiti/json"
                )
                data = response.json()
                return data["info"]["version"]

        latest_version = asyncio.run(get_latest_version())

        current = __version__.split('.')
        latest = latest_version.split('.')

        # 简单版本比较 | Simple version comparison
        needs_update = False
        for c, l in zip(current, latest):
            if int(l) > int(c):
                needs_update = True
                break
            elif int(c) > int(l):
                break

        if needs_update:
            console.print(Panel(
                f"[yellow]发现新版本！| New version available!\n\n"
                f"当前版本: {__version__}\n"
                f"最新版本: {latest_version}\n\n"
                f"升级命令: pip install --upgrade yanzhiti[/yellow]",
                title="更新可用",
                border_style="yellow",
            ))
        else:
            console.print("[green]✓ 已是最新版本 | Already up to date[/green]")
            console.print(f"当前版本: {__version__}")

    except Exception as e:
        console.print(f"[red]检查更新失败: {e}[/red]")
        console.print("[dim]请手动检查: https://pypi.org/project/yanzhiti/[/dim]")


def show_config() -> None:
    """显示当前配置 | Show current configuration"""
    import os

    console.print("\n[bold cyan]当前配置 | Current Configuration[/bold cyan]\n")

    config_table = Table(show_header=False)
    config_table.add_column("配置项", style="cyan", width=20)
    config_table.add_column("值", style="green")
    config_table.add_column("来源", style="yellow")

    # API 配置 | API configuration
    api_key = os.environ.get("YANZHITI_API_KEY", "未设置")
    if api_key != "未设置":
        api_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"

    config_table.add_row("API Key", api_key, "环境变量")

    base_url = os.environ.get("YANZHITI_BASE_URL", "默认 (OpenAI)")
    config_table.add_row("Base URL", base_url, "环境变量")

    model = os.environ.get("YANZHITI_MODEL", "default-model")
    config_table.add_row("Model", model, "环境变量")

    # 配置文件路径 | Config file path
    config_path = Path.home() / ".yanzhiti" / "config.toml"
    if config_path.exists():
        config_table.add_row("配置文件", str(config_path), "本地文件")
    else:
        config_table.add_row("配置文件", "不存在", "-")

    console.print(config_table)

    # 配置说明 | Configuration guide
    config_guide = """
## 配置说明 | Configuration Guide

### 环境变量 | Environment Variables

```bash
# 必需 | Required
export YANZHITI_API_KEY="your-api-key-here"

# 可选 | Optional
export YANZHITI_BASE_URL="https://api.openai.com/v1"
export YANZHITI_MODEL="gpt-4-turbo"
```

### 配置文件 | Config File

位置: `~/.yanzhiti/config.toml`

```toml
[api]
key = "your-api-key"
base_url = "https://api.openrouter.ai/api/v1"
model = "anthropic/claude-3-5-sonnet"

[general]
max_tokens = 4096
temperature = 1.0
verbose = false
```

### 使用配置向导 | Use Setup Wizard

运行 `yzt --setup` 进行交互式配置
"""
    console.print(Panel(Markdown(config_guide), title="配置指南", border_style="blue"))


@click.group()
def cli():
    """衍智体 (YANZHITI) 扩展命令 | Extended commands"""
    pass


@cli.command()
def info():
    """显示项目信息 | Show project information"""
    show_info()


@cli.command()
def tools():
    """显示可用工具 | Show available tools"""
    show_tools()


@cli.command()
def examples():
    """显示示例库 | Show example library"""
    show_examples()


@cli.command()
def update():
    """检查更新 | Check for updates"""
    check_update()


@cli.command()
def config():
    """显示配置 | Show configuration"""
    show_config()


if __name__ == "__main__":
    cli()
