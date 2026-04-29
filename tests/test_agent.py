import json
import unittest
from pathlib import Path

from agent.config import load_config
from agent.core import decide_action, run_agent
from tools.executor import run_powershell, run_remediation


REPO_ROOT = Path(__file__).resolve().parent.parent


class AgentDecisionTests(unittest.TestCase):
    def test_high_latency_scenario_scales(self):
        scenario = json.loads((REPO_ROOT / "scenarios" / "high_latency.json").read_text())
        config = load_config()
        calls = []

        result = run_agent(
            {"service": scenario["trigger"]["service"]},
            config=config,
            metrics_provider=lambda service: scenario["metrics"],
            logs_provider=lambda service: scenario["logs"],
            executor=lambda action, service: calls.append((action, service)) or {"success": True},
        )

        self.assertEqual(scenario["expected_action"], result["action"])
        self.assertEqual([("scale", "payment-api")], calls)
        self.assertIn("latency", result["decision"]["breached_thresholds"])

    def test_errors_restart_when_thresholds_are_not_breached(self):
        action, decision = decide_action(
            metrics={"cpu": 20, "memory": 30, "latency": 100},
            logs=["ERROR: database connection failed"],
            thresholds={"cpu": 85, "memory": 80, "latency": 1000},
        )

        self.assertEqual("restart", action)
        self.assertEqual("errors_detected", decision["reason"])

    def test_noop_when_service_is_healthy(self):
        calls = []

        result = run_agent(
            {"service": "payment-api"},
            config=load_config(),
            metrics_provider=lambda service: {"cpu": 20, "memory": 30, "latency": 100},
            logs_provider=lambda service: ["INFO: healthy"],
            executor=lambda action, service: calls.append((action, service)),
        )

        self.assertEqual("none", result["action"])
        self.assertEqual([], calls)

    def test_unknown_service_fails_before_remediation(self):
        with self.assertRaises(ValueError):
            run_agent(
                {"service": "missing-service"},
                config=load_config(),
                metrics_provider=lambda service: {},
                logs_provider=lambda service: [],
            )


class ExecutorSafetyTests(unittest.TestCase):
    def test_rejects_unknown_remediation_action(self):
        result = run_remediation("delete", "payment-api")

        self.assertFalse(result["success"])
        self.assertIn("Unsupported remediation action", result["error"])

    def test_rejects_invalid_service_name(self):
        result = run_remediation("scale", "payment-api; Remove-Item")

        self.assertFalse(result["success"])
        self.assertIn("Invalid service name", result["error"])

    def test_rejects_non_allowlisted_script(self):
        result = run_powershell(REPO_ROOT / "config.yaml", "payment-api")

        self.assertFalse(result["success"])
        self.assertIn("not allowlisted", result["error"])


if __name__ == "__main__":
    unittest.main()
