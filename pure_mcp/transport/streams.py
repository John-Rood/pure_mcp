"""
Pure Python implementation of memory streams for MCP communication.
No external dependencies required.
"""
import asyncio
from typing import Optional, TypeVar, Generic, Tuple


T = TypeVar('T')


class MemoryObjectSendStream(Generic[T]):
    """Memory stream for sending objects."""
    
    def __init__(self, max_buffer_size: int = 0):
        self._queue: asyncio.Queue[T] = asyncio.Queue(maxsize=max_buffer_size)
        self._closed = False
    
    def get_queue(self) -> asyncio.Queue[T]:
        """Get the underlying queue."""
        return self._queue
    
    async def send(self, item: T) -> None:
        """Send an item to the stream."""
        if self._closed:
            raise RuntimeError("Stream is closed")
        await self._queue.put(item)
    
    async def aclose(self) -> None:
        """Close the stream."""
        self._closed = True
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self._closed and self._queue.empty():
            raise StopAsyncIteration
        return await self._queue.get()


class MemoryObjectReceiveStream(Generic[T]):
    """Memory stream for receiving objects."""
    
    def __init__(self, send_stream: Optional['MemoryObjectSendStream[T]'] = None):
        self._send_stream = send_stream
        # Access the queue through a public method to avoid protected access
        self._queue: asyncio.Queue[T] = send_stream.get_queue() if send_stream else asyncio.Queue()
        self._closed = False
    
    async def receive(self) -> T:
        """Receive an item from the stream."""
        if self._closed:
            raise RuntimeError("Stream is closed")
        try:
            return await self._queue.get()
        except asyncio.CancelledError:
            raise RuntimeError("Stream closed")
    
    async def aclose(self) -> None:
        """Close the stream."""
        self._closed = True
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self._closed and self._queue.empty():
            raise StopAsyncIteration
        try:
            return await self.receive()
        except RuntimeError:
            raise StopAsyncIteration


def create_memory_object_stream(max_buffer_size: int = 0) -> Tuple[MemoryObjectSendStream[T], MemoryObjectReceiveStream[T]]:
    """Create a connected pair of memory object streams."""
    send_stream = MemoryObjectSendStream[T](max_buffer_size)
    receive_stream = MemoryObjectReceiveStream[T](send_stream)
    return send_stream, receive_stream
