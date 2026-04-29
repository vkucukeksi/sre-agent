# SRE Agent

An autonomous Site Reliability Engineering agent that monitors services and takes corrective actions.

## Features

- Real-time metrics monitoring
- Automatic scaling based on CPU/memory thresholds
- Service restart capabilities
- Log analysis and alerting
- Scenario-based testing
- Config-driven remediation decisions
- Allowlisted remediation script execution

## Project Structure

```
.
├── agent/              # Core agent logic
│   ├── core.py        # Main agent execution
│   ├── main.py        # Entry point
│   └── prompt.py      # Agent prompts
├── tools/             # Utility modules
│   ├── executor.py    # Script execution
│   └── observability.py # Metrics & logs
├── scripts/           # PowerShell scripts
│   ├── restart-service.ps1
│   └── scale-service.ps1
├── scenarios/         # Test scenarios
│   └── high_latency.json
└── config.yaml        # Configuration
```

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

## Configuration

See `config.yaml` for service thresholds, monitoring intervals, and action parameters.

The agent currently uses mock observability data from `tools/observability.py`. Replace that module with your Prometheus, CloudWatch, Grafana, or log provider integration before using this against live services.

## Development

- Add new scenarios to `scenarios/` folder
- Modify scripts in `scripts/` for custom actions
- Register new remediation actions in `tools/executor.py`
- Update `agent/prompt.py` for agent behavior customization
