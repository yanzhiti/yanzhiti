"""
Main CLI entry point for 衍智体 (YANZHITI)
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
from yanzhiti.core import QueryEngine, QueryEngineConfig, ToolRegistry
from yanzhiti.tools import (
    # File tools
    FileReadTool,
    FileWriteTool,
    FileEditTool,
    GlobTool,
    GrepTool,
    # Shell tools
    BashTool,
    PowerShellTool,
    TaskTool,
    # Web tools
    WebFetchTool,
    WebSearchTool,
    WebScrapeTool,
    APITestTool,
    # Git tools
    GitTool,
    GitStatusTool,
    GitDiffTool,
    GitLogTool,
    GitBranchTool,
    # Task tools
    TaskCreateTool,
    TaskListTool,
    TaskGetTool,
    TaskUpdateTool,
    TaskDeleteTool,
    TodoWriteTool,
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


def get_api_key() -> Optional[str]:
    """Get API key from environment or config"""
    # Try environment variable
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        return api_key

    # Try config file
    # TODO: Implement config file reading
    return None


def create_tool_registry() -> ToolRegistry:
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

    return registry


async def run_interactive(engine: QueryEngine) -> None:
    """Run interactive REPL"""
    console.print(Panel.fit(
        "[bold]衍智体 (YANZHITI) - Python Edition[/bold]\n"
        f"Version: {__version__}\n"
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
                    f"Input tokens: {stats['usage']['input_tokens']}\n"
                    f"Output tokens: {stats['usage']['output_tokens']}\n"
                    f"Total tokens: {stats['usage']['total_tokens']}\n"
                    f"Tools available: {stats['tool_count']}",
                    title="Session Statistics",
                    style="info",
                ))
                continue
            elif user_input == "/reset":
                engine.reset()
                console.print("[info]Session reset[/info]")
                continue

            # Process query
            console.print("[assistant]YANZHITI[/assistant]: ", end="")

            with console.status("[bold green]Thinking...[/bold green]"):
                response = await engine.query(user_input)

            # Display response
            if isinstance(response.content, str):
                console.print(Markdown(response.content))
            else:
                # Handle structured content
                for block in response.content:
                    if block.get("type") == "text":
                        console.print(Markdown(block["text"]))
                    elif block.get("type") == "tool_use":
                        console.print(f"[info]Used tool: {block['name']}[/info]")

        except KeyboardInterrupt:
            console.print("\n[info]Use /exit to quit[/info]")
        except Exception as e:
            console.print(f"[error]Error: {str(e)}[/error]")


def show_help() -> None:
    """Show help information"""
    help_text = """
# 衍智体 (YANZHITI) - Help

## Special Commands
- `/help` - Show this help message
- `/exit`, `/quit`, `/q` - Exit the program
- `/stats` - Show session statistics
- `/reset` - Reset the current session

## Features
- Natural language queries
- File operations (read, write, edit)
- Shell command execution
- Task management
- And much more...

## Tips
- Be specific in your requests
- Use absolute paths for file operations
- Check `/stats` to monitor token usage
"""
    console.print(Markdown(help_text))


@click.command()
@click.option(
    "--api-key",
    "-k",
    envvar="ANTHROPIC_API_KEY",
    help="Anthropic API key",
)
@click.option(
    "--model",
    "-m",
    default="anthropic/claude-3-5-sonnet-20241022",
    help="Model to use",
)
@click.option(
    "--max-tokens",
    "-t",
    default=4096,
    help="Maximum tokens per response",
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
    api_key: Optional[str],
    model: str,
    max_tokens: int,
    cwd: str,
    verbose: bool,
    version: bool,
    query: Optional[str],
) -> None:
    """
    衍智体 (YANZHITI) - AI-powered coding assistant

    If QUERY is provided, execute it and exit.
    Otherwise, start interactive mode.
    """
    if version:
        console.print(f"衍智体 (YANZHITI) v{__version__}")
        return

    # Get API key
    if not api_key:
        api_key = get_api_key()

    if not api_key:
        console.print("[error]Error: No API key provided[/error]")
        console.print("Set ANTHROPIC_API_KEY environment variable or use --api-key option")
        sys.exit(1)

    # Create tool registry
    tool_registry = create_tool_registry()

    # Create engine config
    config = QueryEngineConfig(
        cwd=cwd,
        model=model,
        max_tokens=max_tokens,
        tools=tool_registry.list_tools(),
        verbose=verbose,
    )

    # Create engine
    engine = QueryEngine(config, api_key=api_key)

    # Run
    if query:
        # Single query mode
        async def run_single():
            with console.status("[bold green]Processing...[/bold green]"):
                response = await engine.query(query)

            if isinstance(response.content, str):
                console.print(Markdown(response.content))
            else:
                for block in response.content:
                    if block.get("type") == "text":
                        console.print(Markdown(block["text"]))

        asyncio.run(run_single())
    else:
        # Interactive mode
        asyncio.run(run_interactive(engine))


if __name__ == "__main__":
    main()
