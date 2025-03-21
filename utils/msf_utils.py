# utils/msf_utils.py
import os
import functools
from typing import Callable, Dict, Any, TypeVar, Optional
from pymetasploit3.msfrpc import MsfRpcClient, MsfRpcError
from mcp.server.fastmcp import Context

# Global client instance
_msf_client = None

# Type variable for ensure_connected decorator
T = TypeVar('T')

def get_client() -> MsfRpcClient:
    """Get the shared MSF client instance."""
    global _msf_client
    if _msf_client is None:
        _msf_client = connect()
    return _msf_client

def connect(
    host: str = None, 
    port: int = None, 
    username: str = None, 
    password: str = None, 
    ssl: bool = None
) -> MsfRpcClient:
    """Connect to MSF RPC server using environment variables or provided parameters."""
    global _msf_client
    
    # Use provided parameters or fall back to environment variables
    host = host or os.environ.get('MSF_RPC_HOST', '127.0.0.1')
    port = port or int(os.environ.get('MSF_RPC_PORT', '55553'))
    username = username or os.environ.get('MSF_RPC_USERNAME', 'msf')
    password = password or os.environ.get('MSF_RPC_PASSWORD', 'msf')
    ssl = ssl if ssl is not None else os.environ.get('MSF_RPC_SSL', 'false').lower() == 'true'
    
    _msf_client = MsfRpcClient(
        password,
        username=username,
        server=host,
        port=port,
        ssl=ssl
    )
    return _msf_client

def disconnect() -> None:
    """Disconnect from MSF RPC server."""
    global _msf_client
    if _msf_client:
        # No explicit disconnect method in MsfRpcClient, so we just delete the reference
        _msf_client = None

def reconnect() -> MsfRpcClient:
    """Reconnect to MSF RPC server."""
    disconnect()
    return connect()

def ensure_connected(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to ensure the MSF client is connected before calling the function."""
    @functools.wraps(func)
    async def wrapper(ctx: Context, *args, **kwargs) -> T:
        try:
            # Try to access the client to check if it's connected
            client = get_client()
            client.auth.token  # Will fail if not authenticated
            return await func(ctx, *args, **kwargs)
        except (AttributeError, MsfRpcError):
            # If not connected or token expired, try to reconnect
            try:
                reconnect()
                return await func(ctx, *args, **kwargs)
            except MsfRpcError as e:
                return {"error": f"Failed to connect to Metasploit RPC server: {str(e)}"}
    return wrapper

# In mcp_server.py, use the helper:
# msf_client = msf_utils.get_msf_client() # No longer initialize at the top level. Initialize within tools.