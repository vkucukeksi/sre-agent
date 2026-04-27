"""Observability tools for monitoring and logging"""

def get_metrics(service):
    """Retrieve metrics for a service"""
    return {
        "cpu": 92,
        "memory": 70,
        "latency": 1200
    }

def get_logs(service):
    """Retrieve logs for a service"""
    return [
        "ERROR: timeout connecting to db",
        "WARN: retry attempt"
    ]