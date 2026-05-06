# SRE Agent

An autonomous Site Reliability Engineering agent that monitors services and takes corrective actions.

## Features

-  **Observability Analysis**
  - Monitors CPU, memory, latency
  - Parses logs for error signals

-  **Decision Engine**
  - AI-based decisions (OpenAI / Azure OpenAI)
  - Automatic fallback to rule-based logic if AI is unavailable

-  **Safe Execution**
  - Allowlisted remediation scripts only
  - Input validation to prevent command injection

-  **Testing**
  - Scenario-driven testing
  - Dependency injection for observability and execution layers

## Project Structure

```
.
├── agent/ # Core agent logic
│ ├── core.py # Main agent execution
│ ├── config.py # Configuration loader
│ ├── ai.py # AI decision logic
│ └── main.py # Entry point
│
├── tools/ # Utility modules
│ ├── executor.py # Safe script execution
│ └── observability.py # Metrics & logs
│
├── scripts/ # PowerShell remediation scripts
│ ├── restart-service.ps1
│ └── scale-service.ps1
│
├── scenarios/ # Test scenarios
│ └── high_latency.json
│
├── tests/ # Unit tests
│ └── test_agent.py
│
├── config.yaml
└── README.md
```
##  Decision Flow

1. Collect metrics and logs  
2. Attempt AI-based decision  
3. If AI fails → fallback to rule-based logic  
4. Execute remediation safely  
5. Return structured result  

---

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure services in `config.yaml`

3. Run the agent:
   ```bash
   python -m agent.main
   ```

4. Run tests:
   ```bash
   python -m unittest discover -s tests
   ```

## AI Configuration

$env:OPENAI_API_KEY="your-api-key"

If AI is unavailable (e.g. quota exceeded), the agent automatically falls back to rule-based decisions.

See `config.yaml` for service thresholds, monitoring intervals, and action parameters.

The agent currently uses mock observability data from `tools/observability.py`. Replace that module with your Prometheus, CloudWatch, Grafana, or log provider integration before using this against live services.

## Development

- Add new scenarios to `scenarios/` folder
- Modify scripts in `scripts/` for custom actions
- Register new remediation actions in `tools/executor.py`
- Update `agent/prompt.py` for agent behavior customization

## Future Improvements

- Azure Monitor / Prometheus integration
- Kubernetes support
- Multi-step AI reasoning
- Incident correlation across services
 -Dashboard / UI

