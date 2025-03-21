# tools/jobs.py
from typing import Dict
from pymetasploit3.msfrpc import MsfRpcError
from mcp.server.fastmcp import Context
from utils.msf_utils import get_client, ensure_connected

@ensure_connected
async def list_jobs(ctx: Context) -> Dict:
    """List all active Metasploit jobs."""
    client = get_client()
    try:
        jobs = client.jobs.list
        return {"jobs": jobs}
    except MsfRpcError as e:
        return {"error": str(e)}

@ensure_connected
async def job_info(ctx: Context, job_id: str) -> Dict:
    """Get information about a specific job."""
    client = get_client()
    try:
        jobs = client.jobs.list
        if job_id in jobs:
            return {"job_id": job_id, "info": jobs[job_id]}
        else:
            return {"error": f"Job {job_id} not found"}
    except MsfRpcError as e:
        return {"error": str(e)}

@ensure_connected
async def stop_job(ctx: Context, job_id: str) -> Dict:
    """Stop a specific job."""
    client = get_client()
    try:
        result = client.jobs.stop(job_id)
        return {"success": True, "message": f"Job {job_id} stopped"}
    except MsfRpcError as e:
        return {"error": str(e)} 