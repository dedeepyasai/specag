"""SpecAg CLI — the main entry point for all rootine commands."""

import click

from rootine import __version__
from rootine.brand import NAME, NAME_LOWER, TAGLINE


@click.group()
@click.version_option(version=__version__, prog_name=NAME_LOWER)
def main():
    """Run an AI engineering team with full cost control and traceability."""


@main.command()
@click.option(
    "--tier",
    type=click.Choice(["starter", "personal", "medium"]),
    prompt="Project tier",
    help="Stakes-based tier: starter (experiments), personal (side project), medium (real users).",
)
@click.option("--name", prompt="Project name", help="Name of your project.")
@click.option("--owner", prompt="Your name", help="Project owner name.")
def init(tier: str, name: str, owner: str):
    """Initialize a new SpecAg project in the current directory."""
    from rootine.init import init_project

    init_project(name=name, owner=owner, tier=tier)


@main.group()
def sprint():
    """Sprint lifecycle commands."""


@sprint.command()
def prepare():
    """Validate specs against Definition of Ready for the next sprint."""
    from rootine.sprint import prepare_sprint

    prepare_sprint()


@sprint.command()
def kickoff():
    """Transition sprint from planned to active."""
    from rootine.sprint import kickoff_sprint

    kickoff_sprint()


@main.command()
def stats():
    """Show token usage, cost summary, and hook activity."""
    from rootine.stats import show_stats

    show_stats()


@main.group()
def tier():
    """View or change the project tier."""


@tier.command("show")
def tier_show():
    """Show current tier and what's enforced."""
    from rootine.tier import show_tier

    show_tier()


@tier.command("set")
@click.argument("new_tier", type=click.Choice(["starter", "personal", "medium"]))
def tier_set(new_tier: str):
    """Change the project tier (starter/personal/medium)."""
    from rootine.tier import set_tier

    set_tier(new_tier)


@tier.command("diff")
@click.argument("target_tier", type=click.Choice(["starter", "personal", "medium"]))
def tier_diff(target_tier: str):
    """Show what changes when moving to a different tier."""
    from rootine.tier import diff_tier

    diff_tier(target_tier)


if __name__ == "__main__":
    main()
