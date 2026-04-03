"""
Web UI launcher for Claude Code Local
"""

import click
import uvicorn
from rich.console import Console

from claude_code import __version__


console = Console()


@click.command()
@click.option(
    "--host",
    "-h",
    default="0.0.0.0",
    help="Host to bind to",
)
@click.option(
    "--port",
    "-p",
    default=8000,
    help="Port to bind to",
)
@click.option(
    "--reload",
    "-r",
    is_flag=True,
    help="Enable auto-reload for development",
)
def main(host: str, port: int, reload: bool):
    """
    Start Claude Code Local Web UI

    Access the web interface at http://localhost:PORT
    """
    console.print(f"[bold cyan]🚀 Starting Claude Code Local Web UI v{__version__}[/bold cyan]")
    console.print(f"[green]📍 Server running at: http://localhost:{port}[/green]")
    console.print("[yellow]💡 Open this URL in your browser[/yellow]")
    console.print("[dim]Press Ctrl+C to stop[/dim]")
    console.print()

    uvicorn.run(
        "claude_code.web.server:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    main()
