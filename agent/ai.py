import os

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def decide_action_ai(metrics, logs, thresholds):
    prompt = f"""
You are a Senior Site Reliability Engineer.

Metrics:
{metrics}

Logs:
{logs}

Thresholds:
{thresholds}

Decide the best action:
- scale (if system is overloaded)
- restart (if errors are occurring)
- none (if system is healthy)

Respond ONLY in valid JSON.

Example:
{{
  "action": "scale",
  "reason": "CPU and latency exceeded thresholds",
  "confidence": 0.92
}}
"""

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "system",
                "content": "You are an expert SRE agent. Respond only with valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown wrappers if returned
    content = content.replace("```json", "").replace("```", "").strip()

    return content