import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
ALLOWED_ACTIONS = {
    "scale": REPO_ROOT / "scripts" / "scale-service.ps1",
    "restart": REPO_ROOT / "scripts" / "restart-service.ps1",
}
SERVICE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,62}$")


def run_remediation(action, service, timeout=30):
    """Execute an allowlisted remediation action."""
    if action not in ALLOWED_ACTIONS:
        return {
            "success": False,
            "error": f"Unsupported remediation action: {action}",
        }

    if not SERVICE_NAME_PATTERN.fullmatch(service):
        return {
            "success": False,
            "error": f"Invalid service name: {service}",
        }

    return run_powershell(ALLOWED_ACTIONS[action], service, timeout=timeout)


def run_powershell(script_path, service, timeout=30):
    """Execute an allowlisted PowerShell script with a service parameter."""
    resolved_script = Path(script_path).resolve()
    allowed_scripts = {path.resolve() for path in ALLOWED_ACTIONS.values()}

    if resolved_script not in allowed_scripts:
        return {
            "success": False,
            "error": f"Script is not allowlisted: {resolved_script}",
        }

    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-File", str(resolved_script), "-ServiceName", service],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
