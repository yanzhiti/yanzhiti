"""
Example: Advanced usage with custom tools
"""

import asyncio
import os
from typing import Any, Dict

from yanzhiti import QueryEngine
from yanzhiti.core import QueryEngineConfig, Tool, ToolContext, ToolInputSchema, ToolResult
from yanzhiti.tools import (
    BashTool,
    FileEditTool,
    FileReadTool,
    FileWriteTool,
    GlobTool,
    GrepTool,
)
from yanzhiti.types import ToolResultStatus


# Custom tool example
class WeatherTool(Tool):
    """Example custom tool for getting weather"""

    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get the current weather for a location",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "location": {
                    "type": "string",
                    "description": "City name or coordinates",
                },
                "units": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature units",
                },
            },
            required=["location"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        location = input_data["location"]
        units = input_data.get("units", "celsius")

        # This is a mock implementation
        # In real usage, you would call a weather API
        weather_data = {
            "location": location,
            "temperature": 22 if units == "celsius" else 72,
            "units": units,
            "condition": "sunny",
            "humidity": 45,
        }

        output = (
            f"Weather for {location}:\n"
            f"Temperature: {weather_data['temperature']}°{units[0].upper()}\n"
            f"Condition: {weather_data['condition']}\n"
            f"Humidity: {weather_data['humidity']}%"
        )

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output=output,
            metadata=weather_data,
        )


async def main():
    # Get API key
    api_key = os.environ.get("YANZHITI_API_KEY")
    if not api_key:
        print("Please set YANZHITI_API_KEY environment variable")
        return

    # Create configuration with custom tool
    config = QueryEngineConfig(
        cwd=".",
        model="default-model",
        max_tokens=4096,
        tools=[
            # Standard tools
            FileReadTool(),
            FileWriteTool(),
            FileEditTool(),
            GlobTool(),
            GrepTool(),
            BashTool(),
            # Custom tool
            WeatherTool(),
        ],
    )

    # Create engine
    engine = QueryEngine(config, api_key=api_key)

    # Example: Using custom tool
    print("Example: Custom weather tool")
    response = await engine.query(
        "What's the weather like in San Francisco?"
    )
    print(f"Response: {response.content}")
    print()

    # Example: Multi-step task
    print("Example: Multi-step task")
    response = await engine.query(
        "Create a Python file called weather_app.py that "
        "asks the user for a city and displays the weather"
    )
    print(f"Response: {response.content}")
    print()

    # Example: Code review
    print("Example: Code review")
    response = await engine.query(
        "Review the code in weather_app.py and suggest improvements"
    )
    print(f"Response: {response.content}")
    print()

    # Get statistics
    stats = engine.get_stats()
    print(f"Session stats:")
    print(f"  Messages: {stats['message_count']}")
    print(f"  Turns: {stats['turn_count']}")
    print(f"  Input tokens: {stats['usage']['input_tokens']}")
    print(f"  Output tokens: {stats['usage']['output_tokens']}")
    print(f"  Total tokens: {stats['usage']['total_tokens']}")


if __name__ == "__main__":
    asyncio.run(main())
