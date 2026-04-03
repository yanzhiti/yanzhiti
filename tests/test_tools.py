"""
Tests for core functionality
"""

import pytest

from yanzhiti.core import Tool, ToolContext, ToolInputSchema, ToolResult
from yanzhiti.tools import FileReadTool, GlobTool, BashTool


class TestToolSystem:
    """Test the tool system"""

    def test_tool_input_schema(self):
        """Test tool input schema"""
        tool = FileReadTool()
        schema = tool.input_schema

        assert schema.type == "object"
        assert "file_path" in schema.properties
        assert "file_path" in schema.required

    def test_tool_to_api_format(self):
        """Test tool conversion to API format"""
        tool = FileReadTool()
        api_format = tool.to_api_format()

        assert api_format["name"] == "file_read"
        assert "description" in api_format
        assert "input_schema" in api_format

    def test_tool_validation(self):
        """Test tool input validation"""
        tool = FileReadTool()

        # Valid input
        result = tool.validate_input({"file_path": "/tmp/test.txt"})
        assert result.valid is True

        # Missing required field
        result = tool.validate_input({})
        assert result.valid is False
        assert "file_path" in result.message


class TestToolRegistry:
    """Test the tool registry"""

    def test_register_tool(self):
        """Test tool registration"""
        from yanzhiti.core import ToolRegistry

        registry = ToolRegistry()
        tool = FileReadTool()

        registry.register(tool)

        assert "file_read" in registry
        assert len(registry) == 1

    def test_get_tool(self):
        """Test getting tool from registry"""
        from yanzhiti.core import ToolRegistry

        registry = ToolRegistry()
        tool = FileReadTool()
        registry.register(tool)

        retrieved = registry.get("file_read")
        assert retrieved is tool

    def test_list_tools(self):
        """Test listing tools"""
        from yanzhiti.core import ToolRegistry

        registry = ToolRegistry()
        registry.register(FileReadTool())
        registry.register(GlobTool())

        tools = registry.list_tools()
        assert len(tools) == 2


@pytest.mark.asyncio
class TestToolExecution:
    """Test tool execution"""

    async def test_file_read_tool(self, tmp_path):
        """Test file read tool"""
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")

        # Execute tool
        tool = FileReadTool()
        context = ToolContext(cwd=str(tmp_path))
        result = await tool.execute({"file_path": str(test_file)}, context)

        assert result.status.value == "success"
        assert "Hello, World!" in result.output

    async def test_glob_tool(self, tmp_path):
        """Test glob tool"""
        # Create test files
        (tmp_path / "test1.txt").write_text("content1")
        (tmp_path / "test2.txt").write_text("content2")
        (tmp_path / "test.py").write_text("content3")

        # Execute tool
        tool = GlobTool()
        context = ToolContext(cwd=str(tmp_path))
        result = await tool.execute({"pattern": "*.txt"}, context)

        assert result.status.value == "success"
        assert "test1.txt" in result.output
        assert "test2.txt" in result.output
        assert "test.py" not in result.output

    async def test_bash_tool(self):
        """Test bash tool"""
        tool = BashTool()
        context = ToolContext()
        result = await tool.execute({"command": "echo 'test'"}, context)

        assert result.status.value == "success"
        assert "test" in result.output
