from tools.azure_monitor import query_logs


def get_logs(service):
    query = f"""
    Heartbeat
    | where Computer contains "{service}"
    | take 5
    """

    results = query_logs(query)

    return [
        f"INFO: Heartbeat received from {row['Computer']}"
        for row in results
    ]


def get_metrics(service):
    """
    Temporary metrics until real Azure metrics are wired in.
    """

    return {
        "cpu": 20,
        "memory": 30,
        "latency": 100
    }