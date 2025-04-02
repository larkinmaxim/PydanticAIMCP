#!/usr/bin/env python
"""
Check the available classes in the mcp.server.stdio module.
"""

import inspect
import mcp.server.stdio

# Print all available classes and functions in the mcp.server.stdio module
print("Available classes and functions in mcp.server.stdio:")
for name, obj in inspect.getmembers(mcp.server.stdio):
    if not name.startswith("_"):  # Skip private members
        print(f"- {name}: {type(obj)}")

# Try to import the StdioServerTransport class
try:
    from mcp.server import stdio

    print("\nContents of mcp.server.stdio.__dict__:")
    for key, value in stdio.__dict__.items():
        if not key.startswith("_"):
            print(f"- {key}: {type(value)}")
except ImportError as e:
    print(f"Error importing mcp.server.stdio: {e}")
