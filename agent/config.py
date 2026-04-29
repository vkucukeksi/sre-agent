"""Configuration loading for the SRE agent."""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = REPO_ROOT / "config.yaml"


def load_config(path=DEFAULT_CONFIG_PATH):
    """Load agent configuration from YAML."""
    config_path = Path(path)
    content = config_path.read_text(encoding="utf-8")

    try:
        import yaml
    except ImportError:
        return _load_supported_yaml(content)

    data = yaml.safe_load(content)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid configuration in {config_path}")
    return data


def get_service_config(config, service_name):
    """Return the config block for a named service."""
    for service in config.get("services", []):
        if service.get("name") == service_name:
            return service
    raise ValueError(f"Unknown service: {service_name}")


def _load_supported_yaml(content):
    """Parse the small config.yaml shape used by this prototype."""
    config = {"services": [], "monitoring": {}, "actions": {}}
    section = None
    current_service = None
    current_action = None
    in_thresholds = False

    for raw_line in content.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        if indent == 0 and stripped.endswith(":"):
            section = stripped[:-1]
            current_service = None
            current_action = None
            in_thresholds = False
            continue

        if section == "services":
            if stripped.startswith("- "):
                key, value = _split_key_value(stripped[2:])
                current_service = {key: _coerce_value(value)}
                config["services"].append(current_service)
                in_thresholds = False
            elif current_service is not None and stripped == "thresholds:":
                current_service["thresholds"] = {}
                in_thresholds = True
            elif current_service is not None and in_thresholds:
                key, value = _split_key_value(stripped)
                current_service["thresholds"][key] = _coerce_value(value)
        elif section == "monitoring":
            key, value = _split_key_value(stripped)
            config["monitoring"][key] = _coerce_value(value)
        elif section == "actions":
            if indent == 2 and stripped.endswith(":"):
                current_action = stripped[:-1]
                config["actions"][current_action] = {}
            elif current_action is not None:
                key, value = _split_key_value(stripped)
                config["actions"][current_action][key] = _coerce_value(value)

    return config


def _split_key_value(text):
    key, value = text.split(":", 1)
    return key.strip(), value.strip()


def _coerce_value(value):
    if value.isdigit():
        return int(value)
    return value
