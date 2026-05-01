import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

Respond in JSON format:
{{
  "action": "...",
  "reason": "...",
  "confidence": 0.0-1.0
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content