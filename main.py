# main.py
"""
Main entry point for the Metasploit MCP server.
This file runs the MCP server defined in mcp_server.py.
"""
from mcp.server.fastmcp import FastMCP
from mcp_server import mcp  # Import the mcp instance
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Configure logging
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = os.path.join(log_directory, f"mcp_{timestamp}.log")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

def main():
    """Run the MCP server."""
    # logger.info("Starting Metasploit MCP server...")
    import asyncio
    
    asyncio.run(mcp.run(transport='stdio'))

if __name__ == "__main__":
    # Run the MCP server
    main()