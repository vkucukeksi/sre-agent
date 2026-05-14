from tools.azure_monitor import query_logs

query = """
Heartbeat
| take 5
"""

results = query_logs(query)

for row in results:
    print(
        f"VM={row['Computer']} | "
        f"OS={row['OSName']} {row['OSMajorVersion']} | "
        f"Agent={row['Category']}"
    )