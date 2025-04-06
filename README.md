# MCP Generator

A web application that generates Model Context Protocol (MCP) servers from OpenAPI specifications.

## Description

This project provides a FastAPI-based Generator Server that accepts an OpenAPI v2 (Swagger) or OpenAPI v3 specification and generates a Python MCP server. The generated MCP server exposes MCP functions corresponding to the API operations defined in the input specification, making actual HTTP requests to the target API when these functions are called.

## Features

- Accepts OpenAPI specifications via URL or direct content
- Supports both OpenAPI v2 and v3 formats
- Generates a fully functional Python MCP server
- Maps OpenAPI paths to MCP functions
- Handles path, query, and header parameters
- Supports request bodies and response schemas
- Maps HTTP error codes to MCP error codes

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Generator Server

```bash
python run.py
```

The server will start at `http://localhost:8000`.

### Generating an MCP Server

Send a POST request to the `/generate` endpoint with the following payload:

```json
{
  "source": "url",
  "value": "https://example.com/api-spec.yaml",
  "server_name": "my_mcp_server"
}
```

Or with direct content:

```json
{
  "source": "content",
  "value": "openapi: 3.0.0\ninfo:\n  title: Example API\n  version: 1.0.0\n...",
  "server_name": "my_mcp_server"
}
```

The server will respond with a ZIP file containing the generated MCP server code.

### Running the Generated MCP Server

1. Unzip the generated code
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the target API URL if needed:

```bash
export TARGET_API_BASE_URL="https://api.example.com"
```

4. Run the MCP server:

```bash
python main.py
```

The MCP server will start at `http://localhost:8888` and can be used by MCP clients.

## API Reference

### POST /generate

Generates an MCP server from an OpenAPI specification.

**Request Body:**

- `source`: Either "url" or "content"
- `value`: The URL of the OpenAPI spec or the spec content itself
- `server_name` (optional): Name for the generated server (defaults to "generated_mcp_server")

**Responses:**

- 200: ZIP file containing the generated MCP server code
- 400: Invalid request or OpenAPI specification
- 500: Internal server error

## License

MIT 