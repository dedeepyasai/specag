# PLAT-001: Token Usage Monitoring & Alerts

## [SUMMARY]
- App: SpecAg
- Epic owner: Datta + PO Agent
- Status: BACKLOG
- Sprint: PC-01 Sprint 1
- Related specs: INFRA-001, PLAT-002, PLAT-003
- Priority: S2 — must be live before agents start working

## [STORY]
As Datta (Advisor), I need real-time visibility into token usage across all providers
and agents so I can make informed decisions about pausing, switching to fallback models,
or letting agents continue — all from a single Slack channel.

## [TECH SPEC]

### SQLite Schema — token_usage.db
```sql
CREATE TABLE IF NOT EXISTS usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    provider TEXT NOT NULL,          -- anthropic / openai / deepseek / google / groq
    agent_role TEXT NOT NULL,        -- lead_dev / associate / po_agent
    model TEXT NOT NULL,             -- claude-sonnet-4-6 / gpt-4.1 / etc.
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    cost_usd REAL NOT NULL,
    tier TEXT NOT NULL               -- primary / fallback / emergency
);

CREATE INDEX idx_usage_daily ON usage(provider, agent_role, DATE(timestamp));
CREATE INDEX idx_usage_weekly ON usage(provider, agent_role, timestamp);
```

### Token Limits Configuration (agent_limits.yaml)
```yaml
providers:
  anthropic:
    agents:
      lead_dev:
        model: "claude-sonnet-4-6"
        daily_token_cap: 40000
        weekly_token_cap: 200000
        max_tokens_per_call: 4000
        cost_per_1m_in: 3.00
        cost_per_1m_out: 15.00
        work_window: "08:00-22:00 CST"

  openai:
    agents:
      associate:
        model: "gpt-4.1"
        daily_token_cap: 80000
        weekly_token_cap: 400000
        max_tokens_per_call: 4000
        cost_per_1m_in: 2.00
        cost_per_1m_out: 8.00
        work_window: "08:00-22:00 CST"
      po_agent:
        model: "gpt-4o-mini"
        daily_token_cap: 20000
        weekly_token_cap: 100000
        max_tokens_per_call: 2000
        cost_per_1m_in: 0.15
        cost_per_1m_out: 0.60
        cron: "0 18 * * 1-5"

  deepseek:
    agents:
      lead_dev:
        model: "deepseek-chat"
        daily_token_cap: 500000
        weekly_token_cap: 2000000
        cost_per_1m_in: 0.27
        cost_per_1m_out: 1.10
      associate:
        model: "deepseek-coder"
        daily_token_cap: 500000
        weekly_token_cap: 2000000
        cost_per_1m_in: 0.14
        cost_per_1m_out: 0.28

  google:
    agents:
      po_agent:
        model: "gemini-2.0-flash"
        daily_token_cap: 1000000
        weekly_token_cap: 5000000
        cost_per_1m_in: 0.00
        cost_per_1m_out: 0.00

alerts:
  thresholds: [50, 80, 100]
  slack_channel: "#specag-dev"
  mention_at: ["@datta"]
```

### Alert Thresholds & Behavior
| Threshold | Icon | Level | Slack Behavior |
|---|---|---|---|
| 50% daily cap | :bar_chart: | INFO | Informational message — no action needed |
| 80% daily cap | :warning: | WARNING | Alert with @datta mention + action commands |
| 100% daily cap | :rotating_light: | LIMIT REACHED | Urgent alert + auto-suggestion to pause or fallback |
| 80% weekly cap | :warning: | WARNING | Weekly budget pressure alert |
| 100% weekly cap | :rotating_light: | HALT | Full halt for that provider until Monday 08:00 CST |

