"""
Logfire Hello World Example

This script demonstrates how to use the logfire library for logging.
Before running this script, you need to:
1. Install logfire (it should be included with pydantic-ai[logfire])
2. Get a logfire write token from https://logfire.ai/
3. Replace the placeholder token below with your actual token
"""

import logfire
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get logfire token from environment variable or use placeholder
# You can add LOGFIRE_TOKEN=your_token to your .env file
logfire_token = os.getenv("LOGFIRE_TOKEN", "__YOUR_LOGFIRE_WRITE_TOKEN__")

# Configure logfire with your token
logfire.configure(token=logfire_token)

# Log a simple message
logfire.info("Hello, {place}!", place="World")

# Log a message with additional context
logfire.info(
    "This is a more detailed log message",
    user_id=123,
    action="example",
    status="success",
)

print("Log messages sent to logfire. Check your logfire dashboard to see them.")
print(
    "If you see any errors, make sure you've replaced the placeholder token with your actual logfire token."
)
