import os
from datetime import timedelta

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

load_dotenv()

workspace_id = os.getenv("AZURE_LOG_ANALYTICS_WORKSPACE_ID")

credential = DefaultAzureCredential()
client = LogsQueryClient(credential)


def query_logs(query, minutes=30):
    response = client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=timedelta(minutes=minutes),
    )

    if response.status == "Success":
        table = response.tables[0]

        results = []
        for row in table.rows:
            results.append(dict(zip(table.columns, row)))

        return results

    return []