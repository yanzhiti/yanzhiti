"""
Local CLI using MLX models - No API required!
"""

import asyncio
import os
import sys
from typing import Optional

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.theme import Theme

from yanzhiti import __version__
from yanzhiti.core import ToolRegistry
from yanzhiti.core.local_query_engine import LocalQueryEngine, LocalQueryEngineConfig
from yanzhiti.core.agent import AgentTool, ForkTool
from yanzhiti.tools import (
    # File tools
    FileReadTool, FileWriteTool, FileEditTool, GlobTool, GrepTool,
    # Shell tools
    BashTool, PowerShellTool, TaskTool,
    # Web tools
    WebFetchTool, WebSearchTool, WebScrapeTool, APITestTool,
    # Git tools
    GitTool, GitStatusTool, GitDiffTool, GitLogTool, GitBranchTool,
    # Task tools
    TaskCreateTool, TaskListTool, TaskGetTool, TaskUpdateTool, TaskDeleteTool, TodoWriteTool,
)


# Custom theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "user": "blue",
    "assistant": "magenta",
})

console = Console(theme=custom_theme)


def create_tool_registry(query_engine: Optional[LocalQueryEngine] = None) -> ToolRegistry:
    """Create and populate tool registry"""
    registry = ToolRegistry()

    # File tools
    registry.register(FileReadTool())
    registry.register(FileWriteTool())
    registry.register(FileEditTool())
    registry.register(GlobTool())
    registry.register(GrepTool())

    # Shell tools
    registry.register(BashTool())
    registry.register(PowerShellTool())
    registry.register(TaskTool())

    # Web tools
    registry.register(WebFetchTool())
    registry.register(WebSearchTool())
    registry.register(WebScrapeTool())
    registry.register(APITestTool())

    # Git tools
    registry.register(GitTool())
    registry.register(GitStatusTool())
    registry.register(GitDiffTool())
    registry.register(GitLogTool())
    registry.register(GitBranchTool())

    # Task tools
    registry.register(TaskCreateTool())
    registry.register(TaskListTool())
    registry.register(TaskGetTool())
    registry.register(TaskUpdateTool())
    registry.register(TaskDeleteTool())
    registry.register(TodoWriteTool())

    # Agent tools (if query_engine provided)
    if query_engine:
        registry.register(AgentTool(query_engine))
        registry.register(ForkTool(query_engine))

    return registry


async def run_interactive(engine: LocalQueryEngine) -> None:
    """Run interactive REPL with local model"""
    console.print(Panel.fit(
        "[bold]Claude Code - Local MLX Edition[/bold]\n"
        f"Version: {__version__}\n"
        f"Model: {engine.config.model_name}\n"
        "Running completely on your Mac - No API required!\n"
        "Type your query and press Enter. Use Ctrl+C to exit.",
        style="info",
    ))

    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[user]You", console=console)

            if not user_input.strip():
                continue

            # Handle special commands
            if user_input in ["/exit", "/quit", "/q"]:
                console.print("[info]Goodbye![/info]")
                break
            elif user_input == "/help":
                show_help()
                continue
            elif user_input == "/stats":
                stats = engine.get_stats()
                console.print(Panel(
                    f"Session ID: {stats['session_id']}\n"
                    f"Messages: {stats['message_count']}\n"
                    f"Turns: {stats['turn_count']}\n"
                    f"Total tokens: {stats['usage']['total_tokens']}\n"
                    f"Tools available: {stats['tool_count']}\n"
                    f"Model: {stats['model']}",
                    title="Session Statistics",
                    style="info",
                ))
                continue
            elif user_input == "/reset":
                engine.reset()
                console.print("[info]Session reset[/info]")
                continue

            # Process query
            console.print("[assistant]Assistant[/assistant]: ", end="")

            with console.status("[bold green]Thinking locally...[/bold green]"):
                response = await engine.query(user_input)

            # Display response
            if isinstance(response.content, str):
                console.print(Markdown(response.content))
            else:
                console.print(str(response.content))

        except KeyboardInterrupt:
            console.print("\n[info]Use /exit to quit[/info]")
        except Exception as e:
            console.print(f"[error]Error: {str(e)}[/error]")


