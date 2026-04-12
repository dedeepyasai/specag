#  PLAT-013: Sprint Cancellation Protocol

## [SUMMARY]
- App: SDD Platform (scaffolding)
- Epic owner: PO Agent (orchestration), Datta (sole authority to cancel)
- Status: BACKLOG
- Sprint: PC-01 Sprint 0
- Related specs: PLAT-006 (ceremonies), PLAT-008 (epic categories), PLAT-010 (continuous improvement)
- Priority: S1 — operational safety net

## [STORY]
As the team, we need a clearly defined protocol for cancelling a sprint mid-flight
when the sprint goal becomes obsolete, invalid, or impossible to achieve. Without
this protocol, a bad sprint drags agents through wasted work and pollutes the
burndown, retro, and velocity metrics. Only Datta can cancel a sprint — agents
cannot self-cancel.

## [TECH SPEC]

### 1. Definition

A **sprint cancellation** is the premature termination of an in-flight sprint
before its scheduled Saturday end. It is different from a normal sprint end:

| | Normal sprint end | Sprint cancellation |
|---|---|---|
| When | Saturday (day 7) | Any day 1–6 of the sprint |
| Authority | Scheduled | Datta only |
| Epics | Accepted or rolled over | All open epics returned to backlog |
| Review | Full demo + retro | Abbreviated post-mortem (no demo) |
| Velocity | Counted | NOT counted (excluded from average) |
| Burndown | Closed normally | Marked `CANCELLED` in history |

### 2. Who Can Cancel

**Datta is the sole authority.** Lead Dev, PO Agent, and Associate Developer
can *recommend* cancellation in `#specag-planning` but cannot execute it.
Slack command `cancel sprint` is restricted to Datta's user ID.

### 3. Valid Cancellation Triggers

| Trigger | Example | Who surfaces it |
|---|---|---|
| **Sprint goal obsolete** | Business requirement changed mid-sprint; all in-flight epics no longer valuable | Datta or PO |
| **Critical dependency broken** | Upstream API / infra failure blocks >50% of sprint scope | Lead Dev |
| **Production incident** | S1 prod bug requires full team focus for >2 days | Lead Dev or Datta |
| **Scope collapse** | >60% of sprint epics blocked and blockers cannot be resolved in ≤2 days | PO Agent |
| **Token/budget halt** | Weekly token cap hit and cannot be raised (see PLAT-001) | PO Agent |
| **Team unavailability** | Datta unavailable for >3 days AND sprint needs his approval gates | PO Agent |

Cancellation is **not** appropriate for:
- A single blocker (use a Blocker epic instead — see PLAT-008)
- Underestimation of a few epics (swap using Section 28 of Project Bible)
- One agent underperforming (reassign epics)
- Datta changing his mind about a feature's priority (swap, don't cancel)

### 4. Cancellation Flow

```
Step 1 — TRIGGER
  Someone surfaces the trigger in #specag-planning with justification.
  Format:
    "Recommend sprint cancellation. Trigger: <trigger>. Evidence: <facts>."

Step 2 — DATTA DECISION (within 4 hours of recommendation)
  Datta replies in #specag-planning:
    ✅ "Cancelling sprint. Reason: <reason>."
       → proceed to Step 3
    ❌ "Declined. Continue sprint. Action: <alternative>."
       → sprint continues, action item logged in retro

Step 3 — HALT
  PO Agent executes `cancel sprint` Slack command.
  PO Agent posts to #specag-dev:
    "🛑 SPRINT S-NN CANCELLED by Datta. All agents: stop work on assigned
     epics and push WIP. Do NOT open new PRs until next sprint kickoff."
  All agents commit/push work-in-progress to their feature branches.
  No new PRs are opened. Open PRs are marked `status: cancelled-sprint` and
  left open for the next sprint to reassess.

Step 4 — EPIC RECLASSIFICATION
  PO Agent updates INDEX.md:
    - Epics in BACKLOG → stay in BACKLOG
    - Epics in IN_PROGRESS → move back to BACKLOG with note
      "Returned from cancelled sprint S-NN. Re-groom before reassignment."
    - Epics in REVIEW → move to BACKLOG with same note
    - Epics in DONE → STAY in DONE (work that was accepted before cancellation
      is still accepted)
    - Blocker epics → remain open, retain due dates
  PO Agent updates burndown.json: sprint marked CANCELLED, velocity NOT
  counted in rolling average.

Step 5 — POST-MORTEM (within 24 hours of cancellation)
  Datta + PO + Lead Dev run a 30-minute post-mortem.
  Output: sprints/S-NN/cancellation-postmortem.md with:
    - Trigger
    - Timeline of events that led to cancellation
    - What was salvaged (accepted epics)
    - Root cause (Five Whys)
    - Action items (prevention) → tracked as AI-NNN in action-items.md
  NO normal retro. NO demo. NO sprint review.

Step 6 — NEXT SPRINT ADJUSTMENT
  Next sprint's planning explicitly accounts for the cancellation:
    - Capacity reduced for agents who worked on cancelled epics (fatigue)
    - Returned epics re-groomed before re-assignment
    - Post-mortem action items added to next sprint's scope
```

