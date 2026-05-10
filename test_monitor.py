from dotenv import dotenv_values

print(dotenv_values(".env"))

from tools.azure_monitor import query_logs

query = """
Heartbeat
| take 5
"""

results = query_logs(query)

print(results)