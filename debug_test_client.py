#!/usr/bin/env python
"""
Debug version of the test client for the BigQuery MCP server.
This script adds more debugging information to help identify connection issues.
"""

import asyncio
import os
import json
import sys
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from .env file in the project root
load_dotenv()  # This will look for .env in the current directory or parent directories


async def test_client():
    """Run a test client that connects to the BigQuery MCP server."""

    print("Debug: Starting test client with more debugging information")
    print(f"Debug: Python version: {sys.version}")
    print(f"Debug: Current working directory: {os.getcwd()}")

    # Configure server parameters
    # Use the correct path to the mcp-bigquery package
    server_path = os.path.join(
        os.getcwd(),
        "mcp-bigquery",
        "src",
        "mcp_server_bigquery",
        "__main__.py",
    )
    print(f"Debug: Server path: {server_path}")
    print(f"Debug: Server path exists: {os.path.exists(server_path)}")

    server_params = StdioServerParameters(
        command="python",
        args=[server_path],
        env=os.environ,
    )

    # Connect to the server
    print("Connecting to BigQuery MCP server...")
    try:
        print("Debug: Creating stdio client")
        async with stdio_client(server_params) as (read, write):
            print("Debug: stdio client created successfully")
            try:
                print("Debug: Creating client session")
                async with ClientSession(read, write) as session:
                    print("Debug: Initializing session")
                    await session.initialize()
                    print("Connected to server!")

                    # Test list_tables tool
                    print("\nListing tables...")
                    result = await session.call_tool("list_tables", {})
                    print_result(result)

                    # Test execute_query tool with a simple query
                    print("\nExecuting a simple query...")
                    query = "SELECT 1 as test"
                    result = await session.call_tool("execute_query", {"query": query})
                    print_result(result)

                    print("\nTest completed successfully!")
            except Exception as e:
                print(f"Debug: Error in client session: {e}")
                raise
    except Exception as e:
        print(f"Debug: Error in stdio client: {e}")
        raise


def print_result(result):
    """Print the result of a tool call in a formatted way."""
    if result.content:
        text = result.content[0].text
        try:
            # Try to parse as JSON for pretty printing
            parsed = json.loads(text)
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
            # If not JSON, print as is
            print(text)
    else:
        print("No content in result")


if __name__ == "__main__":
    try:
        asyncio.run(test_client())
    except Exception as e:
        print(f"Debug: Error in main: {e}")
        raise
