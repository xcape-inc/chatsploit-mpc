# tools/modules.py
from typing import Dict, List, Optional
from pymetasploit3.msfrpc import MsfRpcError
from mcp.server.fastmcp import Context
from utils.msf_utils import get_client, ensure_connected

@ensure_connected
async def list_modules(ctx: Context, type: Optional[str] = None) -> List[str]:
    """List available Metasploit modules, optionally filtered by type.
    
    Args:
        ctx: The context object.
        type: Module type (exploit, auxiliary, post, payload, encoder, nop).
    
    Returns:
        A list of module names.
    """
    client = get_client()
    if type:
        if type == 'exploit':
            return client.modules.exploits
        elif type == 'auxiliary':
            return client.modules.auxiliary
        elif type == 'post':
            return client.modules.post
        elif type == 'payload':
            return client.modules.payloads
        elif type == 'encoder':
            return client.modules.encoders
        elif type == 'nop':
            return client.modules.nops
        else:
            raise ValueError(f"Invalid module type: {type}")
    
    # If no type specified, return all modules
    modules = []
    modules.extend(client.modules.exploits)
    modules.extend(client.modules.auxiliary)
    modules.extend(client.modules.post)
    modules.extend(client.modules.payloads)
    modules.extend(client.modules.encoders)
    modules.extend(client.modules.nops)
    return modules

@ensure_connected
async def module_info(ctx: Context, module_type: str, module_name: str) -> Dict:
    """Get detailed information about a specific Metasploit module.
    
    Args:
        ctx: The context object.
        module_type: Type of the module (exploit, auxiliary, post, etc.).
        module_name: Name of the module.
    
    Returns:
        A dictionary containing module information.
    """
    client = get_client()
    module = client.modules.use(module_type, module_name)
    return {
        "name": module.modulename,
        "type": module.moduletype,
        "description": module.description,
        "options": module.options,
        "references": module.references,
        "targets": module.targets if hasattr(module, "targets") else None,
        "payloads": module.payloads if hasattr(module, "payloads") else None
    }

@ensure_connected
async def search_modules(ctx: Context, query: str) -> List[Dict]:
    """Search for Metasploit modules.
    
    Args:
        ctx: The context object.
        query: Search query string.
    
    Returns:
        A list of matching modules.
    """
    client = get_client()
    modules = client.modules.search(query)
    return modules