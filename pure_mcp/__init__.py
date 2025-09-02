"""
Pure Python MCP Client - A lightweight Model Context Protocol implementation

This package provides a minimal yet complete MCP client implementation using 
only Python standard library components for core functionality.
"""

# Core client interface
from .core.client import ClientSession

# Transport layers
from .transport.sse import sse_client
from .transport.streamable_http import streamablehttp_client
from .transport.streams import (
    MemoryObjectSendStream,
    MemoryObjectReceiveStream,
    create_memory_object_stream
)

# Types
from .types.exceptions import McpError
from .types.protocol import (
    # Common types
    Tool,
    Resource,
    Prompt,
    # Results
    InitializeResult,
    ListToolsResult,
    CallToolResult,
    ListResourcesResult,
    ReadResourceResult,
    ListPromptsResult,
    GetPromptResult,
    # Other useful types
    TextContent,
    ImageContent,
    LoggingLevel,
)

from ._version import __version__

__all__ = [
    # Main client
    "ClientSession",
    # Transport
    "sse_client",
    "streamablehttp_client",
    "MemoryObjectSendStream",
    "MemoryObjectReceiveStream", 
    "create_memory_object_stream",
    # Exceptions
    "McpError",
    # Common types
    "Tool",
    "Resource",
    "Prompt",
    # Results
    "InitializeResult",
    "ListToolsResult",
    "CallToolResult",
    "ListResourcesResult", 
    "ReadResourceResult",
    "ListPromptsResult",
    "GetPromptResult",
    # Content types
    "TextContent",
    "ImageContent",
    "LoggingLevel",
] 