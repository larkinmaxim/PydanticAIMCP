#!/usr/bin/env python
"""
Test client for the BigQuery MCP server.
This script demonstrates how to connect to and use the BigQuery MCP server.
"""

import asyncio
import os
import json
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from .env file in the project root
load_dotenv()  # This will look for .env in the current directory or parent directories


async def test_client():
    """Run a test client that connects to the BigQuery MCP server."""

    # Configure server parameters
    # Use a more specific path to avoid conflicts with mcp_server.py in the root directory
    server_params = StdioServerParameters(
        command="python",
        args=[
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "src",
                "mcp_server_bigquery",
                "__main__.py",
            )
        ],
        env=os.environ,
    )

    # Connect to the server
    print("Connecting to BigQuery MCP server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
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

            # If you have actual tables, you can test describe_table
            # Uncomment and modify the following code:
            """
            print("\nDescribing a table...")
            table_name = "your_dataset.your_table"
            result = await session.call_tool("describe_table", {"table_name": table_name})
            print_result(result)
            """

            print("\nTest completed successfully!")


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
    asyncio.run(test_client())
