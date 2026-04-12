# Architecture — How the Pieces Fit Together

## System Overview

```
┌───────────────────────────────────────────────────────────────┐
│                     YOUR PROJECT REPO                         │
│                                                               │
│  specag.config.yaml ─── tier, providers, hooks, ceremonies   │
│         │                                                     │
│         ├── specs/          ← your feature specs              │
│         ├── sprints/        ← velocity, estimation, retros    │
│         ├── agents/         ← token tracker, hooks, state     │
│         └── .sdd/           ← coding standards, templates     │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              PRE-CALL HOOK CHAIN                     │      │
│  │                                                     │      │
│  │  LLM call request                                   │      │
│  │    → DailyCapHook      (ALLOW / REJECT)             │      │
│  │    → WeeklyCapHook     (ALLOW / REJECT)             │      │
│  │    → WorkWindowHook    (ALLOW / REJECT)             │      │
│  │    → PausedRegistryHook(ALLOW / REJECT)             │      │
│  │    → PCModeHook        (ALLOW / DOWNGRADE)          │      │
│  │    → BudgetGuardHook   (ALLOW / REJECT)             │      │
│  │                                                     │      │
│  │  If all ALLOW → make the API call                   │      │
│  │  If any REJECT → call NOT made, logged              │      │
│  │  If DOWNGRADE → reroute to fallback model           │      │
│  └─────────────────────────────────────────────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ token_usage.db│  │hook_decisions│  │ paused-epics │        │
│  │   (SQLite)   │  │   (SQLite)   │  │   (.yaml)    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              CEREMONY ENGINE                         │      │
│  │                                                     │      │
│  │  Cron-driven (reads tier from config):              │      │
│  │    08:05  daily_standup.py                           │      │
│  │    18:00  po_daily_report.py                        │      │
│  │    15:00 Sat  sprint_review.py                      │      │
│  │    15:30 Sat  sprint_retro.py                       │      │
│  │    16:00 Sat  sprint_planning.py                    │      │
│  │    10:00 Sun  kickoff_reminder.py                   │      │
│  │    */15   token_monitor.py                          │      │
│  │    00:00  midnight_reset.py                         │      │
│  │    23:00 Sun  weekly_cost_report.py                 │      │
│  └─────────────────────────────────────────────────────┘      │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              SLACK INTERFACE                         │      │
│  │                                                     │      │
│  │  #dev      ← standups, reports, alerts, reviews     │      │
│  │  #planning ← sprint planning, kickoff, refinement   │      │
│  │                                                     │      │
│  │  Commands: pause <agent>, fallback <agent>, status,  │      │
│  │           cancel sprint, resume <agent>              │      │
│  └─────────────────────────────────────────────────────┘      │
└───────────────────────────────────────────────────────────────┘
```

## Key Architectural Decisions

### 1. Config-Driven Tier Enforcement

The `tier:` field in `specag.config.yaml` is the single source of truth for what's enforced. Every component reads it:

```
specag.config.yaml → tier: personal
  → Hook loader: loads daily_cap, weekly_cap, work_window, paused_registry, budget_guard
  → Ceremony engine: enables planning, kickoff, standup, review, retro (recommended)
  → Sprint validator: warns on DoR gaps but doesn't block
  → Commit hook: not installed (OPT at T2)
```

Changing the tier changes behavior immediately. No code changes, no redeployment.

### 2. Hooks Are the Enforcement Layer

The hook chain is the architectural pattern that makes everything else work:

```python
class PreCallHook:
    name: str
    def check(self, ctx: CallContext) -> HookResult: ...

class HookResult:
    decision: Decision    # ALLOW / REJECT / DOWNGRADE
    reason: str           # logged + shown in Slack
    hook_name: str

class CallContext:
    agent_role: str       # lead_dev / associate / po_agent
    provider: str
    model: str
    epic_id: str | None
    estimated_tokens: int
    purpose: str          # code-gen / review / report / chat / ceremony
```

**Why this design:**
- Hooks are independent. Each hook knows nothing about other hooks.
- First non-ALLOW wins. No conflicting decisions.
- Every decision is logged. Full audit trail in `hook_decisions` table.
- Adding a new hook = implement the interface + add to `hooks.yaml`. Zero changes to core.
- Removing a hook = delete from `hooks.yaml`. No orphan code.

