"""Type definitions and protocol specifications for MCP."""

from .exceptions import McpError
from .version import SUPPORTED_PROTOCOL_VERSIONS
from .protocol import *  # Re-export all protocol types

__all__ = [
    "McpError",
    "SUPPORTED_PROTOCOL_VERSIONS",
] 