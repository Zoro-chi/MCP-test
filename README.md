# MCP Weather Service

A weather alert service built with Model Context Protocol (MCP) that provides information about active weather alerts across the United States.

## Project Overview

This project demonstrates how to create a simple MCP server that can be used by AI assistants to retrieve real-time weather alert information. It uses the National Weather Service (NWS) API to fetch current weather alerts for any US state.

## Features

- Get active weather alerts for any US state using a simple two-letter state code (e.g., "CA", "TX")
- Format alerts with key information (event type, area, severity, description, and instructions)
- Expose weather data through the Model Context Protocol (MCP)
- Include multiple client implementations (chat-based and programmatic)
- Docker support for containerization

## Prerequisites

- Python 3.11+ (required by MCP)
- UV package manager (`pip install uv`)
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Zoro-chi/MCP-test.git
cd MCP-test
```

2. Create and activate a Python virtual environment using UV:
```bash
uv venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

## Configuration

1. Create a `.env` file in the root directory with your Groq API key:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

### Starting the MCP Server

You have two options to run the weather server:

#### Option 1: Directly using UV

```bash
uv run mcp serve server/weather.py
```

#### Option 2: Using the alternative server implementation

```bash
cd mcpserver
uv run server.py
```

The server will start on the default port (8000).

### Running the Clients

You have multiple client options:

#### Interactive Chat Client

In a separate terminal, activate the virtual environment and run the chat client:

```bash
source .venv/bin/activate
uv run server/client.py
```

This will start an interactive chat using the Groq LLM where you can ask about weather alerts. For example:
- "What are the current weather alerts in California?"
- "Are there any severe weather warnings in Texas?"

#### Programmatic Clients

There are two programmatic client examples in the `mcpserver` directory:

1. SSE Client (Server-Sent Events):
```bash
cd mcpserver
uv run client-sse.py
```

2. STDIO Client:
```bash
cd mcpserver
uv run client-stdio.py
```

### Direct API Calls

You can also make direct calls to the MCP server:

```bash
curl -X POST http://localhost:8000/tools \
  -H "Content-Type: application/json" \
  -d '{"name":"get_alerts","parameters":{"state":"CA"}}'
```

## Docker Deployment

This project includes Docker support for easy deployment:

```bash
cd mcpserver
docker build -t mcp-weather .
docker run -p 8000:8000 mcp-weather
```

This will build and start the server in a container, mapping port 8000 to your host.

## Debugging

If you need to debug the application, check the `data_log.txt` file that gets created when running the server. It contains the raw data received from the NWS API.

Additionally, the server has DEBUG level logging enabled to help diagnose issues.

## Project Structure

- `server/weather.py`: Main MCP server implementation with weather alert functionality
- `server/weather.json`: Configuration file for the MCP server
- `server/client.py`: Interactive chat client that uses the MCP server with Groq LLM
- `mcpserver/server.py`: Alternative server implementation with additional forecast feature
- `mcpserver/client-sse.py`: Example client using Server-Sent Events transport
- `mcpserver/client-stdio.py`: Example client using stdin/stdout transport
- `mcpserver/Dockerfile`: Docker configuration for containerized deployment
- `mcpserver/requirements.txt`: Package requirements for the alternative server

## License

[Your License Information]

## Acknowledgements

- [National Weather Service API](https://www.weather.gov/documentation/services-web-api)
- [MCP (Model Context Protocol)](https://github.com/anthropics/anthropic-model-context-protocol)
- [Groq API](https://console.groq.com/docs/quickstart)