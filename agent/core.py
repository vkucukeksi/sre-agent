from tools.observability import get_metrics, get_logs
from tools.executor import run_powershell

def run_agent(event):
    print("Agent running...")

    service = event["service"]

    metrics = get_metrics(service)
    logs = get_logs(service)

    print(f"[INFO] Metrics: {metrics}")
    print(f"[INFO] Logs: {logs}")

    if metrics["cpu"] > 85:
        action = "scale"
        script = "scripts/scale-service.ps1"
    else:
        action = "restart"
        script = "scripts/restart-service.ps1"

    result = run_powershell(script, service)

    return {
        "service": service,
        "action": action,
        "result": result
    }