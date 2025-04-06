import os
import json
import uuid
import shutil
import yaml
import asyncio
from zipfile import ZipFile
from typing import Optional, Literal, Union, Dict, Any, List
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, HttpUrl
from openapi_spec_validator import validate_spec
from jinja2 import Environment, FileSystemLoader

app = FastAPI(
    title="MCP Server Generator",
    description="Generates Python MCP Server code from OpenAPI specifications",
    version="1.0.0"
)

class GenerateRequest(BaseModel):
    source: Literal["url", "content"]
    value: Union[HttpUrl, str, Dict[str, Any]]  # URL, YAML/JSON string, or parsed dict
    server_name: Optional[str] = Field("generated_mcp_server", 
                                       description="Name for the generated server directory/package")
    skip_validation: Optional[bool] = Field(False, 
                                          description="Skip OpenAPI validation (use for specs with validation issues)")

class ErrorResponse(BaseModel):
    detail: str

@app.post("/generate", 
          response_class=FileResponse,
          responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def generate_mcp_server(request: GenerateRequest, background_tasks: BackgroundTasks):
    """
    Generate a Python MCP server from an OpenAPI specification.
    
    - source: Whether the spec is provided as a 'url' or direct 'content'
    - value: The URL to fetch the spec from, or the spec content itself
    - server_name: Name for the generated server (defaults to "generated_mcp_server")
    - skip_validation: Skip OpenAPI validation (useful for specs with validation issues)
    
    Returns a zip file containing the generated server code.
    """
    # Create unique output directory
    output_dir = Path(f"output_{uuid.uuid4().hex}")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Step 1: Fetch/load the OpenAPI spec
        spec_dict = await load_spec(request.source, request.value)
        
        # Step 2: Validate the spec (if not skipped)
        if not request.skip_validation:
            validate_openapi_spec(spec_dict)
        
        # Step 3: Process the spec into a format suitable for the templates
        processed_functions = process_spec(spec_dict)
        
        # Step 4: Determine the server base URL from the spec
        default_target_url = extract_base_url(spec_dict)
        
        # Step 5: Generate the code using Jinja2 templates
        server_dir = output_dir / request.server_name
        server_dir.mkdir(exist_ok=True)
        
        generate_code(
            server_dir=server_dir,
            context={
                "functions": processed_functions,
                "default_target_url": default_target_url,
                "server_name": request.server_name,
            }
        )
        
        # Step 6: Create a zip file of the generated code
        zip_path = output_dir / f"{request.server_name}.zip"
        with ZipFile(zip_path, 'w') as zipf:
            for file in server_dir.rglob('*'):
                if file.is_file():
                    zipf.write(file, file.relative_to(output_dir))
        
        # Schedule the cleanup of the output directory after the response is sent
        background_tasks.add_task(cleanup_files, output_dir)
        
        return FileResponse(
            path=zip_path,
            filename=f"{request.server_name}.zip",
            media_type="application/zip"
        )
        
    except Exception as e:
        # Cleanup in case of error
        if output_dir.exists():
            shutil.rmtree(output_dir)
        
        if isinstance(e, HTTPException):
            raise e
        
        # Log the error
        print(f"Error generating MCP server: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating MCP server: {str(e)}")

async def load_spec(source: str, value: Union[HttpUrl, str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Load the OpenAPI specification from the provided source.
    """
    try:
        if source == "url":
            # Fetch spec from URL
            response = requests.get(str(value))
            response.raise_for_status()
            content = response.text
            
            # Try to parse as JSON first, then YAML
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return yaml.safe_load(content)
        else:  # source == "content"
            # If value is already a dict, return it
            if isinstance(value, dict):
                return value
            
            # If value is a string, try to parse it as JSON or YAML
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return yaml.safe_load(value)
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch specification: {str(e)}")
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse specification: {str(e)}")

def validate_openapi_spec(spec_dict: Dict[str, Any]) -> None:
    """
    Validate the OpenAPI specification.
    """
    try:
        validate_spec(spec_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid OpenAPI specification: {str(e)}")
    
def process_spec(spec_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Process the OpenAPI spec into a format suitable for code generation.
    
    Returns a list of dictionaries, each representing an MCP function.
    """
    processed_functions = []
    
    # Determine if this is OpenAPI v2 or v3
    openapi_version = spec_dict.get("openapi", "2.0")  # Default to 2.0 if not specified
    is_v3 = openapi_version.startswith("3.")
    
    # Process paths
    paths = spec_dict.get("paths", {})
    for path, path_item in paths.items():
        for method, operation in path_item.items():
            if method in ["get", "post", "put", "delete", "patch", "options", "head"]:
                # Skip if this is a parameter at path level, not an operation
                if method == "parameters":
                    continue
                
                # Get operation ID or generate one
                operation_id = operation.get("operationId")
                if not operation_id:
                    # Generate an operation ID based on the method and path
                    path_segments = [s for s in path.split("/") if s and not s.startswith("{")]
                    if path_segments:
                        resource = path_segments[-1]
                    else:
                        resource = "root"
                    operation_id = f"{method}{resource.capitalize()}"
                
                # Extract parameters
                parameters = operation.get("parameters", [])
                
                # Add path-level parameters
                if "parameters" in path_item:
                    parameters.extend(path_item["parameters"])
                
                # Group parameters by type
                path_params = []
                query_params = []
                header_params = []
                
                for param in parameters:
                    # Handle parameter references
                    if "$ref" in param:
                        # Resolve the reference - this would need a more complex implementation
                        # For now, we'll just skip it
                        continue
                    
                    param_in = param.get("in")
                    if param_in == "path":
                        path_params.append(param)
                    elif param_in == "query":
                        query_params.append(param)
                    elif param_in == "header":
                        header_params.append(param)
                
                # Extract request body (OpenAPI v3) or body parameter (v2)
                request_body_schema = None
                if is_v3 and "requestBody" in operation:
                    request_body = operation["requestBody"]
                    content = request_body.get("content", {})
                    for media_type, media_obj in content.items():
                        if "schema" in media_obj:
                            request_body_schema = media_obj["schema"]
                            break
                else:
                    # Try to find a body parameter in v2
                    for param in parameters:
                        if param.get("in") == "body" and "schema" in param:
                            request_body_schema = param["schema"]
                            break
                
                # Extract response schema
                success_response_schema = None
                responses = operation.get("responses", {})
                for status, response in responses.items():
                    if status.startswith("2"):  # 2xx response
                        if is_v3 and "content" in response:
                            content = response.get("content", {})
                            for media_type, media_obj in content.items():
                                if "schema" in media_obj:
                                    success_response_schema = media_obj["schema"]
                                    break
                        elif "schema" in response:  # OpenAPI v2
                            success_response_schema = response["schema"]
                        break
                
                # Extract security requirements
                security_requirements = []
                if "security" in operation:
                    security_requirements = operation["security"]
                elif "security" in spec_dict:
                    security_requirements = spec_dict["security"]
                
                # Prepare input and output schemas as JSON for Jinja templates
                input_schema_json = json.dumps(create_input_schema(
                    path_params, query_params, header_params, request_body_schema
                ))
                
                output_schema_json = json.dumps(success_response_schema or {})
                
                # Create function data object
                function_data = {
                    "mcp_function_name": operation_id,
                    "openapi_operation_id": operation_id,
                    "openapi_path": path,
                    "openapi_method": method,
                    "description": operation.get("summary", "") or operation.get("description", ""),
                    "path_params": path_params,
                    "query_params": query_params,
                    "header_params": header_params,
                    "request_body_schema": request_body_schema,
                    "success_response_schema": success_response_schema,
                    "security_requirements": security_requirements,
                    "input_schema_json": input_schema_json,
                    "output_schema_json": output_schema_json
                }
                
                processed_functions.append(function_data)
    
    return processed_functions

def create_input_schema(path_params, query_params, header_params, request_body_schema):
    """
    Create an input schema for the MCP function based on the OpenAPI parameters.
    """
    properties = {}
    required = []
    
    # Add path parameters
    for param in path_params:
        properties[param["name"]] = param.get("schema", {"type": "string"})
        if param.get("required", True):  # Path parameters are required by default
            required.append(param["name"])
    
    # Add query parameters
    for param in query_params:
        properties[param["name"]] = param.get("schema", {"type": "string"})
        if param.get("required", False):
            required.append(param["name"])
    
    # Add header parameters
    for param in header_params:
        properties[param["name"]] = param.get("schema", {"type": "string"})
        if param.get("required", False):
            required.append(param["name"])
    
    # Add body parameter if present
    if request_body_schema:
        properties["body"] = request_body_schema
        # If the request body is required, add it to the required list
        # The exact logic here would depend on how you want to structure your MCP functions
        
    # Create the schema
    schema = {
        "type": "object",
        "properties": properties
    }
    
    if required:
        schema["required"] = required
    
    return schema

def extract_base_url(spec_dict: Dict[str, Any]) -> str:
    """
    Extract the base URL from the OpenAPI specification.
    """
    # OpenAPI v3
    if "servers" in spec_dict and spec_dict["servers"]:
        for server in spec_dict["servers"]:
            if "url" in server:
                return server["url"]
    
    # OpenAPI v2
    if "host" in spec_dict:
        scheme = "https"
        if "schemes" in spec_dict and spec_dict["schemes"]:
            scheme = spec_dict["schemes"][0]
        
        base_path = spec_dict.get("basePath", "")
        return f"{scheme}://{spec_dict['host']}{base_path}"
    
    # Default
    return "http://replace.me.example.com"

def generate_code(server_dir: Path, context: Dict[str, Any]) -> None:
    """
    Generate the code for the MCP server using Jinja2 templates.
    """
    env = Environment(
        loader=FileSystemLoader("app/templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # Define the templates and their output files
    templates = {
        "main.py.j2": "main.py",
        "handlers.py.j2": "handlers.py",
        "config.py.j2": "config.py",
        "requirements.txt.j2": "requirements.txt",
        "README.md.j2": "README.md",
        "Dockerfile.j2": "Dockerfile",
    }
    
    # Render each template and write to the output directory
    for template_name, output_file in templates.items():
        template = env.get_template(template_name)
        content = template.render(**context)
        
        output_path = server_dir / output_file
        with open(output_path, "w") as f:
            f.write(content)

async def cleanup_files(directory: Path):
    """
    Clean up the output directory after a short delay.
    This gives time for the file to be served to the client.
    """
    await asyncio.sleep(60)  # Wait for 60 seconds before cleaning up
    if directory.exists():
        shutil.rmtree(directory)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 