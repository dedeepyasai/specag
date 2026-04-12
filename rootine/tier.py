"""Tier management — show, set, diff."""

from pathlib import Path

import yaml
from rich.console import Console
from rich.table import Table

from rootine.config import TIER_DEFAULTS, find_config, get_tier

console = Console()

TIER_LABELS = {"starter": "T1", "personal": "T2", "medium": "T3"}

ENFORCEMENT_MATRIX = {
    "Business spec before code": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Tech spec before code": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Commit epic-ref hook": {"starter": "OFF", "personal": "OPT", "medium": "REQ"},
    "PR updates spec changelog": {"starter": "OFF", "personal": "OPT", "medium": "REQ"},
    "Sprint Planning": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Sunday Kickoff": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Daily standup": {"starter": "OFF", "personal": "OPT", "medium": "REQ"},
    "Daily report": {"starter": "OFF", "personal": "OPT", "medium": "REQ"},
    "Sprint Review": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Sprint Retro": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Backlog refinement": {"starter": "OFF", "personal": "OPT", "medium": "REQ"},
    "Definition of Ready": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Definition of Done": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Test coverage": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "PR review required": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Demo per epic": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Token daily/weekly caps": {"starter": "REQ", "personal": "REQ", "medium": "REQ"},
    "Pre-call hook chain": {"starter": "REQ", "personal": "REQ", "medium": "REQ"},
    "Fallback model chain": {"starter": "REQ", "personal": "REQ", "medium": "REQ"},
    "Blocker SLA (1/3/7)": {"starter": "OFF", "personal": "REC", "medium": "REQ"},
    "Sprint cancellation protocol": {"starter": "OFF", "personal": "OPT", "medium": "REQ"},
    "Sustainable pace ceiling": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Velocity tracking": {"starter": "OFF", "personal": "OPT", "medium": "REQ"},
    "Tech debt register": {"starter": "OFF", "personal": "OPT", "medium": "REQ"},
    "Dev/Prod separation": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
    "Rollback mechanism": {"starter": "OPT", "personal": "REC", "medium": "REQ"},
}

STRICTNESS_STYLES = {
    "OFF": "dim",
    "OPT": "white",
    "REC": "yellow",
    "REQ": "bold green",
}


def show_tier() -> None:
    """Display current tier and enforcement matrix."""
    current = get_tier()
    label = TIER_LABELS.get(current, "??")
    console.print(f"[bold]Current tier: {label} {current.title()}[/bold]\n")

    table = Table(title="Enforcement Matrix")
    table.add_column("Dimension")
    table.add_column("Level", justify="center")

    for dimension, levels in ENFORCEMENT_MATRIX.items():
        level = levels[current]
        style = STRICTNESS_STYLES.get(level, "white")
        table.add_row(dimension, f"[{style}]{level}[/{style}]")

    console.print(table)


def diff_tier(target: str) -> None:
    """Show what changes when moving to a different tier."""
    current = get_tier()
    if current == target:
        console.print(f"[yellow]Already at tier '{target}'.[/yellow]")
        return

    current_label = TIER_LABELS.get(current, "??")
    target_label = TIER_LABELS.get(target, "??")
    upgrading = list(TIER_LABELS.keys()).index(target) > list(TIER_LABELS.keys()).index(current)

    console.print(
        f"[bold]{'Upgrade' if upgrading else 'Downgrade'}: "
        f"{current_label} {current.title()} → {target_label} {target.title()}[/bold]\n"
    )

    table = Table(title="Changes")
    table.add_column("Dimension")
    table.add_column(f"Current ({current_label})", justify="center")
    table.add_column(f"Target ({target_label})", justify="center")

    for dimension, levels in ENFORCEMENT_MATRIX.items():
        old = levels[current]
        new = levels[target]
        if old != new:
            old_style = STRICTNESS_STYLES.get(old, "white")
            new_style = STRICTNESS_STYLES.get(new, "white")
            table.add_row(
                dimension,
                f"[{old_style}]{old}[/{old_style}]",
                f"[{new_style}]{new}[/{new_style}]",
            )

    console.print(table)


def set_tier(new_tier: str) -> None:
    """Update the project tier in rootine.config.yaml."""
    config_path = find_config()
    if config_path is None:
        console.print("[red]No rootine.config.yaml found. Run '{NAME_LOWER} init' first.[/red]")
        return

    current = get_tier()
    if current == new_tier:
        console.print(f"[yellow]Already at tier '{new_tier}'.[/yellow]")
        return

    diff_tier(new_tier)
    console.print()

    upgrading = list(TIER_LABELS.keys()).index(new_tier) > list(TIER_LABELS.keys()).index(current)
    if not upgrading:
        if not click_confirm(
            "Downgrading will loosen enforcement. Some checks will no longer run. Proceed?"
        ):
            console.print("[dim]Cancelled.[/dim]")
            return

    with open(config_path) as f:
        config = yaml.safe_load(f)

    config["project"]["tier"] = new_tier
    config["hooks"]["enabled"] = TIER_DEFAULTS[new_tier]["hooks"]["enabled"]

    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    label = TIER_LABELS[new_tier]
    console.print(f"[bold green]Tier updated to {label} {new_tier.title()}.[/bold green]")


def click_confirm(message: str) -> bool:
    """Simple yes/no confirmation."""
    import click

    return click.confirm(message, default=False)
