# tools/console.py
from typing import Dict, Optional
from pymetasploit3.msfrpc import MsfRpcError
from mcp.server.fastmcp import Context
from utils.msf_utils import get_client, ensure_connected


@ensure_connected
async def create_console(ctx: Context) -> Dict:
    """Create a new Metasploit console."""
    await ctx.debug("Creating new console")
    client = get_client()
    try:
        console_id = client.consoles.console().cid
        await ctx.debug(f"Created console with ID: {console_id}")
        return {"success": True, "console_id": console_id, "message": f"Console {console_id} created"}
    except MsfRpcError as e:
        await ctx.error(f"Failed to create console: {str(e)}")
        return {"error": str(e)}

@ensure_connected
async def destroy_console(ctx: Context, console_id: str) -> Dict:
    """Destroy a specific Metasploit console."""
    await ctx.debug(f"Destroying console with ID: {console_id}")
    client = get_client()
    try:
        result = client.consoles.destroy(console_id)
        await ctx.debug(f"Successfully destroyed console {console_id}")
        return {"success": True, "message": f"Console {console_id} destroyed"}
    except MsfRpcError as e:
        await ctx.error(f"Failed to destroy console {console_id}: {str(e)}")
        return {"error": str(e)}

@ensure_connected
async def list_consoles(ctx: Context) -> Dict:
    """List all active Metasploit consoles."""
    await ctx.debug("Listing all consoles")
    client = get_client()
    try:
        consoles = client.consoles.list
        await ctx.debug(f"Found {len(consoles)} active consoles")
        return {"consoles": consoles}
    except MsfRpcError as e:
        await ctx.error(f"Failed to list consoles: {str(e)}")
        return {"error": str(e)}

@ensure_connected
async def console_write(ctx: Context, console_id: str, command: str) -> Dict:
    """Write a command to a specific Metasploit console."""
    await ctx.debug(f"Writing command to console {console_id}: {command}")
    client = get_client()
    try:
        console = client.consoles.console(console_id)
        console.write(command)
        await ctx.debug(f"Successfully wrote command to console {console_id}")
        return {"success": True, "message": f"Command sent to console {console_id}"}
    except MsfRpcError as e:
        await ctx.error(f"Failed to write to console {console_id}: {str(e)}")
        return {"error": str(e)}

@ensure_connected
async def console_read(ctx: Context, console_id: str) -> Dict:
    """Read output from a specific Metasploit console."""
    await ctx.debug(f"Reading output from console {console_id}")
    client = get_client()
    try:
        console = client.consoles.console(console_id)
        data = console.read()
        await ctx.debug(f"Read data from console {console_id}: busy={data['busy']}")
        return {
            "data": data['data'],
            "busy": data['busy'],
            "prompt": data.get('prompt', '')
        }
    except MsfRpcError as e:
        await ctx.error(f"Failed to read from console {console_id}: {str(e)}")
        return {"error": str(e)}

@ensure_connected
async def run_console_command(ctx: Context, console_id: str, command: str, timeout: Optional[int] = 30) -> Dict:
    """Run a command in a console and get the output."""
    await ctx.debug(f"Running command in console {console_id} with timeout {timeout}s: {command}")
    client = get_client()
    try:
        console = client.consoles.console(console_id)
        console.write(command)
        
        # Wait for command to complete
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            data = console.read()
            if not data['busy']:
                await ctx.debug(f"Command completed successfully in console {console_id}")
                return {
                    "success": True,
                    "data": data['data'],
                    "prompt": data.get('prompt', '')
                }
            time.sleep(1)
        
        await ctx.warning(f"Command timed out after {timeout} seconds in console {console_id}")
        return {
            "success": False,
            "error": f"Command timed out after {timeout} seconds",
            "partial_data": data['data']
        }
    except MsfRpcError as e:
        await ctx.error(f"Failed to run command in console {console_id}: {str(e)}")
        return {"error": str(e)} 