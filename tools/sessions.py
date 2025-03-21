# tools/sessions.py
from typing import Dict, List, Optional
from pymetasploit3.msfrpc import MsfRpcError
from mcp.server.fastmcp import Context
from utils.msf_utils import get_client, ensure_connected

@ensure_connected
async def list_sessions(ctx: Context) -> Dict:
    """List all active Metasploit sessions."""
    client = get_client()
    return client.sessions.list

@ensure_connected
async def session_shell_read(ctx: Context, session_id: str) -> Dict:
    """Read output from a shell session."""
    client = get_client()
    try:
        session = client.sessions.session(session_id)
        return {"data": session.read()}
    except (KeyError, MsfRpcError) as e:
        return {"error": str(e)}

@ensure_connected
async def session_shell_write(ctx: Context, session_id: str, command: str) -> Dict:
    """Send a command to a shell session."""
    client = get_client()
    try:
        session = client.sessions.session(session_id)
        session.write(command)
        return {"success": True, "message": f"Command sent to session {session_id}"}
    except (KeyError, MsfRpcError) as e:
        return {"error": str(e)}

@ensure_connected
async def session_meterpreter_read(ctx: Context, session_id: str) -> Dict:
    """Read output from a meterpreter session."""
    client = get_client()
    try:
        session = client.sessions.session(session_id)
        return {"data": session.read()}
    except (KeyError, MsfRpcError) as e:
        return {"error": str(e)}

@ensure_connected
async def session_meterpreter_write(ctx: Context, session_id: str, command: str) -> Dict:
    """Send a command to a meterpreter session."""
    client = get_client()
    try:
        session = client.sessions.session(session_id)
        session.write(command)
        return {"success": True, "message": f"Command sent to session {session_id}"}
    except (KeyError, MsfRpcError) as e:
        return {"error": str(e)}

@ensure_connected
async def session_run_with_output(ctx: Context, session_id: str, command: str, end_strings: List[str], timeout: Optional[int] = 310) -> Dict:
    """Run a command in a session and wait for complete output."""
    client = get_client()
    try:
        session = client.sessions.session(session_id)
        if hasattr(session, "run_with_output"):
            output = session.run_with_output(command, end_strings, timeout)
            return {"success": True, "output": output}
        else:
            return {"error": "Session type does not support run_with_output"}
    except (KeyError, MsfRpcError) as e:
        return {"error": str(e)}

@ensure_connected
async def stop_session(ctx: Context, session_id: str) -> Dict:
    """Terminate a specific session."""
    client = get_client()
    try:
        session = client.sessions.session(session_id)
        session.stop()
        return {"success": True, "message": f"Session {session_id} terminated"}
    except (KeyError, MsfRpcError) as e:
        return {"error": str(e)}