# tools/database.py
from typing import Dict, List, Optional
from pymetasploit3.msfrpc import MsfRpcError
from mcp.server.fastmcp import Context
from utils.msf_utils import get_client, ensure_connected

@ensure_connected
async def list_workspaces(ctx: Context) -> Dict:
    """List all Metasploit workspaces."""
    client = get_client()
    try:
        workspaces = client.db.workspaces.list
        return {"workspaces": workspaces}
    except MsfRpcError as e:
        return {"error": str(e)}

@ensure_connected
async def create_workspace(ctx: Context, name: str) -> Dict:
    """Create a new Metasploit workspace."""
    client = get_client()
    try:
        client.db.workspaces.add(name)
        return {"success": True, "message": f"Workspace {name} created"}
    except MsfRpcError as e:
        return {"error": str(e)}

@ensure_connected
async def delete_workspace(ctx: Context, name: str) -> Dict:
    """Delete a specific Metasploit workspace."""
    client = get_client()
    try:
        client.db.workspaces.remove(name)
        return {"success": True, "message": f"Workspace {name} deleted"}
    except MsfRpcError as e:
        return {"error": str(e)}

@ensure_connected
async def current_workspace(ctx: Context, name: Optional[str] = None) -> Dict:
    """Get or set the current Metasploit workspace."""
    client = get_client()
    try:
        if name:
            client.db.workspaces.set(name)
            return {"success": True, "message": f"Switched to workspace {name}"}
        else:
            return {"workspace": client.db.workspace}
    except MsfRpcError as e:
        return {"error": str(e)}

@ensure_connected
async def list_hosts(ctx: Context, workspace: Optional[str] = None) -> Dict:
    """List hosts in the current or specified workspace."""
    client = get_client()
    try:
        if workspace:
            ws = client.db.workspaces.workspace(workspace)
        else:
            ws = client.db.workspaces.workspace()
        return {"hosts": ws.hosts.list}
    except MsfRpcError as e:
        return {"error": str(e)}

@ensure_connected
async def list_services(
    ctx: Context, 
    workspace: Optional[str] = None, 
    addresses: Optional[List[str]] = None, 
    ports: Optional[List[int]] = None, 
    protocol: Optional[str] = None
) -> Dict:
    """List services in the current or specified workspace."""
    client = get_client()
    try:
        if workspace:
            ws = client.db.workspaces.workspace(workspace)
        else:
            ws = client.db.workspaces.workspace()
        
        # Build search criteria
        criteria = {}
        if addresses:
            criteria['addresses'] = addresses
        if ports:
            criteria['ports'] = ','.join(map(str, ports))
        if protocol:
            criteria['proto'] = protocol
            
        return {"services": ws.services.find(**criteria)}
    except MsfRpcError as e:
        return {"error": str(e)}

@ensure_connected
async def list_vulns(
    ctx: Context, 
    workspace: Optional[str] = None, 
    addresses: Optional[List[str]] = None
) -> Dict:
    """List vulnerabilities in the current or specified workspace."""
    client = get_client()
    try:
        if workspace:
            ws = client.db.workspaces.workspace(workspace)
        else:
            ws = client.db.workspaces.workspace()
            
        criteria = {}
        if addresses:
            criteria['addresses'] = addresses
            
        return {"vulns": ws.vulns.find(**criteria)}
    except MsfRpcError as e:
        return {"error": str(e)}

@ensure_connected
async def import_scan(
    ctx: Context, 
    data: str,
    workspace: Optional[str] = None
) -> Dict:
    """Import scan results into the database."""
    client = get_client()
    try:
        if workspace:
            ws = client.db.workspaces.workspace(workspace)
        else:
            ws = client.db.workspaces.workspace()
            
        ws.importdata(data)
        return {"success": True, "message": "Data imported successfully"}
    except MsfRpcError as e:
        return {"error": str(e)} 