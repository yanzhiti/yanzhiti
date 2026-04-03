# Claude Code Python - Architecture Documentation

## Overview

Claude Code Python is a complete refactoring of Anthropic's Claude Code CLI from TypeScript to Python. This document describes the architecture, design decisions, and implementation details.

## Project Structure

```
yanzhiti-python/
├── src/yanzhiti/
│   ├── __init__.py              # Package initialization
│   ├── cli/                     # Command-line interface
│   │   ├── __init__.py
│   │   └── main.py              # CLI entry point
│   ├── core/                    # Core functionality
│   │   ├── __init__.py
│   │   ├── query_engine.py      # Query processing engine
│   │   └── tool.py              # Tool system base classes
│   ├── tools/                   # Tool implementations
│   │   ├── __init__.py
│   │   ├── file_tools.py        # File operation tools
│   │   └── shell_tools.py       # Shell execution tools
│   ├── types/                   # Type definitions
│   │   └── __init__.py          # Pydantic models
│   ├── bridge/                  # Communication layer (TODO)
│   ├── utils/                   # Utility functions (TODO)
│   ├── services/                # External services (TODO)
│   └── commands/                # Slash commands (TODO)
├── tests/                       # Test suite
│   └── test_tools.py
├── docs/                        # Documentation
├── examples/                    # Example usage
├── pyproject.toml               # Project configuration
└── README.md                    # Project README
```

## Core Components

### 1. QueryEngine

The `QueryEngine` is the heart of Claude Code. It:

- Processes user queries
- Calls the Anthropic API
- Executes tools
- Manages conversation state
- Tracks usage and statistics

**Key Methods:**
- `query(user_input)` - Process a user query
- `_call_api()` - Make API call to Claude
- `_process_response()` - Handle API response
- `_execute_tool()` - Execute a tool
- `reset()` - Reset session state
- `get_stats()` - Get session statistics

### 2. Tool System

The tool system is built around the `Tool` abstract base class:

```python
class Tool(ABC):
    - name: str
    - description: str
    - input_schema: ToolInputSchema

    Methods:
    - execute(input_data, context) -> ToolResult
    - validate_input(input_data) -> ValidationResult
    - check_permission(input_data, context) -> PermissionResult
    - to_anthropic_format() -> Dict
```

**Tool Lifecycle:**
1. Validate input against schema
2. Check permissions
3. Execute tool
4. Return result

**Tool Registry:**
- Manages available tools
- Provides tool lookup
- Converts tools to Anthropic format

### 3. Type System

All types are defined using Pydantic models for:

- Runtime validation
- Serialization/deserialization
- Type safety
- Documentation

**Key Types:**
- `Message` - Base message type
- `UserMessage`, `AssistantMessage`, `SystemMessage`
- `ToolUseBlock`, `ToolResultBlock`
- `PermissionResult`, `ValidationResult`
- `ToolResult`, `ToolContext`
- `Usage`, `SessionInfo`, `AppState`

### 4. CLI Interface

The CLI is built with Click and Rich:

- **Click** - Command-line argument parsing
- **Rich** - Beautiful terminal output

**Features:**
- Interactive REPL mode
- Single query mode
- Special commands (/help, /stats, /reset, /exit)
- Markdown rendering
- Progress indicators
- Syntax highlighting

## Implemented Tools

### File Tools

1. **FileReadTool** - Read file contents
   - Supports offset and limit
   - Line number formatting
   - Error handling

2. **FileWriteTool** - Write file contents
   - Creates parent directories
   - Overwrites existing files

3. **FileEditTool** - Edit files
   - Find and replace
   - Single or all occurrences

4. **GlobTool** - Find files by pattern
   - Recursive search
   - Sorted by modification time

5. **GrepTool** - Search file contents
   - Regex support
   - File filtering

### Shell Tools

1. **BashTool** - Execute bash commands
   - Timeout support
   - Working directory control
   - Exit code tracking

2. **PowerShellTool** - Execute PowerShell (Windows)
   - Windows-only
   - Same features as BashTool

3. **TaskTool** - Background task management
   - Create, list, stop, output
   - Async execution

## Design Decisions

### Why Python?

1. **Ecosystem** - Rich AI/ML ecosystem
2. **Readability** - Clean, expressive syntax
3. **Type Safety** - Type hints + Pydantic
4. **Async Support** - Native async/await
5. **Community** - Large, active community

### Why Pydantic?

1. **Validation** - Automatic input validation
2. **Serialization** - JSON/dict conversion
3. **Documentation** - Self-documenting schemas
4. **IDE Support** - Excellent autocomplete
5. **Performance** - Rust-based core

### Why Click + Rich?

1. **Click** - De facto standard for CLI
2. **Rich** - Beautiful terminal output
3. **Integration** - Work well together
4. **Features** - Progress, tables, markdown

### Async Architecture

All I/O operations are async:

- File operations (aiofiles)
- API calls (httpx/anthropic)
- Shell execution (asyncio.subprocess)
- Tool execution

This enables:
- Concurrent operations
- Better performance
- Responsive UI
- Background tasks

## Comparison with TypeScript Version

### Similarities

- Same core architecture
- Same tool system design
- Same query loop
- Same API integration

### Differences

| Feature | TypeScript | Python |
|---------|-----------|--------|
| Type System | TypeScript interfaces | Pydantic models |
| Runtime | Node.js/Bun | Python 3.10+ |
| Package Manager | npm | pip/poetry |
| CLI Framework | Custom | Click |
| UI Framework | Ink (React) | Rich |
| Async | Promises | async/await |
| Testing | Jest | pytest |

## Future Work

### Phase 1: Core Completion
- [ ] Complete all 40+ tools
- [ ] Implement bridge system
- [ ] Add utility modules
- [ ] Complete type definitions

### Phase 2: Features
- [ ] MCP (Model Context Protocol) support
- [ ] Session persistence
- [ ] Configuration management
- [ ] Plugin system

### Phase 3: Advanced
- [ ] Multi-agent support
- [ ] Remote control
- [ ] Voice mode
- [ ] Web UI

### Phase 4: Polish
- [ ] Comprehensive tests
- [ ] Full documentation
- [ ] Performance optimization
- [ ] Error handling

## Contributing

See CONTRIBUTING.md for guidelines.

## License

MIT License - see LICENSE file.
