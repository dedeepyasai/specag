# PLAT-004: Agent State Management

## [SUMMARY]
- App: SpecAg
- Epic owner: Lead Dev Agent
- Status: BACKLOG
- Sprint: PC-01 Sprint 1
- Related specs: PLAT-001, PLAT-002, PLAT-003
- Priority: S2 — orchestrator depends on this for all agent lifecycle decisions

## [STORY]
As the orchestrator, I need a single source of truth for each agent's current state
(active/paused, which model tier, pause expiry) so that every component — cron jobs,
Slack commands, model router, token monitor — makes consistent decisions.

## [TECH SPEC]

### State File — agent_state.json
Location: `/app/agents/agent_state.json`
Updated by: Slack commands, token monitor, midnight reset, manual override

```json
{
  "lead_dev": {
    "status": "active",
    "tier": "primary",
    "paused_until": null,
    "current_model": "claude-sonnet-4-6",
    "current_epic": "ROOT-041",
    "last_activity": "2026-04-10T14:32:00"
  },
  "associate": {
    "status": "active",
    "tier": "primary",
    "paused_until": null,
    "current_model": "gpt-4.1",
    "current_epic": "ROOT-048",
    "last_activity": "2026-04-10T14:28:00"
  },
  "po_agent": {
    "status": "active",
    "tier": "primary",
    "paused_until": null,
    "current_model": "gpt-4o-mini",
    "current_epic": null,
    "last_activity": "2026-04-10T08:05:00"
  }
}
```

### State Transitions
```
                    ┌──────────┐
          resume    │          │  pause (Datta command)
       ┌───────────►│  ACTIVE  ├──────────────┐
       │            │          │               │
       │            └────┬─────┘               ▼
       │                 │              ┌──────────┐
       │    fallback cmd │              │  PAUSED  │
       │                 │              │          │
       │                 ▼              └────┬─────┘
       │          ┌──────────┐               │
       │          │ ACTIVE   │    midnight   │
       └──────────┤ (fallback│◄──────────────┘
                  │  tier)   │   auto-resume
                  └──────────┘
```

### State Fields
| Field | Type | Description |
|---|---|---|
| `status` | `active` / `paused` | Whether agent accepts new tasks and makes API calls |
| `tier` | `primary` / `fallback` / `emergency` | Which model tier to use for next API call |
| `paused_until` | ISO datetime / null | Auto-resume timestamp. null = indefinite until manual resume |
| `current_model` | string | Actual model string being used right now |
| `current_epic` | string / null | Epic ID currently being worked on (null if idle) |
| `last_activity` | ISO datetime | Timestamp of last API call or state change |

### State Check — Before Every API Call
The orchestrator calls `is_agent_active()` before every single API call.
If paused, the call is queued. If the pause has expired, auto-resume happens.

### Checkpoint on Pause
When an agent is paused mid-work:
1. Current progress is written to a checkpoint file: `/app/agents/{role}/checkpoint.json`
2. Checkpoint contains: epic ID, files modified so far, last completed step, branch name
3. On resume, agent reads checkpoint and continues from where it stopped
4. No work is lost — just deferred

### Midnight Reset Logic
Runs at 00:00 daily:
1. All agents: `status` → `active`
2. All agents: `tier` → `primary`
3. All agents: `paused_until` → `null`
4. `current_model` updated to primary model per agent_limits.yaml
5. Slack notification posted: "Midnight Reset Complete"
6. Exception: weekly cap hit → agent stays paused until Monday 08:00

### Files Touched
- `/app/agents/agent_state.py` — AgentStateManager class (read/write/pause/resume/fallback)
- `/app/agents/agent_state.json` — persisted state (single source of truth)
- `/app/agents/{role}/checkpoint.json` — mid-work checkpoints per agent
- `/app/agents/midnight_reset.py` — reads + updates agent_state.json

## [STANDARDS]
- agent_state.json is the ONLY file that tracks agent status — no other state stores
- Every state change MUST update `last_activity` timestamp
- Checkpoint files MUST be created before any pause that interrupts active work
- State file MUST be atomic-write safe (write to temp file, then rename)
- All state transitions logged to `/app/logs/state_changes.log`

## [ACCEPTANCE CRITERIA]
```
AC-001: Given Lead Dev is active, when Datta types "pause lead", then
        agent_state.json shows status="paused" and paused_until is set to
        tomorrow 08:00 CST within 2 seconds.

AC-002: Given Associate is paused with paused_until set, when the expiry time
        passes and a cron job or API call check runs, then Associate auto-resumes.

AC-003: Given Lead Dev is mid-epic, when paused, then a checkpoint.json is written
        containing the current epic ID, branch, and last completed step.

AC-004: Given Lead Dev was paused with a checkpoint, when resumed, then the agent
        reads checkpoint.json and continues from the saved step.

AC-005: Given midnight reset runs, then all agents are set to active/primary/null
        and Slack notification is posted.

AC-006: Given weekly cap was hit for OpenAI, when midnight reset runs, then
        Associate and PO Agent remain paused (exception to normal reset).

AC-007: Given two processes try to update agent_state.json simultaneously, then
        atomic write prevents corruption (temp file + rename pattern).
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created
