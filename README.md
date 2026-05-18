# SRE Agent

An autonomous Site Reliability Engineering agent that collects service signals, asks Azure OpenAI for a remediation decision, and safely runs allowlisted recovery scripts.

## Features

- **Azure observability**
  - Queries Azure Log Analytics through `LogsQueryClient`
  - Reads recent VM heartbeat data for the target service
  - Keeps temporary mock metrics in place until live metrics are wired in

- **Decision engine**
  - Uses Azure OpenAI for JSON remediation decisions
  - Falls back to deterministic rule-based logic if AI is unavailable
  - Supports `scale`, `restart`, and `none` actions

- **Safe execution**
  - Runs only allowlisted PowerShell remediation scripts
  - Validates service names before execution
  - Returns structured execution results

- **Testing**
  - Scenario-driven agent tests
  - Dependency injection for metrics, logs, and execution
  - Safety tests for unsupported actions, invalid service names, and non-allowlisted scripts

## Project Structure

```text
.
├── agent/
│   ├── ai.py              # Azure OpenAI decision logic
│   ├── config.py          # Configuration loader
│   ├── core.py            # Agent orchestration and fallback decisions
│   ├── main.py            # Local entry point
│   └── prompt.py          # Prompt customization
├── tools/
│   ├── azure_monitor.py   # Azure Log Analytics client/query helper
│   ├── executor.py        # Safe remediation execution
│   └── observability.py   # Logs and metrics providers
├── scripts/
│   ├── restart-service.ps1
│   └── scale-service.ps1
├── scenarios/
│   └── high_latency.json
├── tests/
│   └── test_agent.py
├── config.yaml
├── test_monitor.py        # Manual Azure Log Analytics smoke test
└── requirements.txt
```

## Decision Flow

1. Load the target service from `config.yaml`.
2. Collect metrics and logs for the service.
3. Ask Azure OpenAI for a JSON remediation decision.
4. Fall back to rule-based logic if the AI call fails.
5. Run the selected remediation through the safe executor.
6. Return the service, action, decision details, and execution result.

## Getting Started

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Configure services and thresholds in `config.yaml`.

3. Set the required environment variables:

   ```powershell
   $env:AZURE_OPENAI_API_KEY="your-api-key"
   $env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
   $env:AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
   $env:AZURE_LOG_ANALYTICS_WORKSPACE_ID="your-workspace-id"
   ```

   You can also place these values in a local `.env` file.

4. Authenticate to Azure for Log Analytics access. The app uses `DefaultAzureCredential`, so Azure CLI login, managed identity, or another supported Azure identity can be used.

5. Run the agent:

   ```bash
   python -m agent.main
   ```

6. Run tests:

   ```bash
   python -m unittest discover -s tests
   ```

## Configuration

`config.yaml` defines the services the agent is allowed to evaluate and the thresholds used by the fallback decision logic. Current service entries include:

- `payment-api`
- `sre-vm-dev`
- `user-service`

The entry point currently sends a sample high-latency event for `sre-vm-dev`.

## Azure Monitoring

`tools/azure_monitor.py` wraps Azure Log Analytics queries. `tools/observability.py` uses it to query the `Heartbeat` table and return recent heartbeat log lines for the requested service:

```kusto
Heartbeat
| where Computer contains "<service>"
| take 5
```

`test_monitor.py` can be used as a quick manual smoke test for Log Analytics connectivity.

Metrics are still temporary static values in `tools/observability.py`; replace `get_metrics` with Azure Monitor, Prometheus, CloudWatch, or another metrics provider before relying on the agent for live remediation.

## Development

- Add new scenarios to `scenarios/`.
- Adjust service thresholds in `config.yaml`.
- Modify remediation scripts in `scripts/`.
- Register new remediation actions in `tools/executor.py`.
- Update `agent/prompt.py` or `agent/ai.py` for decision behavior changes.

## Future Improvements

- Live Azure Monitor metrics integration
- Kubernetes remediation support
- Multi-step AI reasoning
- Incident correlation across services
- Dashboard or UI