### Monitoring Cron Schedule
```bash
# Every 15 minutes during work hours (Mon-Fri)
*/15 8-22 * * 1-5  /app/venv/bin/python /app/agents/token_monitor.py

# Midnight reset — counters don't reset, but agents resume + switch to primary
0 0 * * *          /app/venv/bin/python /app/agents/midnight_reset.py

# Weekly cost summary — Sunday night
0 23 * * 0         /app/venv/bin/python /app/agents/weekly_cost_report.py
```

### Slack Alert Format
```
*Token Usage Alert*

:warning: *ANTHROPIC* — Lead Dev
    Daily: 32,400 / 40,000 (81%)
    Cost today: $0.3150
    Estimated exhaust: ~3:45 PM

:bar_chart: *OPENAI* — Associate
    Daily: 45,000 / 80,000 (56%)
    Cost today: $0.2100

:bar_chart: *OPENAI* — PO Agent
    Daily: 8,200 / 20,000 (41%)
    Cost today: $0.0049

*Commands:*
`pause lead` `pause associate` `pause all`
`fallback lead` `fallback all`
`status`
```

### Weekly Cost Report Format (Sunday 11 PM)
```
*Weekly Cost Report — Week of Apr 6–12*

| Agent | Provider | Tokens Used | Weekly Cap | % Used | Cost |
|---|---|---|---|---|---|
| Lead Dev | Anthropic | 156,000 | 200,000 | 78% | $1.42 |
| Associate | OpenAI | 312,000 | 400,000 | 78% | $1.68 |
| PO Agent | OpenAI | 72,000 | 100,000 | 72% | $0.043 |
| Lead Dev | DeepSeek (fallback) | 24,000 | — | — | $0.03 |

*Total week spend: $3.17*
*Month-to-date: $11.42*
*Projected year: $137.04*

Fallback events this week: 2 (Anthropic cap hit Tue + Thu)
```

### Pre-Call Enforcement Hooks

Before any API call is logged to `token_usage.db`, the tracker runs a chain of
**pre-call hooks**. Each hook can `ALLOW`, `REJECT`, or `DOWNGRADE` the call.
Hooks are pluggable so this repo can be used as a starter template by other
projects — the hook interface stays stable, the implementations are swappable.

**Hook interface:**

```python
# app/agents/hooks/pre_call_hook.py
from dataclasses import dataclass
from enum import Enum

class Decision(Enum):
    ALLOW = "allow"
    REJECT = "reject"       # do not make the call at all
    DOWNGRADE = "downgrade" # force fallback tier (see PLAT-002)

@dataclass
class CallContext:
    agent_role: str         # lead_dev / associate / po_agent
    provider: str
    model: str
    epic_id: str | None     # optional — None for non-epic work (ceremonies, reports)
    sprint_id: str | None
    estimated_tokens: int
    purpose: str            # "code-gen" | "review" | "report" | "chat" | "ceremony"

@dataclass
class HookResult:
    decision: Decision
    reason: str             # shown in logs + Slack
    hook_name: str

class PreCallHook:
    name: str
    def check(self, ctx: CallContext) -> HookResult: ...
```

**Default hook chain (evaluated in order, first non-ALLOW wins):**

| Order | Hook | Purpose | Configurable |
|---|---|---|---|
| 1 | `DailyCapHook` | Reject if daily cap reached | `agent_limits.yaml` |
| 2 | `WeeklyCapHook` | Reject if weekly cap reached | `agent_limits.yaml` |
| 3 | `WorkWindowHook` | Reject if outside agent work window | `agent_limits.yaml` |
| 4 | **`PausedRegistryHook`** | **Reject if `ctx.epic_id` is in the paused-epic registry (blocker hard-pause at T+7)** | **`hooks.yaml` → registry_path** |
| 5 | `PCModeHook` | Downgrade to low-cost model if `active_pc_mode` forces it (see `agent.limits.yaml`) | `agent.limits.yaml` |
| 6 | `BudgetGuardHook` | Reject if estimated cost would exceed remaining weekly budget | `agent_limits.yaml` |

Template users swap, add, or remove hooks by editing `hooks.yaml` — no code
changes to the core tracker.

