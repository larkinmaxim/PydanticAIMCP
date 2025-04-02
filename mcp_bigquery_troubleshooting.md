# MCP BigQuery Server Troubleshooting

This document provides detailed information about the issues encountered when trying to run the BigQuery MCP server and potential solutions.

## Issues Encountered

When testing the BigQuery MCP server, we encountered several issues:

1. The test client kept connecting to the PydanticAI server that generates poems about socks instead of the BigQuery MCP server.
2. We had Python version compatibility issues with the BigQuery MCP server package.
3. We fixed the Python version compatibility issue, but we still had issues with the MCP server due to asyncio conflicts.
4. We tried to create a custom server implementation to avoid asyncio conflicts, but we ran into issues with the `StdioServerTransport` class not being available.
5. We tried to use the `stdio_server` function instead, but we still had issues with the event loop.
6. Finally, we created a simple BigQuery client that connects directly to BigQuery without using the MCP framework, and it works correctly.

The main issue appears to be related to how the MCP framework handles asyncio event loops. There might be a conflict between the event loop used by the MCP framework and the event loop used by the BigQuery client.

## Potential Solutions

### 1. Using a Different Approach to Handle Asyncio Event Loops

The main issue we encountered was related to nested asyncio event loops. Here are more detailed approaches to solve this:

#### Option 1: Use a Custom Event Loop Policy

You could implement a custom event loop policy that allows nested event loops:

```python
import asyncio
import contextvars
import threading

class NestedEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    """Event loop policy that allows nested event loops."""
    
    def __init__(self):
        super().__init__()
        self._loop_stack = contextvars.ContextVar('loop_stack', default=[])
        
    def get_event_loop(self):
        loop_stack = self._loop_stack.get()
        if loop_stack:
            return loop_stack[-1]
        return super().get_event_loop()
        
    def set_event_loop(self, loop):
        loop_stack = self._loop_stack.get()
        loop_stack.append(loop)
        self._loop_stack.set(loop_stack)
        super().set_event_loop(loop)
        
    def reset_event_loop(self):
        loop_stack = self._loop_stack.get()
        if loop_stack:
            loop_stack.pop()
            self._loop_stack.set(loop_stack)
        super().reset_event_loop()
```

Then set this policy before running your MCP server:

```python
asyncio.set_event_loop_policy(NestedEventLoopPolicy())
```

#### Option 2: Use Separate Processes

Another approach is to run the MCP server and the BigQuery client in separate processes:

```python
from multiprocessing import Process

def run_mcp_server():
    # MCP server code here
    pass

def run_bigquery_client():
    # BigQuery client code here
    pass

if __name__ == "__main__":
    server_process = Process(target=run_mcp_server)
    client_process = Process(target=run_bigquery_client)
    
    server_process.start()
    client_process.start()
    
    server_process.join()
    client_process.join()
```

#### Option 3: Use Synchronous APIs Where Possible

For some operations, you might be able to use synchronous APIs instead of async ones:

```python
# Instead of:
async def execute_query(query):
    result = await db.execute_query(query)
    return result

# Use:
def execute_query(query):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(db.execute_query(query))
        return result
    finally:
        loop.close()
```

### 2. Using a Different Version of the MCP Framework

The MCP framework might have compatibility issues with the version of Python or the BigQuery client you're using. Here are some options:

#### Option 1: Check for MCP Framework Updates

The MCP framework might have updates that address the asyncio compatibility issues:

```bash
pip install --upgrade mcp
```

#### Option 2: Use an Older Version of the MCP Framework

If the latest version has introduced incompatibilities, you might try an older version:

```bash
pip install mcp==1.5.0  # Replace with a known working version
```

#### Option 3: Fork and Modify the MCP Framework

You could fork the MCP framework repository and modify it to work with your specific use case:

1. Clone the MCP framework repository
2. Modify the code to handle asyncio event loops differently
3. Install your modified version

#### Option 4: Use a Different Framework

There might be other frameworks that provide similar functionality but with better compatibility:

- FastAPI with WebSockets for real-time communication
- gRPC for efficient RPC communication
- A simple REST API using Flask or FastAPI

## Current Workaround

For now, you can use the `simple_bigquery_client.py` script to interact with BigQuery directly. This script demonstrates that the BigQuery connection itself is working correctly, which is a good starting point for further development.
