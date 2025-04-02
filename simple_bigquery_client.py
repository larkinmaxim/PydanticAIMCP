#!/usr/bin/env python
"""
Simple BigQuery client that connects directly to BigQuery without using the MCP framework.
"""

import os
import json
from dotenv import load_dotenv
from google.cloud import bigquery

# Load environment variables from .env file
load_dotenv()


def main():
    """Main entry point for the script."""
    print("Connecting to BigQuery...")

    # Get configuration from environment variables
    project = os.getenv("BIGQUERY_PROJECT")
    location = os.getenv("BIGQUERY_LOCATION")
    credentials_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not project:
        print("Error: BIGQUERY_PROJECT environment variable is not set.")
        return

    if not location:
        print("Error: BIGQUERY_LOCATION environment variable is not set.")
        return

    if not credentials_file:
        print("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
        return

    print(f"Using project: {project}")
    print(f"Using location: {location}")
    print(f"Using credentials file: {credentials_file}")

    try:
        # Initialize BigQuery client
        client = bigquery.Client(project=project, location=location)
        print("Connected to BigQuery!")

        # List datasets
        print("\nListing datasets...")
        datasets = list(client.list_datasets())

        if not datasets:
            print("No datasets found in project.")
        else:
            print(f"Found {len(datasets)} datasets:")
            for dataset in datasets:
                print(f"- {dataset.dataset_id}")

        # Execute a simple query
        print("\nExecuting a simple query...")
        query = "SELECT 1 as test"
        query_job = client.query(query)
        results = query_job.result()

        # Print results
        print("Query results:")
        for row in results:
            print(row)

        print("\nTest completed successfully!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
