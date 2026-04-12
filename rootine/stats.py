"""Token usage and cost statistics."""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from rootine.brand import NAME
from rootine.config import get_tier, load_config

console = Console()


def show_stats() -> None:
    """Display token usage, cost summary, and active hooks."""
    config = load_config()
    if not config:
        console.print("[red]No rootine.config.yaml found. Run '{NAME_LOWER} init' first.[/red]")
        return

    tier = get_tier()
    project_name = config.get("project", {}).get("name", "unknown")
    hooks = config.get("hooks", {}).get("enabled", [])

    db_path = Path.cwd() / "agents" / "token_usage.db"
    has_db = db_path.exists()

    console.print(
        Panel(
            f"[bold]{NAME} Cost Summary[/bold] — {project_name} (T{'1' if tier == 'starter' else '2' if tier == 'personal' else '3'} {tier.title()})",
            border_style="blue",
        )
    )

    if not has_db:
        console.print("  [dim]No usage data yet. token_usage.db will be created on first API call.[/dim]")
        console.print()
    else:
        _show_usage_from_db(db_path, config)

    hooks_table = Table(title="Active Hooks", show_header=False, box=None, padding=(0, 2))
    hooks_table.add_column("Hook", style="cyan")
    hooks_table.add_column("Status", style="green")
    for hook in hooks:
        hooks_table.add_row(hook, "enabled")
    console.print(hooks_table)
    console.print()

    thresholds = config.get("alerts", {}).get("thresholds", [50, 80, 100])
    console.print(f"  Alert thresholds: {thresholds}")
    console.print(f"  Dedup window: {config.get('alerts', {}).get('deduplicate_minutes', 60)} min")


def _show_usage_from_db(db_path: Path, config: dict) -> None:
    """Read token_usage.db and display summary."""
    import sqlite3

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT provider, agent_role, model, SUM(input_tokens), SUM(output_tokens), SUM(cost_usd) "
            "FROM usage WHERE DATE(timestamp) = DATE('now') GROUP BY provider, agent_role, model"
        )
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        console.print("  [dim]Database exists but usage table not found.[/dim]")
        conn.close()
        return

    if rows:
        table = Table(title="Today's Usage")
        table.add_column("Provider")
        table.add_column("Agent")
        table.add_column("Model")
        table.add_column("Tokens", justify="right")
        table.add_column("Cost", justify="right")

        for provider, agent, model, in_tok, out_tok, cost in rows:
            table.add_row(provider, agent, model, f"{in_tok + out_tok:,}", f"${cost:.4f}")

        console.print(table)
    else:
        console.print("  [dim]No usage recorded today.[/dim]")

    console.print()
    conn.close()