def show_help() -> None:
    """Show help information"""
    help_text = """
# Claude Code Local - Help

## Special Commands
- `/help` - Show this help message
- `/exit`, `/quit`, `/q` - Exit the program
- `/stats` - Show session statistics
- `/reset` - Reset the current session

## Features
- 🚀 Runs completely on your Mac
- 🔒 No API key required
- 💾 Private - nothing leaves your machine
- 🛠️ 23 tools available
- 📁 File operations
- 💻 Shell commands
- 🌐 Web operations
- 📝 Git operations
- ✅ Task management

## Available Models
- mlx-community/Llama-3.2-3B-Instruct-4bit (default)
- mlx-community/Llama-3.2-1B-Instruct-4bit
- mlx-community/Phi-3.5-mini-instruct-4bit

## Tips
- First run will download the model (~2GB)
- Subsequent runs are much faster
- Use specific requests for better results
- Check `/stats` to monitor usage
"""
    console.print(Markdown(help_text))


@click.command()
@click.option(
    "--model",
    "-m",
    default="local-model",
    help="Model name (for LM Studio: local-model, for MLX: model path)",
)
@click.option(
    "--backend",
    "-b",
    type=click.Choice(["lm_studio", "mlx"]),
    default="lm_studio",
    help="Backend to use: lm_studio (default) or mlx",
)
@click.option(
    "--base-url",
    "-u",
    default="http://localhost:1234/v1",
    help="LM Studio base URL (default: http://localhost:1234/v1)",
)
@click.option(
    "--max-tokens",
    "-t",
    default=2048,
    help="Maximum tokens per response",
)
@click.option(
    "--temperature",
    "-T",
    default=0.7,
    help="Temperature for generation",
)
@click.option(
    "--cwd",
    "-d",
    default=".",
    help="Working directory",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
@click.option(
    "--version",
    is_flag=True,
    help="Show version and exit",
)
@click.argument("query", required=False)
def main(
    model: str,
    backend: str,
    base_url: str,
    max_tokens: int,
    temperature: float,
    cwd: str,
    verbose: bool,
    version: bool,
    query: Optional[str],
) -> None:
    """
    Claude Code Local - AI assistant running on your Mac

    No API key required! Uses LM Studio or MLX models.

    If QUERY is provided, execute it and exit.
    Otherwise, start interactive mode.
    """
    if version:
        console.print(f"Claude Code Local v{__version__}")
        return

    # Check backend
    if backend == "mlx" and sys.platform != "darwin":
        console.print("[error]Error: MLX models only work on Mac with Apple Silicon[/error]")
        console.print("Please use LM Studio backend or the regular claude-code command with API key.")
        sys.exit(1)

    console.print(f"[info]🚀 Starting Claude Code with {backend} backend...[/info]")
    console.print(f"[info]Model: {model}[/info]")
    if backend == "lm_studio":
        console.print(f"[info]LM Studio URL: {base_url}[/info]")
    console.print("[info]This will run completely on your Mac - no API required![/info]")
    console.print()

    # Create tool registry
    tool_registry = create_tool_registry()

    # Create engine config
    config = LocalQueryEngineConfig(
        cwd=cwd,
        model_name=model,
        backend=backend,
        base_url=base_url,
        max_tokens=max_tokens,
        temperature=temperature,
        tools=tool_registry.list_tools(),
        verbose=verbose,
    )

    # Create engine
    engine = LocalQueryEngine(config)

    # Run
    if query:
        # Single query mode
        async def run_single():
            with console.status("[bold green]Processing locally...[/bold green]"):
                response = await engine.query(query)

            if isinstance(response.content, str):
                console.print(Markdown(response.content))
            else:
                console.print(str(response.content))

        asyncio.run(run_single())
    else:
        # Interactive mode
        asyncio.run(run_interactive(engine))


if __name__ == "__main__":
    main()
