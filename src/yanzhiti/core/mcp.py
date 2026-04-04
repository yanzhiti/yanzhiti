"""
MCP (Model Context Protocol) Support
Integration with external tools and resources
"""

import asyncio
import json
from enum import Enum
from typing import Any

import httpx
from pydantic import BaseModel, Field


class MCPTransport(str, Enum):
    """MCP transport types"""
    STDIO = "stdio"
    HTTP = "http"
    WEBSOCKET = "websocket"
    SSE = "sse"  # Server-Sent Events


class MCPServerConfig(BaseModel):
    """Configuration for an MCP server"""
    name: str
    command: str | None = None  # For stdio transport
    url: str | None = None  # For http/ws transport
    transport: MCPTransport = MCPTransport.STDIO
    env: dict[str, str] = Field(default_factory=dict)
    args: list[str] = Field(default_factory=list)
    enabled: bool = True


class MCPTool(BaseModel):
    """An MCP tool definition"""
    name: str
    description: str
    input_schema: dict[str, Any]


class MCPResource(BaseModel):
    """An MCP resource"""
    uri: str
    name: str
    description: str | None = None
    mime_type: str | None = None


class MCPClient:
    """
    Client for communicating with MCP servers
    """

    def __init__(self, config: MCPServerConfig):
        self.config = config
        self.tools: list[MCPTool] = []
        self.resources: list[MCPResource] = []
        self._process: asyncio.subprocess.Process | None = None
        self._http_client: httpx.AsyncClient | None = None
        self._initialized = False

    async def connect(self):
        """Connect to the MCP server"""
        if self.config.transport == MCPTransport.STDIO:
            await self._connect_stdio()
        elif self.config.transport == MCPTransport.HTTP:
            await self._connect_http()
        elif self.config.transport == MCPTransport.WEBSOCKET:
            await self._connect_websocket()

        # Initialize connection
        await self._initialize()
        self._initialized = True

    async def _connect_stdio(self):
        """Connect via stdio"""
        if not self.config.command:
            raise ValueError("Command required for stdio transport")

        # Start subprocess
        self._process = await asyncio.create_subprocess_exec(
            self.config.command,
            *self.config.args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**dict(asyncio.os.environ), **self.config.env},
        )

    async def _connect_http(self):
        """Connect via HTTP"""
        if not self.config.url:
            raise ValueError("URL required for HTTP transport")

        self._http_client = httpx.AsyncClient(base_url=self.config.url)

    async def _connect_websocket(self):
        """Connect via WebSocket"""
        # WebSocket connection would be implemented here
        pass

    async def _initialize(self):
        """Initialize MCP connection and get capabilities"""
        # Send initialize request
        await self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "yanzhiti",
                "version": "1.0.0",
            }
        })

        # List tools
        try:
            tools_response = await self._send_request("tools/list", {})
            for tool_data in tools_response.get("tools", []):
                self.tools.append(MCPTool(
                    name=tool_data["name"],
                    description=tool_data.get("description", ""),
                    input_schema=tool_data.get("inputSchema", {}),
                ))
        except Exception:
            pass

        # List resources
        try:
            resources_response = await self._send_request("resources/list", {})
            for resource_data in resources_response.get("resources", []):
                self.resources.append(MCPResource(
                    uri=resource_data["uri"],
                    name=resource_data["name"],
                    description=resource_data.get("description"),
                    mime_type=resource_data.get("mimeType"),
                ))
        except Exception:
            pass

    async def _send_request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        """Send a request to the MCP server"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

        if self.config.transport == MCPTransport.STDIO:
            return await self._send_stdio_request(request)
        elif self.config.transport == MCPTransport.HTTP:
            return await self._send_http_request(request)
        else:
            raise NotImplementedError(f"Transport {self.config.transport} not implemented")

    async def _send_stdio_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Send request via stdio"""
        if not self._process or not self._process.stdin or not self._process.stdout:
            raise RuntimeError("Process not connected")

        # Send request
        request_str = json.dumps(request) + "\n"
        self._process.stdin.write(request_str.encode())
        await self._process.stdin.drain()

        # Read response
        response_str = await self._process.stdout.readline()
        response = json.loads(response_str.decode())

        if "error" in response:
            raise RuntimeError(f"MCP error: {response['error']}")

        return response.get("result", {})

    async def _send_http_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Send request via HTTP"""
        if not self._http_client:
            raise RuntimeError("HTTP client not connected")

        response = await self._http_client.post("/", json=request)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            raise RuntimeError(f"MCP error: {data['error']}")

        return data.get("result", {})

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Call an MCP tool"""
        if not self._initialized:
            await self.connect()

        response = await self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments,
        })

        return response.get("content", [])

    async def read_resource(self, uri: str) -> Any:
        """Read an MCP resource"""
        if not self._initialized:
            await self.connect()

        response = await self._send_request("resources/read", {
            "uri": uri,
        })

        return response.get("contents", [])

    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self._process:
            self._process.terminate()
            await self._process.wait()
            self._process = None

        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

        self._initialized = False


