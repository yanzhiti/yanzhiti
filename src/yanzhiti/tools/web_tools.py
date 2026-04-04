"""
Web operation tools
"""

import re
from typing import Any

import httpx

from yanzhiti.core.tool import Tool, ToolContext, ToolInputSchema, ToolResult
from yanzhiti.types import PermissionResult, ToolResultStatus


class WebFetchTool(Tool):
    """Tool for fetching web content"""

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
                    "description": "The URL to fetch",
                },
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
                    "description": "HTTP method (default: GET)",
                },
                "headers": {
                    "type": "object",
                    "description": "HTTP headers to send",
                },
                "body": {
                    "type": "string",
                    "description": "Request body (for POST/PUT/PATCH)",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds (default: 30)",
                },
            },
            required=["url"],
        )

    async def check_permission(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> PermissionResult:
        # Check if URL is allowed
        # For now, allow all - implement proper URL whitelist later
        return PermissionResult(granted=True)

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        url = input_data["url"]
        method = input_data.get("method", "GET").upper()
        headers = input_data.get("headers", {})
        body = input_data.get("body")
        timeout = input_data.get("timeout", 30)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                request_params = {
                    "url": url,
                    "headers": headers,
                }

                if body and method in ["POST", "PUT", "PATCH"]:
                    request_params["content"] = body

                response = await client.request(method, **request_params)

                # Try to decode as text
                try:
                    content = response.text
                except UnicodeDecodeError:
                    content = f"Binary content ({len(response.content)} bytes)"

                output = [
                    f"URL: {url}",
                    f"Method: {method}",
                    f"Status: {response.status_code}",
                    f"Headers: {dict(response.headers)}",
                    "",
                    "Content:",
                    content[:10000],  # Limit content size
                ]

                if len(content) > 10000:
                    output.append(f"\n... (truncated, {len(content)} total characters)")

                return ToolResult(
                    status=ToolResultStatus.SUCCESS
                    if response.is_success
                    else ToolResultStatus.ERROR,
                    output="\n".join(output),
                    metadata={
                        "url": url,
                        "method": method,
                        "status_code": response.status_code,
                        "content_length": len(response.content),
                    },
                )

        except httpx.TimeoutException:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Request timed out after {timeout} seconds",
            )
        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error fetching URL: {str(e)}",
            )


class WebSearchTool(Tool):
    """Tool for searching the web"""

    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information",
        )
        # Note: This is a mock implementation
        # In production, you would integrate with a real search API
        # like Google Custom Search, Bing, DuckDuckGo, etc.

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "query": {
                    "type": "string",
                    "description": "Search query",
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return (default: 10)",
                },
            },
            required=["query"],
        )

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        query = input_data["query"]
        num_results = input_data.get("num_results", 10)

        # Mock implementation - in production, use a real search API
        # This is just to demonstrate the tool structure

        mock_results = [
            {
                "title": f"Result {i + 1} for '{query}'",
                "url": f"https://example.com/result{i + 1}",
                "snippet": f"This is a mock search result {i + 1} for the query '{query}'. "
                f"In production, this would be a real search result from a search API.",
            }
            for i in range(min(num_results, 5))
        ]

        output = [f"Search results for: {query}", ""]
        for i, result in enumerate(mock_results, 1):
            output.extend(
                [
                    f"{i}. {result['title']}",
                    f"   URL: {result['url']}",
                    f"   {result['snippet']}",
                    "",
                ]
            )

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output="\n".join(output),
            metadata={
                "query": query,
                "num_results": len(mock_results),
                "note": "Mock implementation - integrate with real search API in production",
            },
        )


class WebScrapeTool(Tool):
    """Tool for scraping web pages"""

    def __init__(self):
        super().__init__(
            name="web_scrape",
            description="Scrape and extract content from web pages",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "url": {
                    "type": "string",
                    "description": "URL to scrape",
                },
                "selector": {
                    "type": "string",
                    "description": "CSS selector to extract specific elements",
                },
                "extract": {
                    "type": "string",
                    "enum": ["text", "html", "links", "images"],
                    "description": "What to extract (default: text)",
                },
            },
            required=["url"],
        )

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        url = input_data["url"]
        extract = input_data.get("extract", "text")

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(url)

                if not response.is_success:
                    return ToolResult(
                        status=ToolResultStatus.ERROR,
                        error=f"Failed to fetch URL: {response.status_code}",
                    )

                html = response.text

                # Simple extraction without full HTML parser
                # In production, use BeautifulSoup or lxml
                if extract == "text":
                    # Remove HTML tags (simple approach)
                    text = re.sub(r"<[^>]+>", "", html)
                    text = re.sub(r"\s+", " ", text).strip()
                    content = text[:5000]
                elif extract == "links":
                    # Extract links
                    links = re.findall(r'href=["\']([^"\']+)["\']', html)
                    content = "\n".join(links[:100])
                elif extract == "images":
                    # Extract image URLs
                    images = re.findall(
                        r'src=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp))["\']', html, re.I
                    )
                    content = "\n".join(images[:100])
                else:
                    content = html[:5000]

                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=content,
                    metadata={
                        "url": url,
                        "extract": extract,
                        "content_length": len(content),
                    },
                )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error scraping URL: {str(e)}",
            )


class APITestTool(Tool):
    """Tool for testing REST APIs"""

    def __init__(self):
        super().__init__(
            name="api_test",
            description="Test REST API endpoints",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "url": {
                    "type": "string",
                    "description": "API endpoint URL",
                },
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
                    "description": "HTTP method",
                },
                "headers": {
                    "type": "object",
                    "description": "Request headers",
                },
                "params": {
                    "type": "object",
                    "description": "Query parameters",
                },
                "json": {
                    "type": "object",
                    "description": "JSON body",
                },
                "expected_status": {
                    "type": "integer",
                    "description": "Expected status code",
                },
            },
            required=["url", "method"],
        )

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        url = input_data["url"]
        method = input_data["method"]
        headers = input_data.get("headers", {})
        params = input_data.get("params")
        json_body = input_data.get("json")
        expected_status = input_data.get("expected_status")

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json_body,
                )

                output = [
                    f"API Test: {method} {url}",
                    f"Status: {response.status_code}",
                    f"Headers: {dict(response.headers)}",
                ]

                # Check status if expected
                if expected_status:
                    status_match = response.status_code == expected_status
                    output.append(
                        f"Expected Status: {expected_status} ({'✓' if status_match else '✗'})"
                    )

                # Try to parse JSON
                try:
                    json_response = response.json()
                    import json

                    output.append(f"\nResponse:\n{json.dumps(json_response, indent=2)}")
                except Exception:
                    output.append(f"\nResponse:\n{response.text[:1000]}")

                success = response.is_success
                if expected_status:
                    success = response.status_code == expected_status

                return ToolResult(
                    status=ToolResultStatus.SUCCESS if success else ToolResultStatus.ERROR,
                    output="\n".join(output),
                    metadata={
                        "url": url,
                        "method": method,
                        "status_code": response.status_code,
                        "expected_status": expected_status,
                    },
                )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"API test failed: {str(e)}",
            )
