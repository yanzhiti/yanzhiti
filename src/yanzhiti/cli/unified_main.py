"""
统一启动器 - 同时启动 Web UI 和 Console
"""

import asyncio
import contextlib
import threading
import webbrowser

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from yanzhiti import __version__
from yanzhiti.core import QueryEngine, QueryEngineConfig, ToolRegistry
from yanzhiti.tools import (
    APITestTool, BashTool, FileEditTool, FileReadTool, FileWriteTool,
    GitBranchTool, GitDiffTool, GitLogTool, GitStatusTool, GitTool,
    GlobTool, GrepTool, PowerShellTool, TaskCreateTool, TaskDeleteTool,
    TaskGetTool, TaskListTool, TaskTool, TaskUpdateTool, TodoWriteTool,
    WebFetchTool, WebScrapeTool, WebSearchTool,
)

console = Console()


def start_web_server(port: int):
    """在新线程中启动 Web 服务器"""
    import uvicorn
    from yanzhiti.web.server import app

    uvicorn.run(app, host="0.0.0.0", port=port)


async def run_console():
    """运行 Console 交互模式"""
    registry = ToolRegistry()
    for tool in [
        FileReadTool(), FileWriteTool(), FileEditTool(), GlobTool(), GrepTool(),
        BashTool(), PowerShellTool(), TaskTool(),
        WebFetchTool(), WebSearchTool(), WebScrapeTool(), APITestTool(),
        GitTool(), GitStatusTool(), GitDiffTool(), GitLogTool(), GitBranchTool(),
        TaskCreateTool(), TaskListTool(), TaskGetTool(), TaskUpdateTool(), TaskDeleteTool(), TodoWriteTool(),
    ]:
        registry.register(tool)

    config = QueryEngineConfig(
        cwd=".",
        model="default-model",
        max_tokens=4096,
        tools=registry.list_tools(),
        verbose=False,
    )

    engine = QueryEngine(config, api_key=None, base_url=None)

    console.print("[cyan]Console 交互模式已启动，输入 /help 查看帮助[/cyan]")
    console.print()

    while True:
        try:
            user_input = Prompt.ask("\n[blue]你[/blue]")
            if not user_input.strip():
                continue
            if user_input in ["/exit", "/quit", "/q"]:
                break
            if user_input == "/help":
                console.print("[dim]支持 /exit /quit /q 退出[/dim]")
                continue

            with console.status("[bold green]思考中...[/bold green]"):
                response = await engine.query(user_input)

            if isinstance(response.content, str):
                console.print(Markdown(response.content))
            else:
                for block in response.content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        console.print(Markdown(block["text"]))
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]错误: {e}[/red]")


@click.command()
@click.option(
    "--port",
    "-p",
    default=8500,
    help="Web UI 端口",
)
@click.option(
    "--web-only",
    is_flag=True,
    help="仅启动 Web UI",
)
@click.option(
    "--console-only",
    is_flag=True,
    help="仅启动 Console",
)
@click.option(
    "--no-browser",
    is_flag=True,
    help="不自动打开浏览器",
)
def main(port: int, web_only: bool, console_only: bool, no_browser: bool):
    """
    衍智体 (YANZHITI) - AI 智能编程助手

    默认同时启动 Web UI 和 Console
    """
    console.print(Panel.fit(
        "[bold cyan]🤖 衍智体 (YANZHITI) v" + __version__ + "[/bold cyan]\n"
        "AI 智能编程助手 | AI-Powered Coding Assistant",
        style="cyan",
    ))

    web_url = f"http://localhost:{port}"

    if console_only:
        console.print("[cyan]🚀 启动 Console 模式...[/cyan]")
        asyncio.run(run_console())
        return

    if web_only or (not console_only and not web_only):
        console.print(f"[green]🌐 Web UI: {web_url}[/green]")
        console.print(f"[yellow]💡 浏览器将自动打开，或访问 {web_url}[/yellow]")
        console.print()

        if not no_browser:
            webbrowser.open(web_url)

        web_thread = threading.Thread(target=start_web_server, args=(port,), daemon=True)
        web_thread.start()

        console.print("[cyan]🖥️  Console 交互模式已启动[/cyan]")
        console.print("[dim]按 Ctrl+C 停止服务器[/dim]\n")

        with contextlib.suppress(KeyboardInterrupt):
            asyncio.run(run_console())

        console.print("\n[green]已停止[/green]")


if __name__ == "__main__":
    main()
