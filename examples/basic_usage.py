"""
Example: Basic usage of Claude Code Python
"""

import asyncio
import os

from yanzhiti import QueryEngine
from yanzhiti.core import QueryEngineConfig
from yanzhiti.tools import (
    BashTool,
    FileEditTool,
    FileReadTool,
    FileWriteTool,
    GlobTool,
    GrepTool,
)


async def main():
    # Get API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    # Create configuration
    config = QueryEngineConfig(
        cwd=".",
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        tools=[
            FileReadTool(),
            FileWriteTool(),
            FileEditTool(),
            GlobTool(),
            GrepTool(),
            BashTool(),
        ],
    )

    # Create engine
    engine = QueryEngine(config, api_key=api_key)

    # Example 1: Simple query
    print("Example 1: Simple query")
    response = await engine.query("What is 2 + 2?")
    print(f"Response: {response.content}")
    print()

    # Example 2: File operations
    print("Example 2: File operations")
    response = await engine.query(
        "Create a file called test.txt with the content 'Hello, Claude!'"
    )
    print(f"Response: {response.content}")
    print()

    # Example 3: Code analysis
    print("Example 3: Code analysis")
    response = await engine.query(
        "Read the file test.txt and tell me what's in it"
    )
    print(f"Response: {response.content}")
    print()

    # Get statistics
    stats = engine.get_stats()
    print(f"Session stats: {stats}")


if __name__ == "__main__":
    asyncio.run(main())
