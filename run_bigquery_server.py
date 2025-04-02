#!/usr/bin/env python
"""
Simple script to run the BigQuery MCP server directly.
"""

import os
import sys
from dotenv import load_dotenv
import mcp_server_bigquery

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    print("Starting BigQuery MCP server...")
    # Call the main function directly without asyncio.run
    # since the main function will handle its own asyncio setup
    mcp_server_bigquery.main()