### Paused Epic Registry (Hard-Pause Store)

The `PausedRegistryHook` reads a small, portable file that lists epics
currently in hard-pause state (see Project Bible Section 29.8 — T+7 cascade).
Format is deliberately minimal so any tool can write to it:

```yaml
## {registry_path — default: agents/state/paused-epics.yaml}
## Written by: PO Agent when a blocker reaches T+7
## Written by: any tool exposing the same schema
## Read by:    PausedRegistryHook before every LLM call

paused_epics:
  - epic_id: "ROOT-055"
    blocker_id: "BLOCK-001"
    paused_at: "2026-05-18T09:00:00-05:00"
    reason: "BLOCK-001 hard-pause — waiting on Datta decision on auth provider"
    owner: "Datta"
    dependent_epics: ["ROOT-056", "ROOT-057"]
  - epic_id: "ROOT-056"
    blocker_id: "BLOCK-001"
    paused_at: "2026-05-18T09:00:00-05:00"
    reason: "Dependent on ROOT-055 (hard-paused)"
    owner: "Datta"
```

**Rules:**
- Registry path is configured in `hooks.yaml`, NOT hard-coded to this project
- Epic IDs are opaque strings — this repo uses `ROOT-NNN` / `PLAT-NNN` / `BLOCK-NNN`, but a template user may use `ACME-123`, `JIRA-456`, etc.
- Writing to the registry is PO Agent's job during PC-01. A template user may point to a different writer (cron that pulls from Linear, Jira webhook, etc.) as long as it produces the same schema.
- PO Agent also removes entries when blockers are resolved.
- The registry is append-mostly — PO writes full file atomically (temp file + rename) to avoid torn reads.

### hooks.yaml — Hook Configuration

```yaml
## Where to find the hook registry & which hooks are active.
## This file is meant to be EDITED by template users when they adopt this
## repo for their own project.

pre_call_hooks:
  enabled:
    - daily_cap
    - weekly_cap
    - work_window
    - paused_registry
    - pc_mode
    - budget_guard

  paused_registry:
    implementation: "PausedRegistryHook"
    registry_path: "agents/state/paused-epics.yaml"
    # To use a different source (Linear, Jira, database), replace implementation:
    # implementation: "LinearPausedHook"
    # linear_api_key: "${LINEAR_API_KEY}"
    # linear_project_id: "xyz"

  pc_mode:
    implementation: "PCModeHook"
    source: "year-{year}/PC-{pc}/pc.manifest.yaml"  # template — {year} and {pc} resolved at runtime
    # Template users change this path to match their project layout
```

### Hook Decision Logging

Every rejected or downgraded call is logged to a new table so Datta can audit
what was suppressed and why:

```sql
CREATE TABLE IF NOT EXISTS hook_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    agent_role TEXT NOT NULL,
    epic_id TEXT,
    hook_name TEXT NOT NULL,
    decision TEXT NOT NULL,     -- allow / reject / downgrade
    reason TEXT NOT NULL
);

CREATE INDEX idx_hook_decisions_daily ON hook_decisions(DATE(timestamp), decision);
```

The daily report includes a line:
```
Hook rejections today: 3 (2 × paused_registry, 1 × daily_cap)
Hook downgrades today: 12 (12 × pc_mode)
```

### Files Touched
- `/app/agents/token_tracker.py` — SQLite read/write functions; runs the hook chain before every call
- `/app/agents/token_monitor.py` — cron job, threshold checks, Slack alerts
- `/app/agents/midnight_reset.py` — auto-resume + primary model switch
- `/app/agents/weekly_cost_report.py` — Sunday night summary
- `/app/agents/hooks/pre_call_hook.py` — hook interface + default implementations
- `/app/agents/hooks/paused_registry_hook.py` — reads registry file, rejects paused epics
- `/app/agents/hooks/pc_mode_hook.py` — reads PC manifest, downgrades per active_pc_mode
- `/app/config/agent_limits.yaml` — all caps and thresholds
- `/app/config/hooks.yaml` — hook configuration (template users edit this)
- `{registry_path}` — paused epic registry (default: `agents/state/paused-epics.yaml`)
- `/app/agents/token_usage.db` — SQLite database (auto-created, contains `usage` + `hook_decisions` tables)

