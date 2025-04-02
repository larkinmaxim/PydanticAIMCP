"""
Test script for logfire integration

This script tests the logfire integration by:
1. Loading environment variables from .env
2. Configuring logfire with the token from the environment
3. Sending a test log message
"""

import os
from dotenv import load_dotenv
import logfire

# Load environment variables from .env file
load_dotenv()

# Get logfire token from environment variable
logfire_token = os.getenv("LOGFIRE_TOKEN")

print(f"Logfire token found: {'Yes' if logfire_token else 'No'}")

# Configure logfire with the token
if logfire_token:
    logfire.configure(token=logfire_token)
    print("Logfire configured with token")
else:
    logfire.configure()
    print("Logfire configured without token (logs may not be sent to logfire.ai)")

# Send a test log message
logfire.info("Test log message from test_logfire.py")
print("Test log message sent")

# Log with structured data
logfire.info(
    "Structured log message", test_id=123, environment="development", status="success"
)
print("Structured log message sent")

print("\nTo see these logs in logfire.ai:")
print("1. Make sure you have a valid LOGFIRE_TOKEN in your .env file")
print("2. Visit https://logfire.ai/ and log in to your account")
print("3. Check your logs dashboard for the test messages")
print("Logfire project URL: https://logfire-us.pydantic.dev/larkinmaxim/bigquery-mcp")
