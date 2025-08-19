"""
Example usage of the Pure MCP Python Client.

This example demonstrates how to connect to an MCP server and perform basic operations.
"""

import asyncio
from typing import Union
from pure_mcp import ClientSession, sse_client, McpError


async def main():
    """Main example function demonstrating MCP client usage."""
    server_url = "http://localhost:8080/sse"  # Replace with your MCP server URL
    
    try:
        # Connect to MCP server using SSE transport
        async with sse_client(server_url) as (read_stream, write_stream):
            # Create a client session
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the connection
                print("Connecting to MCP server...")
                init_result = await session.initialize()
                print(f"Connected to: {init_result.serverInfo.name} v{init_result.serverInfo.version}")
                print(f"Server capabilities: {init_result.capabilities}")
                
                # List available tools
                print("\n--- Available Tools ---")
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"  {tool.name}: {tool.description}")
                    if tool.inputSchema:
                        print(f"    Input schema: {tool.inputSchema}")
                
                # Call a tool (example)
                if tools.tools:
                    tool_name = tools.tools[0].name
                    print(f"\n--- Calling tool: {tool_name} ---")
                    result = await session.call_tool(
                        name=tool_name,
                        arguments={"example": "argument"}  # Adjust based on tool requirements
                    )
                    for content in result.content:
                        if hasattr(content, 'text'):
                            print(f"Result: {content.text}")
                
                # List resources
                print("\n--- Available Resources ---")
                resources = await session.list_resources()
                for resource in resources.resources:
                    print(f"  {resource.name}: {resource.uri}")
                    if resource.description:
                        print(f"    {resource.description}")
                
                # Read a resource (if any exist)
                if resources.resources:
                    resource_uri = resources.resources[0].uri
                    print(f"\n--- Reading resource: {resource_uri} ---")
                    content = await session.read_resource(resource_uri)
                    for item in content.contents:
                        if hasattr(item, 'text'):
                            print(f"Content: {item.text[:200]}...")  # First 200 chars
                
                # List prompts
                print("\n--- Available Prompts ---")
                prompts = await session.list_prompts()
                for prompt in prompts.prompts:
                    print(f"  {prompt.name}")
                    if prompt.description:
                        print(f"    {prompt.description}")
                    if prompt.arguments:
                        print(f"    Arguments: {[arg.name for arg in prompt.arguments]}")
                
                # Get a prompt (if any exist)
                if prompts.prompts:
                    prompt_name = prompts.prompts[0].name
                    print(f"\n--- Getting prompt: {prompt_name} ---")
                    prompt_result = await session.get_prompt(
                        name=prompt_name,
                        arguments={}  # Add arguments as needed
                    )
                    for message in prompt_result.messages:
                        print(f"  {message.role}: {message.content.text if hasattr(message.content, 'text') else message.content}")
                
    except McpError as e:
        print(f"MCP Error: {e.error.code} - {e.error.message}")
        if e.error.data:
            print(f"Additional info: {e.error.data}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")


async def example_with_progress():
    """Example showing progress tracking for long-running operations."""
    server_url = "http://localhost:8080/sse"
    
    async def progress_callback(progress: float, total: Union[float, None], message: Union[str, None]):
        """Handle progress updates."""
        percent = (progress / total * 100) if total else 0
        print(f"Progress: {percent:.1f}% - {message or 'Processing...'}")
    
    async with sse_client(server_url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # Call a long-running tool with progress tracking
            result = await session.call_tool(
                name="long_running_task",
                arguments={"data": "large dataset"},
                progress_callback=progress_callback
            )
            print("Task completed!")


if __name__ == "__main__":
    # Run the main example
    asyncio.run(main())
    
    # Uncomment to run the progress example
    # asyncio.run(example_with_progress()) 