## [STANDARDS]
- Every API call MUST run the pre-call hook chain BEFORE the API call is made
- A `REJECT` decision from any hook means the call MUST NOT be made — no "try anyway"
- A `DOWNGRADE` decision MUST route the call to the fallback tier per PLAT-002
- Every hook decision (allow/reject/downgrade) MUST be logged to `hook_decisions` table
- Every successful API call MUST log to `usage` table before returning the response to the agent
- Cost calculation MUST use exact per-model pricing from agent_limits.yaml
- Alerts MUST deduplicate — same threshold level for same agent not re-sent within 1 hour
- Weekly cap hit = full halt, no override except manual `resume` command from Datta
- Hook implementations are pluggable via `hooks.yaml` — core tracker code MUST NOT hard-code project-specific paths or epic ID formats
- Paused registry path MUST be configurable — default `agents/state/paused-epics.yaml`, template users may point elsewhere
- token_usage.db MUST be backed up with weekly VPS snapshot

## [ACCEPTANCE CRITERIA]
```
AC-001: Given an agent makes an API call, when the call completes, then the
        usage (provider, model, tokens, cost) is logged to token_usage.db.

AC-002: Given Lead Dev usage hits 80% daily cap, when token_monitor.py runs,
        then a WARNING alert is posted to #specag-dev with @datta mention.

AC-003: Given Associate usage hits 100% daily cap, when token_monitor.py runs,
        then a LIMIT REACHED alert is posted with pause/fallback commands.

AC-004: Given weekly cap is hit for a provider, when token_monitor.py detects it,
        then all agents on that provider are halted until Monday 08:00 CST.

AC-005: Given it is Sunday 11 PM, when weekly_cost_report.py runs, then a
        formatted cost summary is posted to #specag-dev showing all agents.

AC-006: Given the same threshold was already alerted within the last hour, when
        token_monitor.py runs again, then no duplicate alert is sent.

AC-007: Given an agent attempts an LLM call, when the tracker is invoked, then
        the pre-call hook chain runs in the order defined by hooks.yaml, and
        the first non-ALLOW decision is returned without running later hooks.

AC-008: Given an epic ID is present in the paused epic registry, when an agent
        makes a call tagged with that epic_id, then the PausedRegistryHook
        returns REJECT with reason "blocker hard-pause active", the call is
        NOT made, and the decision is logged to the hook_decisions table.

AC-009: Given a template user points `paused_registry.registry_path` in
        hooks.yaml to a custom location, when the tracker starts, then the
        PausedRegistryHook reads from that path without any core code change.

AC-010: Given active_pc_mode is set to a low-cost mode in the PC manifest, when
        an agent makes a call, then PCModeHook returns DOWNGRADE and the call
        is routed to the fallback tier (per PLAT-002), unless the epic has an
        active escalation override.

AC-011: Given hooks.yaml lists only a subset of hooks under `enabled`, when the
        tracker starts, then only those hooks are loaded and executed — no
        disabled hook runs.

AC-012: Given a PausedRegistryHook REJECT fires, when the daily report runs,
        then the report shows the rejection count grouped by hook name and
        agent role.
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created
- 2026-04-11: Added pluggable pre-call hook chain (Decision: ALLOW/REJECT/DOWNGRADE). Added PausedRegistryHook to enforce blocker hard-pause (Project Bible Section 29.8 / PLAT-008 cascading SLA). Added hooks.yaml configuration. Added hook_decisions table. Hook implementations and registry paths are configurable so this repo can be used as a starter template by other projects without editing core code. Added AC-007..AC-012.