class MCPManager:
    """
    Manager for multiple MCP servers
    """

    def __init__(self):
        self.clients: dict[str, MCPClient] = {}
        self._tool_to_server: dict[str, str] = {}

    async def add_server(self, config: MCPServerConfig):
        """Add and connect to an MCP server"""
        client = MCPClient(config)
        await client.connect()
        self.clients[config.name] = client

        # Map tools to server
        for tool in client.tools:
            self._tool_to_server[tool.name] = config.name

    async def remove_server(self, name: str):
        """Remove and disconnect an MCP server"""
        if name in self.clients:
            await self.clients[name].disconnect()
            del self.clients[name]

            # Remove tool mappings
            self._tool_to_server = {
                k: v for k, v in self._tool_to_server.items() if v != name
            }

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Call a tool on the appropriate MCP server"""
        if tool_name not in self._tool_to_server:
            raise ValueError(f"Tool not found: {tool_name}")

        server_name = self._tool_to_server[tool_name]
        client = self.clients[server_name]

        return await client.call_tool(tool_name, arguments)

    async def read_resource(self, uri: str) -> Any:
        """Read a resource from an MCP server"""
        # Parse server name from URI (e.g., "server://resource")
        parts = uri.split("://", 1)
        if len(parts) == 2:
            server_name = parts[0]
            if server_name in self.clients:
                return await self.clients[server_name].read_resource(uri)

        raise ValueError(f"Invalid resource URI: {uri}")

    def list_tools(self) -> list[MCPTool]:
        """List all available MCP tools"""
        tools = []
        for client in self.clients.values():
            tools.extend(client.tools)
        return tools

    def list_resources(self) -> list[MCPResource]:
        """List all available MCP resources"""
        resources = []
        for client in self.clients.values():
            resources.extend(client.resources)
        return resources

    async def disconnect_all(self):
        """Disconnect all MCP servers"""
        for name in list(self.clients.keys()):
            await self.remove_server(name)


def create_mcp_tool_wrapper(mcp_manager: MCPManager, tool: MCPTool):
    """Create a Tool wrapper for an MCP tool"""
    from yanzhiti.core.tool import Tool, ToolContext, ToolResult
    from yanzhiti.types import ToolResultStatus

    class MCPToolWrapper(Tool):
        """Wrapper for MCP tool"""

        def __init__(self, mcp_tool: MCPTool, manager: MCPManager):
            super().__init__(
                name=mcp_tool.name,
                description=mcp_tool.description,
            )
            self.mcp_tool = mcp_tool
            self.manager = manager

        @property
        def input_schema(self) -> dict[str, Any]:
            return self.mcp_tool.input_schema

        async def execute(
            self,
            input_data: dict[str, Any],
            context: ToolContext,
        ) -> ToolResult:
            try:
                result = await self.manager.call_tool(
                    self.mcp_tool.name,
                    input_data
                )

                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=str(result),
                    metadata={"mcp_tool": self.mcp_tool.name},
                )
            except Exception as e:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"MCP tool error: {str(e)}",
                )

    return MCPToolWrapper(tool, mcp_manager)
