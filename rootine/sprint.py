"""Sprint lifecycle commands — prepare, kickoff, status."""

from pathlib import Path

from rich.console import Console
from rich.table import Table

from rootine.brand import NAME_LOWER
from rootine.config import get_tier, load_config

console = Console()


def prepare_sprint() -> None:
    """Validate all specs in specs/ against the Definition of Ready."""
    config = load_config()
    if not config:
        console.print("[red]No rootine.config.yaml found. Run '{NAME_LOWER} init' first.[/red]")
        return

    tier = get_tier()
    specs_dir = Path.cwd() / "specs"

    if not specs_dir.exists():
        console.print("[red]No specs/ directory found. Write some specs first.[/red]")
        return

    spec_files = list(specs_dir.rglob("*.spec.md"))
    if not spec_files:
        console.print("[yellow]No .spec.md files found in specs/. Write your first spec.[/yellow]")
        return

    console.print(f"[bold]Sprint Preparation — Tier: {tier}[/bold]\n")

    total_issues = 0
    for spec_file in sorted(spec_files):
        issues = _validate_spec(spec_file, tier)
        rel_path = spec_file.relative_to(Path.cwd())
        if issues:
            console.print(f"[red]FAIL[/red] {rel_path}")
            for issue in issues:
                console.print(f"  [red]x[/red] {issue}")
                total_issues += 1
        else:
            console.print(f"[green]PASS[/green] {rel_path}")

    console.print()
    if total_issues == 0:
        console.print("[bold green]All specs pass Definition of Ready. Ready for sprint.[/bold green]")
    else:
        console.print(f"[bold red]{total_issues} issue(s) found. Fix and re-run.[/bold red]")


def _validate_spec(spec_path: Path, tier: str) -> "List[str]":
    """Check a spec file against DoR. Returns list of issues (empty = pass)."""
    content = spec_path.read_text(encoding="utf-8")
    issues = []

    if tier in ("personal", "medium"):
        if "## [STORY]" not in content and "## [SUMMARY]" not in content:
            issues.append("Missing [SUMMARY] or [STORY] section")
        if "## [ACCEPTANCE CRITERIA]" not in content:
            issues.append("Missing [ACCEPTANCE CRITERIA] section")

    if tier == "medium":
        if "## [TECH SPEC]" not in content:
            issues.append("Missing [TECH SPEC] section")
        if "Story points" not in content and "story_points" not in content:
            issues.append("Story points not assigned")
        if "### Files Touched" not in content:
            issues.append("Missing 'Files Touched' section")

    return issues


def kickoff_sprint() -> None:
    """Transition the current sprint from planned to active."""
    config = load_config()
    if not config:
        console.print("[red]No rootine.config.yaml found. Run '{NAME_LOWER} init' first.[/red]")
        return

    console.print("[bold]Sprint Kickoff[/bold]")
    console.print()
    console.print("[yellow]Sprint state machine not yet implemented (v0.2.0).[/yellow]")
    console.print(f"For now, validate your specs with [bold]{NAME_LOWER} sprint prepare[/bold]")
    console.print("and begin work manually.")
