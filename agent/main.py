import sys
import os

sys.path.append(os.path.dirname(__file__))

from core import run_agent

if __name__ == "__main__":
    print("Starting agent...")

    event = {
        "service": "payment-api",
        "issue": "high latency"
    }

    result = run_agent(event)

    print("Final Result:")
    print(result)