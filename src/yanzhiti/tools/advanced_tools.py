"""
Additional Tools - NotebookEdit, AskUser, etc.
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from yanzhiti.core.tool import Tool, ToolContext, ToolResult
from yanzhiti.types import ToolResultStatus


class NotebookEditTool(Tool):
    """Tool for editing Jupyter notebooks"""

    def __init__(self):
        super().__init__(
            name="notebook_edit",
            description="Edit a Jupyter notebook cell",
        )

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "notebook_path": {
                    "type": "string",
                    "description": "Path to the notebook file",
                },
                "cell_index": {
                    "type": "integer",
                    "description": "Index of the cell to edit",
                },
                "new_source": {
                    "type": "string",
                    "description": "New source code for the cell",
                },
                "cell_type": {
                    "type": "string",
                    "enum": ["code", "markdown"],
                    "description": "Type of the cell",
                },
            },
            "required": ["notebook_path", "cell_index", "new_source"],
        }

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        notebook_path = input_data["notebook_path"]
        cell_index = input_data["cell_index"]
        new_source = input_data["new_source"]
        cell_type = input_data.get("cell_type", "code")

        try:
            path = Path(notebook_path)
            if not path.exists():
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Notebook not found: {notebook_path}",
                )

            # Read notebook
            with open(path) as f:
                notebook = json.load(f)

            # Validate cell index
            if cell_index < 0 or cell_index >= len(notebook["cells"]):
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Invalid cell index: {cell_index}",
                )

            # Edit cell
            notebook["cells"][cell_index]["source"] = new_source.split('\n')
            notebook["cells"][cell_index]["cell_type"] = cell_type

            # Write notebook
            with open(path, 'w') as f:
                json.dump(notebook, f, indent=2)

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=f"Edited cell {cell_index} in {notebook_path}",
                metadata={"notebook_path": notebook_path, "cell_index": cell_index},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error editing notebook: {str(e)}",
            )


class AskUserQuestionTool(Tool):
    """Tool for asking user questions interactively"""

    def __init__(self):
        super().__init__(
            name="ask_user",
            description="Ask the user a question and get their response",
        )
        self._prompt_callback = None

    def set_prompt_callback(self, callback):
        """Set callback for prompting user"""
        self._prompt_callback = callback

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question to ask the user",
                },
                "options": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of options for the user to choose from",
                },
                "default": {
                    "type": "string",
                    "description": "Default value if user doesn't respond",
                },
            },
            "required": ["question"],
        }

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        question = input_data["question"]
        options = input_data.get("options", [])
        default = input_data.get("default")

        try:
            if self._prompt_callback:
                # Use custom prompt callback
                response = await self._prompt_callback(question, options, default)
            else:
                # Default: use console input
                if options:
                    options_str = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(options))
                    prompt = f"{question}\n\n{options_str}\n\nYour choice (1-{len(options)}): "
                else:
                    prompt = f"{question}: "

                # Run input in executor to avoid blocking
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, input, prompt)

                # Parse option choice
                if options and response.strip().isdigit():
                    idx = int(response.strip()) - 1
                    if 0 <= idx < len(options):
                        response = options[idx]

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=response,
                metadata={"question": question, "response": response},
            )

        except Exception as e:
            # Return default if available
            if default:
                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=default,
                    metadata={"question": question, "default_used": True},
                )

            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error getting user input: {str(e)}",
            )


class ImageAnalyzerTool(Tool):
    """Tool for analyzing images"""

    def __init__(self):
        super().__init__(
            name="image_analyzer",
            description="Analyze an image and extract information",
        )

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the image file",
                },
                "task": {
                    "type": "string",
                    "description": "What to analyze (e.g., 'describe', 'extract text', 'detect objects')",
                },
            },
            "required": ["image_path", "task"],
        }

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        image_path = input_data["image_path"]
        task = input_data["task"]

        try:
            path = Path(image_path)
            if not path.exists():
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Image not found: {image_path}",
                )

            # Check if it's an image file
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
            if path.suffix.lower() not in image_extensions:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Not an image file: {image_path}",
                )

            # For now, return basic info
            # In a full implementation, this would use vision models
            stat = path.stat()
            result = {
                "path": str(path),
                "size": stat.st_size,
                "task": task,
                "note": "Image analysis requires vision model integration",
            }

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=json.dumps(result, indent=2),
                metadata=result,
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error analyzing image: {str(e)}",
            )


class CodeSearchTool(Tool):
    """Tool for semantic code search"""

    def __init__(self):
        super().__init__(
            name="code_search",
            description="Search for code using semantic understanding",
        )

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (natural language or code pattern)",
                },
                "path": {
                    "type": "string",
                    "description": "Directory to search in",
                },
                "language": {
                    "type": "string",
                    "description": "Programming language to filter",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results",
                },
            },
            "required": ["query"],
        }

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        query = input_data["query"]
        search_path = input_data.get("path", context.cwd)
        language = input_data.get("language")
        max_results = input_data.get("max_results", 10)

        try:
            path = Path(search_path)
            results = []

            # Language to extension mapping
            lang_ext = {
                "python": ".py",
                "javascript": ".js",
                "typescript": ".ts",
                "java": ".java",
                "cpp": ".cpp",
                "c": ".c",
                "go": ".go",
                "rust": ".rs",
            }

            # Get file extension filter
            ext_filter = lang_ext.get(language.lower()) if language else None

            # Search files
            for file_path in path.rglob("*"):
                if not file_path.is_file():
                    continue

                if ext_filter and file_path.suffix != ext_filter:
                    continue

                # Skip common non-code directories
                if any(part in {'node_modules', 'venv', '__pycache__', '.git', 'dist', 'build'}
                       for part in file_path.parts):
                    continue

                try:
                    with open(file_path, encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Simple text matching (semantic search would use embeddings)
                    if query.lower() in content.lower():
                        # Find matching lines
                        lines = content.split('\n')
                        matches = []
                        for i, line in enumerate(lines):
                            if query.lower() in line.lower():
                                matches.append({
                                    "line": i + 1,
                                    "content": line.strip()[:100],
                                })

                        results.append({
                            "file": str(file_path),
                            "matches": matches[:3],  # Top 3 matches per file
                        })

                        if len(results) >= max_results:
                            break

                except Exception:
                    continue

            output = json.dumps(results, indent=2)

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=output,
                metadata={"query": query, "results": len(results)},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error searching code: {str(e)}",
            )


class DiagramGeneratorTool(Tool):
    """Tool for generating diagrams from code"""

    def __init__(self):
        super().__init__(
            name="diagram",
            description="Generate diagrams (UML, flowchart, etc.) from code or description",
        )

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["flowchart", "sequence", "class", "component"],
                    "description": "Type of diagram to generate",
                },
                "description": {
                    "type": "string",
                    "description": "Description of the diagram",
                },
                "code_path": {
                    "type": "string",
                    "description": "Optional path to code file to analyze",
                },
                "output_format": {
                    "type": "string",
                    "enum": ["mermaid", "plantuml", "svg"],
                    "description": "Output format for the diagram",
                },
            },
            "required": ["type", "description"],
        }

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        diagram_type = input_data["type"]
        description = input_data["description"]
        output_format = input_data.get("output_format", "mermaid")

        try:
            # Generate Mermaid diagram (simplified)
            if output_format == "mermaid":
                if diagram_type == "flowchart":
                    diagram = f"""graph TD
    A[Start] --> B[Process]
    B --> C{{Decision}}
    C -->|Yes| D[Action 1]
    C -->|No| E[Action 2]
    D --> F[End]
    E --> F

    %% {description}
"""
                elif diagram_type == "sequence":
                    diagram = f"""sequenceDiagram
    participant A as Actor
    participant S as System
    A->>S: Request
    S-->>A: Response

    %% {description}
"""
                elif diagram_type == "class":
                    diagram = f"""classDiagram
    class MyClass {{
        +attribute: str
        +method(): void
    }}

    %% {description}
"""
                else:
                    diagram = f"graph TD\n    A[{description}]"

                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=diagram,
                    metadata={
                        "type": diagram_type,
                        "format": output_format,
                    },
                )
            else:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Unsupported output format: {output_format}",
                )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error generating diagram: {str(e)}",
            )
