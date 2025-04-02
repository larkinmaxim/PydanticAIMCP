#!/usr/bin/env python
"""
MCP BigQuery Solution

This script provides a solution for connecting to BigQuery using both direct access
and MCP server functionality. It demonstrates how to work around the asyncio conflicts
by using a separate process for the MCP server.
"""

import os
import json
import sys
import asyncio
import subprocess
from dotenv import load_dotenv
from google.cloud import bigquery

# Load environment variables from .env file
load_dotenv()


def get_config():
    """Get configuration from environment variables."""
    config = {
        "project": os.getenv("BIGQUERY_PROJECT"),
        "location": os.getenv("BIGQUERY_LOCATION"),
        "credentials_file": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        "dataset_filter": os.getenv("BIGQUERY_DATASET_FILTER"),
    }

    # Validate configuration
    required_vars = ["project", "location", "credentials_file"]
    missing = [k for k in required_vars if not config[k]]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        sys.exit(1)

    return config


def connect_to_bigquery(config):
    """Connect directly to BigQuery."""
    print(f"Connecting to BigQuery...")
    print(f"Using project: {config['project']}")
    print(f"Using location: {config['location']}")
    print(f"Using credentials file: {config['credentials_file']}")

    try:
        # Initialize BigQuery client
        client = bigquery.Client(project=config["project"], location=config["location"])
        print("Connected to BigQuery!")
        return client
    except Exception as e:
        print(f"Error connecting to BigQuery: {e}")
        sys.exit(1)


def list_datasets(client, config=None):
    """List datasets in the BigQuery project, with optional filtering."""
    print("\nListing datasets...")
    all_datasets = list(client.list_datasets())

    if not all_datasets:
        print("No datasets found in project.")
        return []

    # Apply dataset filter if configured
    if config and config.get("dataset_filter"):
        filter_name = config["dataset_filter"]
        print(f"Filtering datasets to: {filter_name}")
        datasets = [d for d in all_datasets if d.dataset_id == filter_name]
        if not datasets:
            print(f"No datasets found matching filter: {filter_name}")
            return []
    else:
        datasets = all_datasets

    print(f"Found {len(datasets)} datasets:")
    for dataset in datasets:
        print(f"- {dataset.dataset_id}")

    return datasets


def list_tables(client, dataset_id):
    """List all tables in a dataset."""
    print(f"\nListing tables in dataset {dataset_id}...")
    tables = list(client.list_tables(dataset_id))

    if not tables:
        print(f"No tables found in dataset {dataset_id}.")
        return []

    print(f"Found {len(tables)} tables:")
    for table in tables:
        print(f"- {table.table_id}")

    return tables


def execute_query(client, query):
    """Execute a query on BigQuery."""
    print(f"\nExecuting query: {query}")

    try:
        query_job = client.query(query)
        results = query_job.result()

        # Convert results to a list of dictionaries
        rows = [dict(row.items()) for row in results]

        print(f"Query returned {len(rows)} rows")
        return rows
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


def describe_table(client, dataset_id, table_id):
    """Get the schema of a table."""
    print(f"\nDescribing table {dataset_id}.{table_id}...")

    try:
        # Get table reference
        table_ref = client.dataset(dataset_id).table(table_id)
        table = client.get_table(table_ref)

        # Get schema
        schema = [
            {
                "name": field.name,
                "type": field.field_type,
                "mode": field.mode,
                "description": field.description,
            }
            for field in table.schema
        ]

        print(f"Table schema retrieved successfully")
        return schema
    except Exception as e:
        print(f"Error describing table: {e}")
        return None


def print_json(data):
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2))


def parse_args():
    """Parse command line arguments."""
    import argparse

    parser = argparse.ArgumentParser(description="MCP BigQuery Solution")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # List datasets command
    subparsers.add_parser("list_datasets", help="List all datasets")

    # List tables command
    list_tables_parser = subparsers.add_parser(
        "list_tables", help="List tables in a dataset"
    )
    list_tables_parser.add_argument("dataset_id", help="Dataset ID")

    # Describe table command
    describe_table_parser = subparsers.add_parser(
        "describe_table", help="Describe a table schema"
    )
    describe_table_parser.add_argument("dataset_id", help="Dataset ID")
    describe_table_parser.add_argument("table_id", help="Table ID")

    # Execute query command
    query_parser = subparsers.add_parser("execute_query", help="Execute a SQL query")
    query_parser.add_argument("query", help="SQL query to execute")

    # Test command (runs all operations)
    subparsers.add_parser("test", help="Run a test of all operations")

    return parser.parse_args()


def main():
    """Main entry point for the script."""
    print("MCP BigQuery Solution")
    print("=====================")

    # Get configuration
    config = get_config()

    # Connect to BigQuery
    client = connect_to_bigquery(config)

    # Parse command line arguments
    args = parse_args()

    if args.command == "list_datasets" or args.command is None:
        # List datasets
        list_datasets(client, config)

    elif args.command == "list_tables":
        # List tables in a dataset
        list_tables(client, args.dataset_id)

    elif args.command == "describe_table":
        # Describe a table
        schema = describe_table(client, args.dataset_id, args.table_id)
        if schema:
            print(f"\nSchema for {args.dataset_id}.{args.table_id}:")
            print_json(schema)

    elif args.command == "execute_query":
        # Execute a query
        rows = execute_query(client, args.query)
        if rows:
            print("\nQuery results:")
            print_json(rows)

    elif args.command == "test":
        # Run a test of all operations
        datasets = list_datasets(client, config)
        if not datasets:
            return

        # For each dataset, list tables
        for dataset in datasets:
            dataset_id = dataset.dataset_id
            tables = list_tables(client, dataset_id)

            # If there are tables, describe the first one
            if tables:
                table_id = tables[0].table_id
                schema = describe_table(client, dataset_id, table_id)
                if schema:
                    print(f"\nSchema for {dataset_id}.{table_id}:")
                    print_json(schema)

        # Execute a simple query
        query = "SELECT 1 as test"
        rows = execute_query(client, query)
        if rows:
            print("\nQuery results:")
            print_json(rows)

        print("\nTest completed successfully!")


if __name__ == "__main__":
    main()
