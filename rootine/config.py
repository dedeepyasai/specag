"""Configuration loader — reads rootine.config.yaml and applies tier defaults."""

from pathlib import Path
from typing import Optional

import yaml

CONFIG_FILE = "rootine.config.yaml"

TIER_DEFAULTS = {
    "starter": {
        "ceremonies": {
            "sprint_planning": False,
            "sunday_kickoff": False,
            "daily_standup": False,
            "daily_report": False,
            "sprint_review": False,
            "sprint_retro": False,
            "backlog_refinement": False,
        },
        "hooks": {
            "enabled": ["daily_cap", "weekly_cap", "budget_guard"],
        },
        "spec_required": False,
        "commit_hook": False,
        "pr_review_required": False,
    },
    "personal": {
        "ceremonies": {
            "sprint_planning": True,
            "sunday_kickoff": True,
            "daily_standup": False,
            "daily_report": False,
            "sprint_review": True,
            "sprint_retro": True,
            "backlog_refinement": False,
        },
        "hooks": {
            "enabled": [
                "daily_cap",
                "weekly_cap",
                "work_window",
                "paused_registry",
                "budget_guard",
            ],
        },
        "spec_required": True,
        "commit_hook": False,
        "pr_review_required": True,
    },
    "medium": {
        "ceremonies": {
            "sprint_planning": True,
            "sunday_kickoff": True,
            "daily_standup": True,
            "daily_report": True,
            "sprint_review": True,
            "sprint_retro": True,
            "backlog_refinement": True,
        },
        "hooks": {
            "enabled": [
                "daily_cap",
                "weekly_cap",
                "work_window",
                "paused_registry",
                "pc_mode",
                "budget_guard",
            ],
        },
        "spec_required": True,
        "commit_hook": True,
        "pr_review_required": True,
    },
}


def find_config() -> "Optional[Path]":
    """Walk up from cwd to find rootine.config.yaml."""
    current = Path.cwd()
    while current != current.parent:
        candidate = current / CONFIG_FILE
        if candidate.exists():
            return candidate
        current = current.parent
    return None


def load_config() -> dict:
    """Load and return the project config, merged with tier defaults."""
    config_path = find_config()
    if config_path is None:
        return {}

    with open(config_path) as f:
        config = yaml.safe_load(f) or {}

    tier = config.get("project", {}).get("tier", "personal")
    defaults = TIER_DEFAULTS.get(tier, TIER_DEFAULTS["personal"])

    for key, value in defaults.items():
        if key not in config:
            config[key] = value
        elif isinstance(value, dict) and isinstance(config[key], dict):
            for k, v in value.items():
                config[key].setdefault(k, v)

    return config


def get_tier() -> str:
    """Return the current project tier."""
    config = load_config()
    return config.get("project", {}).get("tier", "personal")
