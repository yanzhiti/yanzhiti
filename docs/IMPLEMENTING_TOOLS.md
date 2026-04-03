# Implementing New Tools

This guide explains how to implement new tools for 衍智体 (YANZHITI) Python.

## Tool Structure

Every tool must:

1. Inherit from `Tool` base class
2. Define `input_schema` property
3. Implement `execute()` method
4. Optionally implement `check_permission()` and `validate_input()`

## Basic Tool Template

```python
from typing import Any, Dict
from yanzhiti.core import Tool, ToolContext, ToolInputSchema, ToolResult
from yanzhiti.types import ToolResultStatus

class MyCustomTool(Tool):
    """Description of what this tool does"""

    def __init__(self):
        super().__init__(
            name="my_custom_tool",  # Unique tool name
            description="Human-readable description",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        """Define the input schema"""
        return ToolInputSchema(
            properties={
                "param1": {
                    "type": "string",
                    "description": "Description of param1",
                },
                "param2": {
                    "type": "integer",
                    "description": "Description of param2",
                },
            },
            required=["param1"],  # List required parameters
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        """Execute the tool"""
        param1 = input_data["param1"]
        param2 = input_data.get("param2", 0)

        try:
            # Tool logic here
            result = f"Processed {param1} with {param2}"

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=result,
                metadata={"custom": "data"},
            )
        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=str(e),
            )
```

## Input Schema

The input schema follows JSON Schema format:

### Common Types

```python
# String
"name": {
    "type": "string",
    "description": "User name",
}

# Integer
"age": {
    "type": "integer",
    "description": "User age",
}

# Number (float)
"price": {
    "type": "number",
    "description": "Item price",
}

# Boolean
"verbose": {
    "type": "boolean",
    "description": "Enable verbose output",
}

# Array
"items": {
    "type": "array",
    "items": {"type": "string"},
    "description": "List of items",
}

# Enum
"mode": {
    "type": "string",
    "enum": ["read", "write", "delete"],
    "description": "Operation mode",
}

# Object
"config": {
    "type": "object",
    "properties": {
        "key": {"type": "string"},
        "value": {"type": "string"},
    },
    "description": "Configuration object",
}
```

## Permission Checking

Override `check_permission()` for tools that need permission:

```python
async def check_permission(
    self,
    input_data: Dict[str, Any],
    context: ToolContext,
) -> PermissionResult:
    """Check if operation is allowed"""

    # Example: Check if file is in allowed directory
    file_path = input_data["file_path"]
    allowed_dirs = ["/home/user", "/tmp"]

    if not any(file_path.startswith(d) for d in allowed_dirs):
        return PermissionResult(
            granted=False,
            reason=f"File {file_path} is outside allowed directories",
        )

    return PermissionResult(granted=True)
```

## Custom Validation

Override `validate_input()` for complex validation:

```python
def validate_input(self, input_data: Dict[str, Any]) -> ValidationResult:
    """Custom validation logic"""

    # First do schema validation
    result = super().validate_input(input_data)
    if not result.valid:
        return result

    # Custom validation
    file_path = input_data["file_path"]

    # Check file extension
    if not file_path.endswith(".py"):
        return ValidationResult(
            valid=False,
            message="Only Python files are allowed",
            error_code=400,
        )

    return ValidationResult(valid=True)
```

## Tool Context

The `ToolContext` provides:

- `tool_use_id` - Unique ID for this tool use
- `cwd` - Current working directory
- `permission_mode` - Current permission mode
- `metadata` - Additional context data

## Tool Result

Return a `ToolResult` with:

- `status` - SUCCESS or ERROR
- `output` - Success output (string)
- `error` - Error message (string)
- `metadata` - Additional result data (dict)

## Examples

### Web Request Tool

```python
import httpx

class WebFetchTool(Tool):
    def __init__(self):
        super().__init__(
            name="web_fetch",
            description="Fetch content from a URL",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "url": {
                    "type": "string",
                    "format": "uri",
                    "description": "URL to fetch",
                },
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST", "PUT", "DELETE"],
                    "description": "HTTP method",
                },
            },
            required=["url"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        url = input_data["url"]
        method = input_data.get("method", "GET")

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url)

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=response.text,
                metadata={
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                },
            )
```

### Database Query Tool

```python
import asyncpg

class DatabaseQueryTool(Tool):
    def __init__(self, connection_string: str):
        super().__init__(
            name="db_query",
            description="Execute a database query",
        )
        self.connection_string = connection_string

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "query": {
                    "type": "string",
                    "description": "SQL query to execute",
                },
                "params": {
                    "type": "array",
                    "description": "Query parameters",
                },
            },
            required=["query"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        query = input_data["query"]
        params = input_data.get("params", [])

        conn = await asyncpg.connect(self.connection_string)
        try:
            rows = await conn.fetch(query, *params)
            result = [dict(row) for row in rows]

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=str(result),
                metadata={"row_count": len(rows)},
            )
        finally:
            await conn.close()
```

## Registering Tools

Add your tool to the registry:

```python
from yanzhiti.core import ToolRegistry

registry = ToolRegistry()
registry.register(MyCustomTool())
```

Or in the CLI:

```python
# In src/yanzhiti/cli/main.py

def create_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()

    # Standard tools
    registry.register(FileReadTool())
    # ...

    # Custom tools
    registry.register(MyCustomTool())

    return registry
```

## Testing Tools

Write tests for your tools:

```python
import pytest
from yanzhiti.core import ToolContext

@pytest.mark.asyncio
async def test_my_custom_tool():
    tool = MyCustomTool()
    context = ToolContext()

    # Test success case
    result = await tool.execute({"param1": "test"}, context)
    assert result.status.value == "success"

    # Test error case
    result = await tool.execute({"param1": ""}, context)
    assert result.status.value == "error"
```

## Best Practices

1. **Clear Names** - Use descriptive, unique tool names
2. **Good Descriptions** - Help Claude understand when to use the tool
3. **Validation** - Validate all inputs thoroughly
4. **Error Handling** - Return meaningful error messages
5. **Documentation** - Document parameters and behavior
6. **Testing** - Write comprehensive tests
7. **Security** - Check permissions for sensitive operations
8. **Performance** - Use async operations for I/O
9. **Metadata** - Include useful metadata in results
10. **Idempotency** - Make tools idempotent when possible

## Tool Ideas

Here are some tools you could implement:

- Git operations (commit, push, pull, branch)
- Docker commands
- Cloud services (AWS, GCP, Azure)
- Database operations
- API testing
- Image processing
- PDF manipulation
- Email sending
- Slack integration
- Jira operations
- And many more!