### 3. SQLite for Everything Local

Two databases, both SQLite, both local:

| Database | Purpose | Tables |
|---|---|---|
| `token_usage.db` | Token tracking + cost accounting | `usage`, `hook_decisions` |

**Why SQLite, not Postgres:**
- Zero setup. `specag init` creates it automatically.
- File-based. Backs up with a single `cp` command.
- Fast enough for the scale (even 1M rows/year is trivial for SQLite).
- No network dependency. Works offline.
- For SpecAg Cloud (Path B), we swap SQLite for Postgres. Same schema, different driver.

### 4. Specs Are Markdown, Not Database Rows

Specs live as `.spec.md` files in the `specs/` directory, not in a database or issue tracker.

**Why:**
- Version-controlled. Git tracks every change.
- Readable without tooling. Any developer can read a spec in GitHub, their editor, or `cat`.
- Portable. No vendor lock-in.
- AI-friendly. LLMs read Markdown natively — no API adapter needed.
- Traceable. `git log --grep="ROOT-041"` shows every commit tied to a spec.

### 5. Framework vs. Project Separation

```
specag (pip package)          your-project/
├── templates/                 ├── specag.config.yaml    ← project-specific
├── rootine/ (CLI)             ├── specs/                 ← project-specific
└── docs/                      ├── agents/                ← copied from templates
                               ├── sprints/               ← generated at runtime
                               └── .sdd/                  ← copied from templates
```

`specag init` copies from `templates/` into your project. After that, your project owns those files. Framework updates don't overwrite your customizations.

**Upgrade path:** `specag upgrade` merges new template changes into your project, showing diffs for files you've modified. Never auto-overwrites.

## Data Flow

### 1. API Call Flow

```
Agent wants to call LLM API
  → Token tracker receives request
  → Hook chain runs (6 hooks in order)
  → If all ALLOW:
      → API call made
      → Response received
      → Usage logged to token_usage.db (provider, model, tokens, cost)
      → Response returned to agent
  → If any REJECT:
      → Call NOT made
      → Rejection logged to hook_decisions table
      → Agent receives rejection reason
      → Slack alert if threshold crossed
  → If DOWNGRADE:
      → Call rerouted to fallback model
      → Downgrade logged to hook_decisions table
      → Proceeds as ALLOW with fallback model
```

### 2. Blocker Escalation Flow

```
Blocker created (BLOCK-NNN)
  → Clock starts (T+0)
  → T+1: PO Agent posts nudge to #planning
  → T+3: PO Agent bumps priority, broadcasts downstream impact
  → T+7: PO Agent writes epic to paused-epics.yaml
       → PausedRegistryHook reads the file
       → All LLM calls tagged with that epic_id → REJECT
       → All dependent epics → also REJECT
       → Zero token spend on blocked paths
       → Stays paused until human resolves + PO removes from registry
```

### 3. Sprint Lifecycle Flow

```
Saturday 15:00  Sprint Review (PO posts completed work)
Saturday 15:30  Sprint Retro (all team posts, PO compiles)
                  → velocity.json updated
                  → estimation-log.md updated
                  → burndown.md updated
Saturday 16:00  Sprint Planning (PO proposes, Lead Dev reviews, Advisor approves)
                  → Sprint state: draft → planned

Sunday 10:00    Kickoff (tech spec grooming)
                  → Sprint state: planned → active

Mon-Fri         Development (agents work in 1hr ON / 3hr BREAK blocks)
                  → Daily standup 08:05
                  → Daily report 18:00
                  → Token monitor every 15 min

Saturday 15:00  Next Sprint Review (cycle repeats)
```

## Extension Points

| Extension | How | Example |
|---|---|---|
| Add a custom hook | Implement `PreCallHook`, add to `hooks.yaml` | GDPR hook that rejects calls with PII in the prompt |
| Change ceremony schedule | Edit `specag.config.yaml` → ceremonies section | Move standup to 09:00 instead of 08:05 |
| Add a new epic category | Add entry to Bible §8, update PO Agent logic | "Research" category with relaxed DoD |
| Integrate with Jira | Write a hook that reads blocker status from Jira API | `JiraPausedHook` replaces file-based `PausedRegistryHook` |
| Change the fallback chain | Edit provider config in `specag.config.yaml` | Add Groq as Tier 2 instead of DeepSeek |
