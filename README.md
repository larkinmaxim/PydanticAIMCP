# MCP BigQuery

This repository contains a Model Context Protocol (MCP) server for BigQuery integration. It allows Claude and other AI assistants to interact with Google BigQuery through the MCP protocol.

## Project Structure

- `mcp-bigquery/`: The main MCP server package
  - `src/mcp_server_bigquery/`: Source code for the MCP server
  - `examples/`: Example configurations and usage
- `run_bigquery_server.py`: Script to run the BigQuery MCP server
- `simple_bigquery_client.py`: Simple client for testing BigQuery integration
- `check_mcp_stdio.py`: Utility to check MCP stdio communication
- `requirements.txt`: Python dependencies

## Getting Started 1

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your Google Cloud credentials and configure the `.env` file with your BigQuery settings.

3. Run the BigQuery MCP server:
   ```
   python run_bigquery_server.py
   ```

4. Configure your AI assistant to use the MCP server.

## Documentation

For more information on how to use this MCP server, see the following files:
- `mcp_bigquery_troubleshooting.md`: Troubleshooting guide
- `LOGFIRE_SETUP.md`: Guide for setting up logging with LogFire
