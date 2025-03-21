# tools/execute.py
from typing import Dict, Any, Optional
from mcp.server.fastmcp import Context
from utils.msf_utils import get_client, ensure_connected

@ensure_connected
async def execute_module(ctx: Context, module_type: str, module_name: str, options: Optional[Dict[str, Any]] = None) -> Dict:
    """Execute a Metasploit module with the given options.
    
    Args:
        ctx: The context object.
        module_type: Type of the module (exploit, auxiliary, post, etc.).
        module_name: Name of the module.
        options: Module options as key-value pairs.
    
    Returns:
        A dictionary containing the execution result.
    """
    client = get_client()
    module = client.modules.use(module_type, module_name)
    
    if options:
        for key, value in options.items():
            module[key] = value
    
    result = module.execute()
    return {
        "job_id": result.get("job_id"),
        "uuid": result.get("uuid"),
        "status": "success" if result else "failed"
    }

@ensure_connected
async def get_options(ctx: Context, module_type: str, module_name: str) -> Dict:
    """Get the available options for a module.
    
    Args:
        ctx: The context object.
        module_type: Type of the module (exploit, auxiliary, post, etc.).
        module_name: Name of the module.
    
    Returns:
        A dictionary of module options.
    """
    client = get_client()
    module = client.modules.use(module_type, module_name)
    return module.options

@ensure_connected
async def set_option(ctx: Context, module_type: str, module_name: str, option_name: str, option_value: str) -> Dict:
    """Set an option for a specific module.
    
    Args:
        ctx: The context object.
        module_type: Type of the module (exploit, auxiliary, post, etc.).
        module_name: Name of the module.
        option_name: Name of the option to set.
        option_value: Value to set for the option.
    
    Returns:
        A dictionary indicating success.
    """
    client = get_client()
    module = client.modules.use(module_type, module_name)
    module[option_name] = option_value
    return {"status": "success", "message": f"Option {option_name} set to {option_value}"}