### 5. What Happens to In-Flight Work

| Artifact | Action |
|---|---|
| Commits already pushed | Stay on feature branch |
| Open PRs | Marked `cancelled-sprint` label, left open |
| Merged PRs | Stay merged (do not revert) |
| Feature branches | Kept — may be resumed next sprint |
| Dev environment deploys | Stay as-is (no rollback) |
| Prod environment deploys | Stay as-is (no rollback unless separate trigger) |
| Completed acceptance tests | Still valid |
| Draft tech specs | Kept as-is in specs/backlog/ |

**Rollback is NOT part of sprint cancellation.** Cancellation stops *future*
work; it does not undo *completed* work. If a rollback is also needed, Datta
triggers it separately via PLAT-012.

### 6. Burndown & Velocity Treatment

```json
// sprints/S-NN/burndown.json
{
  "sprint": "S-03",
  "status": "CANCELLED",
  "cancelled_on": "2026-05-20T14:30:00-05:00",
  "cancelled_by": "Datta",
  "reason": "Sprint goal invalidated — upstream API vendor changed contract",
  "points_forecast": 22,
  "points_accepted": 6,
  "points_returned_to_backlog": 16,
  "velocity_counted_in_average": false,
  "postmortem": "sprints/S-03/cancellation-postmortem.md"
}
```

**Velocity rule:** Cancelled sprints are excluded from the rolling velocity
average used for forecasting. This prevents a single bad sprint from
suppressing forecasts for 3+ sprints afterward.

### 7. Slack Commands

```
Datta: "cancel sprint"
  → Bot replies:
    ┌──────────────────────────────────────────┐
    │  ⚠️  SPRINT CANCELLATION                 │
    │                                           │
    │  Current: S-03 (Day 4 of 7)               │
    │  Goal:    <sprint goal>                   │
    │                                           │
    │  This will:                               │
    │  • Stop all agent work                    │
    │  • Return in-flight epics to backlog      │
    │  • Skip Saturday review + retro + demos   │
    │  • Trigger post-mortem within 24h         │
    │  • Exclude from velocity average          │
    │                                           │
    │  Reason (required):                       │
    │  Reply with "confirm cancel <reason>"     │
    │  Reply with "abort" to cancel this dialog │
    └──────────────────────────────────────────┘

Datta: "confirm cancel <reason text>"
  → Bot runs cancellation flow (Steps 3–4)
  → Bot posts cancellation notice to #specag-dev
  → Bot creates sprints/S-NN/cancellation-postmortem.md stub
  → Bot schedules post-mortem reminder in 24 hours

Datta: "sprint status"
  → Shows current sprint state, including CANCELLED if applicable
```

### 8. Post-Mortem Template

```markdown
# Sprint S-NN Cancellation Post-Mortem

- **Sprint:** S-NN
- **Cancelled on:** YYYY-MM-DD HH:MM CST
- **Cancelled by:** Datta
- **Day of sprint:** N of 7
- **Reason (short):** <one line>

## Timeline
- Day 1: ...
- Day 2: ...
- Day N: Cancellation decision

## What was forecast
- Points forecast: N
- Epics forecast: [IDs]

## What was salvaged (accepted before cancellation)
- Points accepted: N
- Epics accepted: [IDs]

## What returned to backlog
- Points returned: N
- Epics returned: [IDs]
- Re-grooming required: [IDs that changed substantially]

## Root cause (Five Whys)
1. Why did the sprint need to be cancelled? ...
2. Why did that happen? ...
3. ...
4. ...
5. ...

## Action items (AI-NNN — prevention)
- AI-NNN: <description> — Owner: <who> — Due: <date>

## Next sprint impact
- Capacity adjustment: ...
- Carried-over work: ...
- New scope from action items: ...
```

