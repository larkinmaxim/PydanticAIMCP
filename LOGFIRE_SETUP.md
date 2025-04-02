# Logfire Integration for MCP Server

This document explains how to set up and use logfire with the MCP server.

## What is Logfire?

[Logfire](https://logfire.ai/) is a structured logging service that helps you collect, analyze, and monitor logs from your applications. It provides a simple API for sending structured logs and a web interface for viewing and analyzing them.

## Setup Instructions

### 1. Get a Logfire Token

1. Sign up for an account at [logfire.ai](https://logfire.ai/)
2. Create a new project or use an existing one
3. Navigate to the API tokens section
4. Create a new write token
5. Copy the token

### 2. Configure the MCP Server

1. Add the token to your `.env` file:
   ```
   LOGFIRE_TOKEN=your_token_here
   ```
   Replace `your_token_here` with the token you copied from logfire.ai.

2. The MCP server is already configured to use this token. The relevant code in `mcp_server.py` is:
   ```python
   # Load environment variables from .env file
   load_dotenv()

   # Initialize logfire
   logfire_token = os.getenv("LOGFIRE_TOKEN")
   if logfire_token:
       logfire.configure(token=logfire_token)
       logfire.info("Logfire initialized with token")
   else:
       logfire.configure()
       logfire.warning("Logfire initialized without token. Logs may not be sent to logfire.ai")
   ```

### 3. Test the Integration

Run the test script to verify that logfire is working correctly:

```bash
python test_logfire.py
```

You should see output indicating that the token was found and that log messages were sent.

## Using Logfire in Your Code

Logfire provides several logging methods that correspond to different log levels:

- `logfire.debug()`: Debug-level messages
- `logfire.info()`: Informational messages
- `logfire.warning()`: Warning messages
- `logfire.error()`: Error messages
- `logfire.critical()`: Critical error messages
- `logfire.exception()`: Exception messages (includes stack trace)

Each method accepts a message string and optional key-value pairs for structured data:

```python
logfire.info("User logged in", user_id=123, ip_address="192.168.1.1")
```

### Using Context

Logfire allows you to group related logs using contexts:

```python
with logfire.Context(request_id="abc123", user_id=456):
    # All logs in this block will include the request_id and user_id
    logfire.info("Processing request")
    
    # You can nest contexts
    with logfire.Context(operation="validate"):
        logfire.info("Validating input")
```

## Viewing Logs

To view your logs:

1. Go to the project URL: [https://logfire-us.pydantic.dev/larkinmaxim/bigquery-mcp](https://logfire-us.pydantic.dev/larkinmaxim/bigquery-mcp)
2. Log in to your account
3. Navigate to the logs dashboard
4. Use the search and filter options to find specific logs

## Additional Resources

- [Logfire Documentation](https://docs.logfire.ai/)
- [Python SDK Reference](https://docs.logfire.ai/sdk/python)
