import asyncio
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tools import modules, sessions, console, jobs, exploits, database, execute

load_dotenv()  # Load environment variables

# Initialize the MCP server
mcp = FastMCP(
    "metasploit-mcp-server",
    description="An MCP server for interacting with the Metasploit Framework.",
    dependencies=["pymetasploit3>=1.0.6"],
    log_level="DEBUG",
    debug=True
)

# Add module management tools
mcp.add_tool(
    modules.list_modules,
    name="list_modules",
    description="List available Metasploit modules. Optionally filter by type: 'exploit', 'auxiliary', 'post', 'payload', 'encoder', or 'nop'. Returns a list of module names."
)
mcp.add_tool(
    modules.module_info,
    name="module_info",
    description="Get detailed information about a specific Metasploit module including description, options, references, targets, and compatible payloads. Required args: module_type (e.g., 'exploit', 'auxiliary', 'post') and module_name (e.g., 'windows/smb/ms17_010_eternalblue')."
)
mcp.add_tool(
    modules.search_modules,
    name="search_modules",
    description="Search for Metasploit modules using keywords. Can search by CVE, name, description, author, etc. Returns a list of matching modules with details."
)

# Add module execution tools from execute.py
mcp.add_tool(
    execute.execute_module,
    name="execute_module",
    description="Execute a Metasploit module with specified options. Required args: module_type (e.g., 'exploit'), module_name, and options dictionary (e.g., {'RHOSTS': '192.168.1.1', 'LHOST': '192.168.1.2'}). Returns job ID and execution status."
)
mcp.add_tool(
    execute.get_options,
    name="get_options",
    description="Get all available options for a Metasploit module. Required args: module_type and module_name. Returns dictionary of options with their descriptions, types, and required status."
)
mcp.add_tool(
    execute.set_option,
    name="set_option",
    description="Set a single option for a Metasploit module. Required args: module_type, module_name, option_name (e.g., 'RHOSTS'), and option_value. Returns success status."
)

# Add session management tools
mcp.add_tool(
    sessions.list_sessions,
    name="list_sessions",
    description="List all active Metasploit sessions. Returns session IDs, types (shell/meterpreter), target hosts, and information."
)
mcp.add_tool(
    sessions.session_shell_read,
    name="session_shell_read",
    description="Read output from a shell session. Required arg: session_id (integer). Returns the session output buffer."
)
mcp.add_tool(
    sessions.session_shell_write,
    name="session_shell_write",
    description="Send a command to a shell session. Required args: session_id (integer) and command (string). Use session_shell_read to get the output."
)
mcp.add_tool(
    sessions.session_meterpreter_read,
    name="session_meterpreter_read",
    description="Read output from a Meterpreter session. Required arg: session_id (integer). Returns the session output buffer."
)
mcp.add_tool(
    sessions.session_meterpreter_write,
    name="session_meterpreter_write",
    description="Send a command to a Meterpreter session. Required args: session_id (integer) and command (string). Common commands: 'sysinfo', 'getuid', 'ps', 'migrate', etc."
)
mcp.add_tool(
    sessions.session_run_with_output,
    name="session_run_with_output",
    description="Run a command in any session type and wait for output. Required args: session_id (integer) and command (string). Returns command output directly."
)
mcp.add_tool(
    sessions.stop_session,
    name="stop_session",
    description="Terminate an active session. Required arg: session_id (integer). Use with caution as this will close the connection to the target."
)

# Add console management tools
mcp.add_tool(
    console.create_console,
    name="create_console",
    description="Create a new Metasploit console for running commands. Returns console ID for use with other console tools."
)
mcp.add_tool(
    console.destroy_console,
    name="destroy_console",
    description="Destroy a Metasploit console. Required arg: console_id (string). Frees up resources by closing the console."
)
mcp.add_tool(
    console.list_consoles,
    name="list_consoles",
    description="List all active Metasploit consoles with their IDs and busy status."
)
mcp.add_tool(
    console.console_write,
    name="console_write",
    description="Write a command to a Metasploit console. Required args: console_id (string) and command (string). Use console_read to get output."
)
mcp.add_tool(
    console.console_read,
    name="console_read",
    description="Read output from a Metasploit console. Required arg: console_id (string). Returns console output buffer and prompt status."
)
mcp.add_tool(
    console.run_console_command,
    name="run_console_command",
    description="Run a command in a console and get the output. Required arg: command (string). Creates temporary console, runs command, and returns output."
)

# Add job management tools
mcp.add_tool(
    jobs.list_jobs,
    name="list_jobs",
    description="List all active Metasploit jobs including handlers and background tasks. Returns job IDs and descriptions."
)
mcp.add_tool(
    jobs.job_info,
    name="job_info",
    description="Get detailed information about a specific job. Required arg: job_id (integer). Returns job type, start time, and status."
)
mcp.add_tool(
    jobs.stop_job,
    name="stop_job",
    description="Stop a running Metasploit job. Required arg: job_id (integer). Use with caution as this terminates the job immediately."
)

# Add exploit execution tools
mcp.add_tool(
    exploits.execute_module,
    name="execute_exploit_module",
    description="Execute an exploit module with options. Required args: module_name (e.g., 'windows/smb/ms17_010_eternalblue') and options dictionary. Returns job ID and session information if successful."
)
mcp.add_tool(
    exploits.check_exploit,
    name="check_exploit",
    description="Check if a target is vulnerable to an exploit without actually exploiting it. Required args: module_name and target options. Returns vulnerability status."
)
mcp.add_tool(
    exploits.list_compatible_payloads,
    name="list_compatible_payloads",
    description="List all payloads compatible with a specific exploit module. Required arg: module_name. Returns list of compatible payload names and descriptions."
)
mcp.add_tool(
    exploits.get_module_options,
    name="get_module_options",
    description="Get all available options for an exploit module. Required arg: module_name. Returns dictionary of options with descriptions and requirements."
)

# Add database management tools
mcp.add_tool(
    database.list_workspaces,
    name="list_workspaces",
    description="List all Metasploit workspaces. Workspaces help organize different penetration testing engagements."
)
mcp.add_tool(
    database.create_workspace,
    name="create_workspace",
    description="Create a new Metasploit workspace. Required arg: workspace_name (string). Optional: description and boundary information."
)
mcp.add_tool(
    database.delete_workspace,
    name="delete_workspace",
    description="Delete a Metasploit workspace and all its data. Required arg: workspace_name (string). Use with caution - this cannot be undone."
)
mcp.add_tool(
    database.current_workspace,
    name="current_workspace",
    description="Get or set the current Metasploit workspace. Optional arg: workspace_name (string) to switch workspace. Returns current workspace name."
)
mcp.add_tool(
    database.list_hosts,
    name="list_hosts",
    description="List all hosts in the current workspace. Returns host addresses, operating systems, and other discovered information."
)
mcp.add_tool(
    database.list_services,
    name="list_services",
    description="List all services discovered in the current workspace. Returns service names, ports, protocols, and states."
)
mcp.add_tool(
    database.list_vulns,
    name="list_vulns",
    description="List all vulnerabilities found in the current workspace. Returns vulnerability details, affected hosts, and references."
)
mcp.add_tool(
    database.import_scan,
    name="import_scan",
    description="Import scan results into the database. Required args: file_path (string) and file_type (e.g., 'nmap', 'nessus'). Supports various scan file formats."
)

# Note: The server is run from main.py, not from here