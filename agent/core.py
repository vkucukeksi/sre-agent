from agent.config import get_service_config, load_config
from tools.executor import run_remediation
from tools.observability import get_logs, get_metrics


def decide_action(metrics, logs, thresholds):
    """Choose a remediation action from metrics and logs."""
    breached = [
        name
        for name, limit in thresholds.items()
        if name in metrics and metrics[name] > limit
    ]
    has_errors = any("ERROR" in line.upper() for line in logs)

    # Case 1: Thresholds breached → scale
    if breached:
        return "scale", {
            "breached_thresholds": breached,
            "reason": f"Thresholds exceeded: {', '.join(breached)}",
            "confidence": min(1.0, len(breached) * 0.3),
        }

    # Case 2: Errors in logs → restart
    if has_errors:
        return "restart", {
            "breached_thresholds": [],
            "reason": "Errors detected in logs",
            "confidence": 0.6,
        }
            
     # Case 3: No issues → do nothing
    return "none", {
        "breached_thresholds": [],
        "reason": "No action required",
        "confidence": 0.9,
    }


def run_agent(
    event,
    config=None,
    metrics_provider=get_metrics,
    logs_provider=get_logs,
    executor=run_remediation,
):
    print("Agent running...")

    service = event["service"]
    config = config or load_config()
    service_config = get_service_config(config, service)
    thresholds = service_config.get("thresholds", {})

    metrics = metrics_provider(service)
    logs = logs_provider(service)

    print(f"[INFO] Metrics: {metrics}")
    print(f"[INFO] Logs: {logs}")

    action, decision = decide_action(metrics, logs, thresholds)

    if action == "none":
        result = {
            "success": True,
            "stdout": "No remediation required.",
            "stderr": "",
            "returncode": 0,
        }
    else:
        result = executor(action, service)

    return {
        "service": service,
        "action": action,
        "decision": decision,
        "result": result,
    }
