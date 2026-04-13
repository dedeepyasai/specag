"""Project initialization — scaffolds a new SpecAg project."""

from datetime import date, timedelta
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

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
    """Initialize a new SpecAg project — interactive new/existing flow."""
    cwd = Path.cwd()
    config_path = cwd / CONFIG_FILE

    if config_path.exists():
        console.print(f"[red]{CONFIG_FILE} already exists. Aborting.[/red]")
        return

    # Step 1: New or existing?
    console.print()
    project_type = click.prompt(
        "Is this a new project or an existing project?",
        type=click.Choice(["new", "existing"]),
        default="new",
    )

    # Step 2: Sprint configuration
    console.print()
    console.print("[bold]Sprint Configuration[/bold]")
    sprint_naming = click.prompt(
        "Sprint naming pattern (use {n} for number)",
        default="S{n}",
    )
    cadence_days = click.prompt(
        "Sprint cadence (days)",
        type=click.IntRange(1, 30),
        default=7,
    )
    start_day = click.prompt(
        "Sprint start day",
        type=click.Choice(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]),
        default="sunday",
    )

    # Calculate next occurrence of start_day
    default_start = _next_weekday(start_day)
    first_sprint_date = click.prompt(
        "First sprint start date (YYYY-MM-DD)",
        default=default_start.isoformat(),
    )

    current_sprint_num = 1
    if project_type == "existing":
        current_sprint_num = click.prompt(
            "What sprint number should we start from?",
            type=int,
            default=1,
        )

    current_sprint = sprint_naming.replace("{n}", str(current_sprint_num))

    # Show summary
    console.print()
    console.print(
        Panel(
            f"[bold]Initializing {NAME} project[/bold]\n\n"
            f"  Type:    {project_type}\n"
            f"  Name:    {name}\n"
            f"  Owner:   {owner}\n"
            f"  Tier:    {tier}\n"
            f"  Sprint:  {current_sprint} ({cadence_days}-day cadence, starts {first_sprint_date})",
            title=f"{NAME_LOWER} init",
            border_style="green",
        )
    )

    # Create scaffold directories
    for dir_path in SCAFFOLD_DIRS:
        (cwd / dir_path).mkdir(parents=True, exist_ok=True)
        console.print(f"  [dim]created[/dim] {dir_path}/")

    # Write config
    config = {
        "project": {
            "name": name,
            "owner": owner,
            "tier": tier,
            "timezone": "America/Chicago",
        },
        "sprints": {
            "naming": sprint_naming,
            "cadence_days": cadence_days,
            "start_day": start_day,
            "current_sprint": current_sprint,
            "current_sprint_num": current_sprint_num,
            "first_sprint_date": first_sprint_date,
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

    # Handle existing project scanning
    specs_generated = 0
    if project_type == "existing":
        specs_generated = _handle_existing_project(cwd, name, owner)

    # Done
    console.print()
    console.print(f"[bold green]Done![/bold green] Project '{name}' initialized at tier '{tier}'.")
    if specs_generated > 0:
        console.print(f"  Generated [bold]{specs_generated}[/bold] spec drafts — review them in specs/")
    console.print()
    console.print("Next steps:")
    if project_type == "existing":
        console.print("  1. Review generated specs in specs/ — they are DRAFT status")
        console.print("  2. Fill in [STORY], [TECH SPEC], and [ACCEPTANCE CRITERIA]")
        console.print("  3. Change status from DRAFT to READY when approved")
    else:
        console.print("  1. Write your first spec in specs/")
    console.print(f"  {3 if project_type == 'existing' else 2}. Run [bold]{NAME_LOWER} sprint prepare[/bold] to validate")
    console.print(f"  {4 if project_type == 'existing' else 3}. Run [bold]{NAME_LOWER} stats[/bold] to check budget")
    console.print()


def _handle_existing_project(cwd: Path, name: str, owner: str) -> int:
    """Scan existing project and generate spec drafts."""
    from rootine.scanner import generate_spec_drafts, scan_project, write_spec_file

    console.print()
    console.print("[bold]Scanning project...[/bold]")

    scan_result = scan_project(cwd)

    if scan_result["total_files"] == 0:
        console.print("  [yellow]No source files found to scan.[/yellow]")
        return 0

    # Show scan results
    console.print(f"  Found [bold]{scan_result['total_files']}[/bold] files across [bold]{len(scan_result['directories'])}[/bold] directories")
    if scan_result["languages"]:
        langs = ", ".join(f"{k} ({v})" for k, v in sorted(scan_result["languages"].items(), key=lambda x: -x[1]))
        console.print(f"  Languages: {langs}")
    if scan_result["frameworks"]:
        console.print(f"  Frameworks: {', '.join(scan_result['frameworks'])}")
    if scan_result["entry_points"]:
        console.print(f"  Entry points: {', '.join(scan_result['entry_points'])}")

    # Generate spec drafts
    drafts = generate_spec_drafts(scan_result, name, owner)

    if not drafts:
        console.print("  [yellow]No modules detected for spec generation.[/yellow]")
        return 0

    # Show drafts table for user to review
    console.print()
    table = Table(title="Generated Spec Drafts")
    table.add_column("#", style="dim")
    table.add_column("Spec ID", style="bold")
    table.add_column("Title")
    table.add_column("Files", justify="right")
    table.add_column("SP", justify="right")
    table.add_column("Languages")

    for i, draft in enumerate(drafts, 1):
        table.add_row(
            str(i),
            draft["id"],
            draft["title"],
            str(draft["file_count"]),
            str(draft["story_points"]),
            draft["languages"],
        )

    console.print(table)
    console.print()

    # Ask user which specs to generate
    generate_all = click.confirm("Generate all spec drafts?", default=True)

    if not generate_all:
        selected_input = click.prompt(
            "Enter spec numbers to generate (comma-separated, e.g. 1,3,5)",
            default=",".join(str(i) for i in range(1, len(drafts) + 1)),
        )
        try:
            selected_indices = [int(x.strip()) - 1 for x in selected_input.split(",")]
            drafts = [drafts[i] for i in selected_indices if 0 <= i < len(drafts)]
        except (ValueError, IndexError):
            console.print("[yellow]Invalid selection. Generating all specs.[/yellow]")

    # Write spec files
    spec_dir = cwd / "specs" / "backlog"
    count = 0
    for draft in drafts:
        filepath = write_spec_file(spec_dir, draft, name, owner)
        console.print(f"  [green]created[/green] {filepath.relative_to(cwd)}")
        count += 1

    return count


def _hooks_for_tier(tier: str) -> list:
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


def _next_weekday(day_name: str) -> date:
    """Return the date of the next occurrence of the given weekday."""
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    target = days.index(day_name.lower())
    today = date.today()
    days_ahead = target - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return today + timedelta(days=days_ahead)


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
    """Copy tier-appropriate templates into the project."""
    demo_script = cwd / ".sdd" / "templates" / "demo-script.md"
    if not demo_script.exists():
        demo_script.write_text(
            "# Demo Script Template\n\n"
            f"See https://github.com/dedeepyasai/specag/blob/master/templates/shared/.sdd/templates/demo-script.md\n"
        )
        console.print(f"  [green]created[/green] .sdd/templates/demo-script.md")
