# Pure MCP Client

A lightweight, pure Python implementation of the Model Context Protocol (MCP) client that enables communication with MCP servers without external SDK dependencies.

## Why Pure MCP?

While the official MCP SDK is comprehensive, it comes with heavy dependencies and complex abstractions that can be overkill for many use cases. Pure MCP addresses common pain points:

- **🪶 Lightweight Deployments**: Minimal dependencies mean faster Docker builds, smaller Lambda packages, and easier integration into existing projects
- **🔒 Dependency Control**: No surprise transitive dependencies or version conflicts with your existing stack
- **🚀 Cloud-Friendly**: Perfect for serverless, containers, or any environment where package size matters
- **⚡ Simple Integration**: Drop into any Python project without restructuring your codebase
- **🎯 Just What You Need**: Full MCP protocol support without the bloat

**Choose Pure MCP when you want MCP functionality without the overhead.**

## Features

- **Minimal Dependencies**: Core functionality using only Python standard library
- **Full Protocol Support**: Complete implementation of MCP including tools, resources, prompts, and completions
- **Type-Safe**: Comprehensive Pydantic models for all protocol types
- **Async-First**: Built on Python's asyncio for efficient concurrent operations
- **Multiple Transports**: Support for Server-Sent Events (SSE) and streamable HTTP
- **Progress Tracking**: Monitor long-running operations with callbacks
- **Error Handling**: Robust error handling with typed exceptions

## Installation

```bash
# Install 
pip install pure-mcp

# Or install from source
git clone https://github.com/John-Rood/pure-mcp.git
cd pure-mcp
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
import asyncio
from pure_mcp import ClientSession, sse_client

async def main():
    # Connect to MCP server
    async with sse_client("http://localhost:8080/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize connection
            result = await session.initialize()
            print(f"Connected to: {result.serverInfo.name}")
            
            # List and call tools
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"Tool: {tool.name} - {tool.description}")

asyncio.run(main())
```

### Working with Tools

```python
async def use_tools():
    async with sse_client("http://localhost:8080/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # Call a tool
            result = await session.call_tool(
                name="search",
                arguments={"query": "Python MCP"}
            )
            
            # Process results
            for content in result.content:
                if hasattr(content, 'text'):
                    print(content.text)
```

### Resource Management

```python
async def manage_resources():
    async with sse_client("http://localhost:8080/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # List resources
            resources = await session.list_resources()
            
            # Read a resource
            if resources.resources:
                content = await session.read_resource(resources.resources[0].uri)
                for item in content.contents:
                    if hasattr(item, 'text'):
                        print(item.text)
```

### Using Prompts

```python
async def use_prompts():
    async with sse_client("http://localhost:8080/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # Get a prompt
            prompt_result = await session.get_prompt(
                name="code_review",
                arguments={"language": "python"}
            )
            
            for message in prompt_result.messages:
                print(f"{message.role}: {message.content.text}")
```

## Advanced Features

### Progress Tracking

Monitor progress for long-running operations:

```python
async def track_progress():
    async def progress_callback(progress: float, total: float | None, message: str | None):
        percent = (progress / total * 100) if total else 0
        print(f"Progress: {percent:.1f}% - {message or 'Processing...'}")
    
    async with sse_client("http://localhost:8080/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            result = await session.call_tool(
                name="long_task",
                arguments={"data": "large_input"},
                progress_callback=progress_callback
            )
```

### Custom Timeouts

Configure timeouts for different scenarios:

```python
from datetime import timedelta

# Session-level timeout
session = ClientSession(
    read_stream, 
    write_stream,
    read_timeout_seconds=timedelta(seconds=60)
)

# Per-request timeout
result = await session.call_tool(
    name="slow_tool",
    arguments={},
    read_timeout_seconds=timedelta(seconds=120)
)
```

### Error Handling

Handle MCP-specific errors:

```python
from pure_mcp import McpError

try:
    result = await session.call_tool("unknown_tool")
except McpError as e:
    print(f"Error {e.error.code}: {e.error.message}")
    if e.error.data:
        print(f"Details: {e.error.data}")
```

## Project Structure

```
pure_mcp/
├── __init__.py              # Package exports
├── core/                    # Core functionality
│   ├── client.py           # ClientSession implementation
│   ├── session.py          # Base session protocol
│   ├── context.py          # Request context management
│   └── message.py          # Message types and metadata
├── transport/              # Transport implementations
│   ├── sse.py             # Server-Sent Events transport
│   ├── streams.py         # Memory stream implementation
│   └── http_utils.py      # HTTP client utilities
└── types/                  # Type definitions
    ├── protocol.py        # MCP protocol types
    ├── exceptions.py      # Error types
    └── version.py         # Protocol version support
```

## API Reference

### ClientSession

The main interface for MCP communication.

#### Methods

- `initialize()` - Initialize connection and exchange capabilities
- `list_tools()` - Get available tools from the server
- `call_tool(name, arguments)` - Execute a tool with arguments
- `list_resources()` - Get available resources
- `read_resource(uri)` - Read resource content
- `list_prompts()` - Get available prompt templates
- `get_prompt(name, arguments)` - Get prompt with arguments
- `set_logging_level(level)` - Configure server logging
- `send_ping()` - Send keepalive ping

### Transport Configuration

#### sse_client

Connect using Server-Sent Events:

```python
async with sse_client(
    url="http://localhost:8080/sse",
    headers={"Authorization": "Bearer token"},
    timeout=30,
    sse_read_timeout=300
) as (read_stream, write_stream):
    # Use streams with ClientSession
```

## Supported Types

The package exports commonly used types:

- **Core Types**: `Tool`, `Resource`, `Prompt`
- **Result Types**: `InitializeResult`, `ListToolsResult`, `CallToolResult`, etc.
- **Content Types**: `TextContent`, `ImageContent`
- **Other Types**: `LoggingLevel`, `McpError`

## Protocol Versions

Supports MCP protocol versions:
- 2024-11-05
- 2025-03-26
- 2025-06-18 (latest)

## Requirements

- Python 3.8+
- anyio >= 3.0.0
- httpx >= 0.25.0
- httpx-sse >= 0.3.0
- pydantic >= 2.0.0
- jsonschema >= 4.0.0
- typing-extensions >= 4.0.0

## Examples

See `example.py` for complete working examples demonstrating:
- Basic connection and initialization
- Tool discovery and execution
- Resource listing and reading
- Prompt management
- Progress tracking
- Error handling

## Contributing

Contributions are welcome! Please ensure:
- Type hints for all functions
- Docstrings for public APIs
- Async-first implementations
- Tests for new features

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

This implementation provides a lightweight alternative to the official MCP SDK, focusing on minimal dependencies and cloud-friendly deployment. 