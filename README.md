# Metasploit MCP Server

A Model Context Protocol (MCP) server for interacting with the Metasploit Framework through Python. This server provides a standardized interface for AI models to interact with Metasploit's functionality.

## Features

- Module Management
  - List available modules
  - Get detailed module information
  - Search for modules
- Module Execution
  - Execute modules with custom options
  - Get and set module options
- Session Management
  - List active sessions
  - Get session information
  - Read/write to sessions
  - Execute commands in sessions

## Prerequisites

- Python 3.12 or higher
- Metasploit Framework with MSFRPC enabled
- MCP client library
- uv (Python package installer)

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file with the following settings:

```env
MSF_RPC_USERNAME=your_username
MSF_RPC_PASSWORD=your_password
MSF_RPC_HOST=127.0.0.1
MSF_RPC_PORT=55553
MSF_RPC_SSL=false
```

## Usage

1. Start the Metasploit RPC server:
   ```bash
   msfrpcd -P your_password -S -a 127.0.0.1
   ```

2. Run the MCP server (this is also how your MCP client can run this server):
   ```bash
   uv --directory <path you cloned to> run python main.py --role viewer
   ```

## Available Tools

### Module Management
- `list_modules`: List available Metasploit modules
- `module_info`: Get detailed information about a specific module
- `search_modules`: Search for modules matching a query

### Module Execution
- `execute_module`: Execute a module with specified options
- `get_options`: Get available options for a module
- `set_option`: Set an option for a module

### Session Management
- `list_sessions`: List all active sessions
- `session_info`: Get detailed information about a session
- `session_write`: Write data to a session
- `session_read`: Read data from a session
- `run_command`: Execute a command in a session

## License

MIT License