### 9. Audit Trail

Every cancellation leaves a permanent record in:
- `sprints/S-NN/cancellation-postmortem.md`
- `sprints/S-NN/burndown.json` (status: CANCELLED)
- `CHANGELOG.md` (entry: "Sprint S-NN cancelled — <reason>")
- `#specag-planning` Slack thread (pinned)
- `pc.manifest.yaml` cancellation log (appended):

```yaml
cancellation_log:
  - sprint: S-03
    date: "2026-05-20"
    reason: "Upstream API vendor changed contract"
    points_lost: 16
    postmortem: sprints/S-03/cancellation-postmortem.md
```

### 10. Limits

- **Max cancellations per PC:** 1. A second cancellation in the same PC requires
  Datta to also decide whether the entire PC is viable (see PC close protocol).
- **Cooldown:** After cancellation, the next sprint cannot also be cancelled
  unless the trigger is *different* from the first.
- **No partial cancellation.** Either the whole sprint is cancelled or it runs
  to completion. Partial scope reduction uses the Section 28 swap protocol.

### Files Touched
- `specs/platform/PLAT-013-sprint-cancellation.spec.md` — this spec
- `specag_project_bible.md` — Section 17 Quick Reference entry
- `app/agents/slack_commands.py` — `cancel sprint` / `confirm cancel` handlers
- `app/agents/po_agent.py` — cancellation orchestration
- `sprints/S-NN/cancellation-postmortem.md` — created on cancellation
- `sprints/S-NN/burndown.json` — CANCELLED status field
- `pc.manifest.yaml` — cancellation_log append

## [STANDARDS]
- Only Datta can cancel a sprint — Slack command is user-ID restricted
- A cancellation recommendation must include a trigger from Section 3
- Cancelled sprints are excluded from velocity averages
- Post-mortem must be created within 24 hours of cancellation
- No demo, no review, no normal retro for a cancelled sprint
- Merged work stays merged — cancellation is not rollback
- Max 1 cancellation per PC; second requires PC viability review
- All cancellations audited in `pc.manifest.yaml` cancellation_log

## [ACCEPTANCE CRITERIA]
```
AC-001: Given a cancellation trigger from Section 3, when a team member posts
        a recommendation in #specag-planning with justification, then Datta
        responds within 4 hours with accept or decline.

AC-002: Given Datta types "cancel sprint", when the bot responds with the
        confirmation dialog, then the dialog shows current sprint ID, day
        count, sprint goal, and impact summary.

AC-003: Given Datta types "confirm cancel <reason>", when the cancellation
        flow runs, then all agents receive the stop-work notification within
        60 seconds and INDEX.md reflects returned epics within 5 minutes.

AC-004: Given a sprint is cancelled, when burndown.json is updated, then
        status is set to CANCELLED, velocity_counted_in_average is false,
        and the entry is excluded from the rolling velocity average.

AC-005: Given a sprint is cancelled, when 24 hours pass, then a post-mortem
        using the Section 8 template must exist at
        sprints/S-NN/cancellation-postmortem.md — PO Agent auto-creates the
        stub at cancellation time.

AC-006: Given a cancellation recommendation does NOT match a Section 3
        trigger, when PO Agent reviews it, then the recommendation is
        declined with a pointer to the correct protocol (Blocker epic,
        mid-sprint swap, or reassignment).

AC-007: Given a cancellation has occurred in the current PC, when a second
        cancellation is recommended, then Datta must also complete a PC
        viability review before approving.

AC-008: Given a Slack user who is NOT Datta types "cancel sprint", when the
        bot receives the command, then the command is rejected with
        "Only Datta can cancel a sprint. Post a recommendation in
        #specag-planning instead."
```

## [CHANGE LOG]
- 2026-04-11: Initial spec created — cancellation authority, triggers, flow, post-mortem template, audit trail
