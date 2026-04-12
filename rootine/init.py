"""Project initialization — scaffolds a new SpecAg project."""

import shutil
from importlib import resources
from pathlib import Path

import yaml
from rich.console import Console
from rich.panel import Panel

from rootine.brand import NAME, NAME_LOWER
from rootine.config import CONFIG_FILE

console = Console()

SCAFFOLD_DIRS = [
    "specs/platform",
    "specs/backlog",
    "specs/interrupt",
    "agents/hooks",
    "agents/state",
    "sprints",
    ".sdd/templates",
    ".sdd/onboarding",
]


def init_project(name: str, owner: str, tier: str) -> None:
    """Initialize a new SpecAg project in the current directory."""
    cwd = Path.cwd()
    config_path = cwd / CONFIG_FILE

    if config_path.exists():
        console.print(f"[red]{CONFIG_FILE} already exists. Aborting.[/red]")
        return

    console.print(
        Panel(
            f"[bold]Initializing {NAME} project[/bold]\n\n"
            f"  Name:  {name}\n"
            f"  Owner: {owner}\n"
            f"  Tier:  {tier}",
            title=f"{NAME_LOWER} init",
            border_style="green",
        )
    )

    for dir_path in SCAFFOLD_DIRS:
        (cwd / dir_path).mkdir(parents=True, exist_ok=True)
        console.print(f"  [dim]created[/dim] {dir_path}/")

    config = {
        "project": {
            "name": name,
            "owner": owner,
            "tier": tier,
            "timezone": "America/Chicago",
        },
        "hooks": {
            "enabled": _hooks_for_tier(tier),
            "paused_registry": {
                "registry_path": "agents/state/paused-epics.yaml",
            },
        },
        "alerts": {
            "thresholds": [50, 80, 100],
            "slack_channel": "#dev",
            "deduplicate_minutes": 60,
        },
    }

    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    console.print(f"  [green]created[/green] {CONFIG_FILE}")

    _write_empty_velocity(cwd / "sprints" / "velocity.json")
    _write_empty_estimation_log(cwd / "sprints" / "estimation-log.md")
    _write_paused_registry(cwd / "agents" / "state" / "paused-epics.yaml")
    _copy_templates(cwd, tier)

    console.print()
    console.print(f"[bold green]Done![/bold green] Project '{name}' initialized at tier '{tier}'.")
    console.print()
    console.print("Next steps:")
    console.print("  1. Write your first spec in specs/")
    console.print(f"  2. Run [bold]{NAME_LOWER} sprint prepare[/bold] to validate")
    console.print(f"  3. Run [bold]{NAME_LOWER} stats[/bold] to check budget")
    console.print()
    console.print(f"Read the study guide: [link]docs/study-guide.md[/link]")


def _hooks_for_tier(tier: str) -> "List[str]":
    if tier == "starter":
        return ["daily_cap", "weekly_cap", "budget_guard"]
    if tier == "personal":
        return ["daily_cap", "weekly_cap", "work_window", "paused_registry", "budget_guard"]
    return [
        "daily_cap",
        "weekly_cap",
        "work_window",
        "paused_registry",
        "pc_mode",
        "budget_guard",
    ]


def _write_empty_velocity(path: Path) -> None:
    path.write_text('{\n  "sprints": [],\n  "rolling_average_5": null,\n  "last_updated": null\n}\n')
    console.print(f"  [green]created[/green] {path.relative_to(Path.cwd())}")


def _write_empty_estimation_log(path: Path) -> None:
    content = (
        "# Estimation Calibration Log\n"
        "# Owner: PO Agent | Reviewed: every retro\n\n"
        "| Epic | Category | Estimated | Actual | Drift % | Notes |\n"
        "|---|---|---|---|---|---|\n"
    )
    path.write_text(content)
    console.print(f"  [green]created[/green] {path.relative_to(Path.cwd())}")


def _write_paused_registry(path: Path) -> None:
    path.write_text("paused_epics: []\n")
    console.print(f"  [green]created[/green] {path.relative_to(Path.cwd())}")


def _copy_templates(cwd: Path, tier: str) -> None:
    """Copy tier-appropriate templates into the project.

    In v0.1.0, this creates placeholder files. In v0.2.0+, it will
    copy from the installed package's templates/ directory.
    """
    demo_script = cwd / ".sdd" / "templates" / "demo-script.md"
    if not demo_script.exists():
        demo_script.write_text(
            "# Demo Script Template\n\n"
            "See https://github.com/YOUR_USERNAME/rootine/blob/main/templates/shared/.sdd/templates/demo-script.md\n"
        )
        console.print(f"  [green]created[/green] .sdd/templates/demo-script.md")
