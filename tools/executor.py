def run_powershell(script_path, service):
    """Execute a PowerShell script with service parameter"""
    import subprocess
    try:
        result = subprocess.run(
            ["powershell", "-File", script_path, "-ServiceName", service],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }