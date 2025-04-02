# Plan for Rebuilding BigQuery MCP Server with Pydantic Framework

## Overview

This document outlines the plan to rebuild the BigQuery MCP server using the Pydantic framework. The goal is to leverage Pydantic's data validation capabilities and integrate with the FastMCP server implementation to create a more robust and maintainable BigQuery server.

## Analysis of Current Implementations

### BigQuery MCP Server
- Uses the standard MCP SDK to create a server that provides access to BigQuery
- Implements three tools:
  - `execute-query`: Executes SQL queries on BigQuery
  - `list-tables`: Lists all tables in the BigQuery database
  - `describe-table`: Gets schema information for specific tables
- Uses a `BigQueryDatabase` class to handle interactions with BigQuery
- Takes command-line arguments for configuration (project, location, datasets)
- Uses async/await pattern for all operations

### Pydantic AI MCP Server
- Uses the Pydantic AI framework with FastMCP
- Implements a tool for generating poems using the Anthropic API
- Uses environment variables for configuration
- Has fallback functionality when the API key is not valid
- Uses decorators for defining tools

## Step-by-Step Implementation Plan

### 1. Set up project structure
- Create a new directory for the Pydantic-based BigQuery server
- Set up the basic file structure (similar to the original)
- Create a requirements.txt file with necessary dependencies:
  ```
  google-cloud-bigquery>=3.27.0
  mcp>=1.0.0
  pydantic_ai
  python-dotenv
  ```

### 2. Create Pydantic models
- Define Pydantic models for BigQuery data structures
- Create models for:
  - Query parameters
  - Query results
  - Table information
  - Error responses
- Use Pydantic's validation capabilities for input parameters
- Example model structure:
  ```python
  from pydantic import BaseModel, Field
  from typing import List, Dict, Any, Optional

  class QueryParams(BaseModel):
      query: str = Field(..., description="SQL query to execute")
      params: Optional[Dict[str, Any]] = Field(None, description="Query parameters")

  class TableInfo(BaseModel):
      dataset_id: str
      table_id: str
      full_name: str = Field(..., description="Full table name in format dataset.table")
  ```

### 3. Implement BigQuery database class
- Port the existing `BigQueryDatabase` class to use Pydantic models
- Ensure all methods are async and properly typed
- Add error handling with Pydantic validation
- Implement connection pooling and retry logic
- Example implementation structure:
  ```python
  class BigQueryDatabase:
      def __init__(self, project: str, location: str, datasets_filter: List[str]):
          """Initialize a BigQuery database client with validation"""
          # Validate inputs
          # Initialize client
          
      async def execute_query(self, params: QueryParams) -> List[Dict[str, Any]]:
          """Execute a SQL query with proper validation and error handling"""
          # Validate query
          # Execute query
          # Format and return results
          
      async def list_tables(self) -> List[TableInfo]:
          """List all tables with proper typing"""
          # List datasets
          # List tables
          # Return formatted results
  ```

### 4. Create the FastMCP server
- Use the FastMCP class from the Pydantic AI framework
- Set up command-line argument parsing
- Configure environment variable loading
- Example implementation:
  ```python
  from mcp.server.fastmcp import FastMCP
  from dotenv import load_dotenv
  import os

  # Load environment variables
  load_dotenv()

  # Create server
  server = FastMCP("BigQuery Server")
  ```

### 5. Implement tools using decorators
- Port the existing tools to use the FastMCP decorator syntax
- Ensure proper typing and validation using Pydantic
- Implement error handling and fallbacks
- Example implementation:
  ```python
  @server.tool()
  async def execute_query(query: str) -> str:
      """Execute a SQL query on the BigQuery database"""
      try:
          params = QueryParams(query=query)
          results = await db.execute_query(params)
          return str(results)
      except Exception as e:
          return f"Error: {str(e)}"
  ```

### 6. Add configuration and environment handling
- Use dotenv for environment variable loading
- Implement validation for configuration parameters
- Add fallback mechanisms for missing configurations
- Example implementation:
  ```python
  # Configuration validation
  def validate_config():
      project = os.getenv("BIGQUERY_PROJECT")
      location = os.getenv("BIGQUERY_LOCATION")
      
      if not project:
          raise ValueError("BIGQUERY_PROJECT environment variable is required")
      if not location:
          raise ValueError("BIGQUERY_LOCATION environment variable is required")
          
      return project, location
  ```

### 7. Create entry point
- Set up the main function to initialize the server
- Handle command-line arguments
- Configure logging
- Example implementation:
  ```python
  def main():
      """Main entry point for the package."""
      parser = argparse.ArgumentParser(description='BigQuery MCP Server')
      parser.add_argument('--project', help='BigQuery project', required=False)
      parser.add_argument('--location', help='BigQuery location', required=False)
      parser.add_argument('--dataset', help='BigQuery dataset', required=False, action='append')
      
      args = parser.parse_args()
      
      # Use command line args or environment variables
      project = args.project or os.getenv("BIGQUERY_PROJECT")
      location = args.location or os.getenv("BIGQUERY_LOCATION")
      datasets_filter = args.dataset if args.dataset else []
      
      # Initialize and run server
      server.run()
  ```

### 8. Add testing and documentation
- Create tests for the server functionality
- Document the API and usage
- Add examples
- Testing structure:
  ```
  tests/
  ├── test_database.py
  ├── test_models.py
  ├── test_server.py
  └── test_tools.py
  ```

## Benefits of Using Pydantic

1. **Strong typing and validation**: Pydantic provides runtime validation of data, ensuring that inputs and outputs conform to expected types and formats.

2. **Self-documenting code**: Pydantic models serve as documentation for the data structures used in the application.

3. **Error handling**: Pydantic provides clear error messages when validation fails, making it easier to debug issues.

4. **Integration with FastAPI**: Pydantic models can be used directly with FastAPI for API documentation and validation.

5. **Serialization and deserialization**: Pydantic handles conversion between Python objects and JSON/dict representations.

## Implementation Timeline

1. **Day 1**: Set up project structure, create Pydantic models
2. **Day 2**: Implement BigQuery database class, create FastMCP server
3. **Day 3**: Implement tools, add configuration handling
4. **Day 4**: Create entry point, add testing and documentation
5. **Day 5**: Review, refine, and finalize

## Conclusion

By rebuilding the BigQuery MCP server with the Pydantic framework, we'll create a more robust, maintainable, and type-safe implementation. The use of Pydantic models will provide better validation and error handling, making the server more reliable and easier to use.
