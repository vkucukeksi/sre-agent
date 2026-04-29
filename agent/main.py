from agent.core import run_agent

if __name__ == "__main__":
    print("Starting agent...")

    event = {
        "service": "payment-api",
        "issue": "high latency"
    }

    result = run_agent(event)

    print("Final Result:")
    print(result)
