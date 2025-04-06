"""
Configuration for the launchdarkly_mcp_server MCP server.
"""
import os

# Target API base URL (configurable via environment variable)
TARGET_API_BASE_URL = os.environ.get("TARGET_API_BASE_URL", "https://app.launchdarkly.com")

# Target API authentication settings (if needed)
# Uncomment and modify as needed for the target API
# TARGET_API_KEY = os.environ.get("TARGET_API_KEY")
# TARGET_API_USERNAME = os.environ.get("TARGET_API_USERNAME")
# TARGET_API_PASSWORD = os.environ.get("TARGET_API_PASSWORD")
# TARGET_API_TOKEN = os.environ.get("TARGET_API_TOKEN") 