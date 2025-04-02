# MCP BigQuery Solution

This solution provides a workaround for the asyncio conflicts encountered when trying to use the BigQuery MCP server. Instead of using the MCP framework, it directly connects to BigQuery using the Google Cloud BigQuery client library.

## Background

When trying to run the BigQuery MCP server, we encountered several issues:

1. Asyncio conflicts between the MCP framework and the BigQuery client
2. Issues with the event loop
3. Process termination errors

These issues are documented in detail in the `mcp_bigquery_troubleshooting.md` file.

## Solution

The solution is to use a direct connection to BigQuery instead of going through the MCP framework. The `mcp_bigquery_solution.py` script provides a command-line interface that mimics the functionality of the MCP server, allowing you to:

- List datasets
- List tables in a dataset
- Describe a table schema
- Execute SQL queries

## Prerequisites

1. Python 3.12 or higher
2. Google Cloud BigQuery client library
3. Environment variables set up in a `.env` file:
   - `BIGQUERY_PROJECT`: The Google Cloud project ID
   - `BIGQUERY_LOCATION`: The BigQuery location (e.g., "europe-west3")
   - `GOOGLE_APPLICATION_CREDENTIALS`: Path to the service account key file
   - `BIGQUERY_DATASET_FILTER`: (Optional) Filter to a specific dataset (e.g., "TP_projects")

## Usage

```bash
# List all datasets
python mcp_bigquery_solution.py list_datasets

# List tables in a dataset
python mcp_bigquery_solution.py list_tables DATASET_ID

# Describe a table schema
python mcp_bigquery_solution.py describe_table DATASET_ID TABLE_ID

# Execute a SQL query
python mcp_bigquery_solution.py execute_query "SELECT * FROM DATASET_ID.TABLE_ID LIMIT 10"

# Run a test of all operations
python mcp_bigquery_solution.py test
```

## Troubleshooting

### Dataset Location Issues

If you encounter a "404 Not found" error when trying to execute a query, it might be because the dataset is in a different location than what's specified in the environment variables. Make sure the `BIGQUERY_LOCATION` environment variable is set to the correct location for your datasets.

### Authentication Issues

If you encounter authentication issues, make sure the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set to the correct path of your service account key file.

## Future Improvements

1. Add support for more BigQuery operations
2. Implement a REST API to provide a more MCP-like interface
3. Add support for authentication through other methods (e.g., user credentials)
4. Improve error handling and reporting
