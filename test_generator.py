#!/usr/bin/env python
"""
Test script for the MCP Generator.

This script sends a test OpenAPI specification to the MCP Generator server
and saves the generated MCP server code.
"""
import os
import requests
import json

# Configuration
GENERATOR_URL = "http://localhost:8000/generate"
API_SPEC_PATH = "sample_spec.yaml"
OUTPUT_ZIP_PATH = "generated_mcp_server.zip"

def main():
    """Test the MCP Generator with a sample API spec."""
    print(f"Reading API spec from {API_SPEC_PATH}...")
    with open(API_SPEC_PATH, "r") as f:
        spec_content = f.read()
    
    print(f"Sending request to {GENERATOR_URL}...")
    response = requests.post(
        GENERATOR_URL,
        json={
            "source": "content",
            "value": spec_content,
            "server_name": "sample_mcp_server"
        }
    )
    
    if response.status_code == 200:
        print(f"Success! Saving generated code to {OUTPUT_ZIP_PATH}...")
        with open(OUTPUT_ZIP_PATH, "wb") as f:
            f.write(response.content)
        print("Done!")
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Response text: {response.text}")

if __name__ == "__main__":
    main() 