#!/usr/bin/env python
"""
Simple test client for the BigQuery MCP server.
This script only tries to connect to the server without executing any queries.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from .env file in the project root
load_dotenv()


async def simple_test():
    """Run a simple test that just connects to the server."""
    print("Debug: Starting simple test client")
    print(f"Debug: Python version: {sys.version}")
    print(f"Debug: Current working directory: {os.getcwd()}")

    # Configure server parameters
    server_path = os.path.join(
        os.getcwd(),
        "mcp-bigquery",
        "src",
        "mcp_server_bigquery",
        "__main__.py",
    )
    print(f"Debug: Server path: {server_path}")
    print(f"Debug: Server path exists: {os.path.exists(server_path)}")

    # Set a timeout for the connection attempt
    print("Setting connection timeout to 10 seconds")
    connection_timeout = 10  # seconds

    # Connect to the server with timeout
    print("Connecting to BigQuery MCP server...")
    try:
        # Create a task for the connection attempt
        connection_task = asyncio.create_task(connect_to_server(server_path))

        # Wait for the task to complete with a timeout
        try:
            await asyncio.wait_for(connection_task, timeout=connection_timeout)
            print("Connection successful!")
        except asyncio.TimeoutError:
            print(f"Connection timed out after {connection_timeout} seconds")
            print("This might indicate an issue with the server or the communication")
            print("Check the server logs for more information")
    except Exception as e:
        print(f"Error: {e}")


async def connect_to_server(server_path):
    """Connect to the server and return when connected."""
    try:
        server_params = StdioServerParameters(
            command="python",
            args=[server_path],
            env=os.environ,
        )

        print("Debug: Creating stdio client")
        try:
            async with stdio_client(server_params) as (read, write):
                print("Debug: stdio client created successfully")
                try:
                    print("Debug: Creating client session")
                    async with ClientSession(read, write) as session:
                        print("Debug: Initializing session")
                        await session.initialize()
                        print("Connected to server!")
                        # Just return after connecting
                        return
                except Exception as e:
                    import traceback

                    print(f"Debug: Error in client session: {e}")
                    print("Traceback:")
                    traceback.print_exc()
                    raise
        except Exception as e:
            import traceback

            print(f"Debug: Error in stdio client: {e}")
            print("Traceback:")
            traceback.print_exc()
            raise
    except Exception as e:
        import traceback

        print(f"Debug: Error in connect_to_server: {e}")
        print("Traceback:")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    try:
        asyncio.run(simple_test())
    except Exception as e:
        import traceback

        print(f"Main exception: {e}")
        print("Traceback:")
        traceback.print_exc()
