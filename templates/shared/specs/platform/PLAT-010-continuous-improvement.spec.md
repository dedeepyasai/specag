# PLAT-010: Continuous Improvement & Enhanced Retrospective

## [SUMMARY]
- App: SpecAg
- Epic owner: {{ADVISOR}} (Scrum Master / Advisor), PO (facilitates)
- Status: BACKLOG
- Sprint: PC-01 Sprint 0
- Related specs: PLAT-006 (ceremonies)
- Priority: S1 — the feedback loop that improves everything else

## [STORY]
As the team, we need a structured retrospective that captures real problems from every
role — developers, PO, and Advisor — and produces concrete action items that {{ADVISOR}}
(as Scrum Master) owns and tracks. The Agile methodology itself is a living system
that {{ADVISOR}} continuously evolves based on retro findings.

## [TECH SPEC]

### 1. {{ADVISOR}}'s Dual Role: Advisor + Scrum Master

| Responsibility | What it means |
|---|---|
| **Advisor** | Final authority, QA tester, epic seeder, decision gates |
| **Scrum Master** | Owns action items from retros, removes impediments, evolves the process |

{{ADVISOR}} does NOT just approve/reject — he actively improves the system based on
what the retro reveals. Action items are HIS responsibility to resolve.

### 2. Enhanced Retrospective Format

**When:** Saturday — after Sprint Review (3:00 PM), before Sprint Planning (4:00 PM)
**Where:** `#specag-dev` (Slack) + saved to `sprints/S-NN/retro.md`
**Who:** ALL team members contribute. PO facilitates. {{ADVISOR}} owns action items.

#### Step 1 — Each team member posts their retro input

**Lead Dev posts:**
```
*Lead Dev — Sprint S-03 Retro*

*What went well:*
  - ROOT-051 push service delivered on time despite API provider change
  - PR review turnaround was <2 hours all week

*What didn't go well:*
  - ROOT-055 retry logic was underestimated (3pt → actually 5pt effort)
  - Blocked for 4 hours waiting on Associate's API contract question

*What can be improved:*
  - Better estimation for error-handling epics (add buffer)
  - Associate should flag blocking questions immediately, not at standup

*Blockers faced:*
  - Anthropic rate limit hit Tuesday 3 PM — switched to DeepSeek, quality was ok
```

**Associate posts:**
```
*Associate — Sprint S-03 Retro*

*What went well:*
  - ROOT-052 and ROOT-053 both completed in same sprint
  - Tech spec grooming on Sunday saved time during coding

*What didn't go well:*
  - ROOT-054 blocked by ROOT-051 API not ready until Wednesday
  - Didn't understand AC-003 clearly — had to rework after PR review

*What can be improved:*
  - Dependency epics should be completed by mid-week, not end-of-week
  - ACs need a 5-minute walkthrough during Sunday kickoff

*Blockers faced:*
  - Dependency on Lead Dev's ROOT-051 (resolved Wed)
```

**PO posts:**
```
*PO Agent — Sprint S-03 Retro*

*What went well:*
  - Sprint goal achieved (push notifications delivered)
  - Zero collision issues — collision guard working perfectly

*What didn't go well:*
  - Underestimated ROOT-055 at planning — should have been 5pt not 3pt
  - Daily report burndown showed "on track" when we were actually behind

*What can be improved:*
  - Re-estimate epics if >20% scope change discovered during grooming
  - Burndown should flag "at risk" when blocking dependencies exist

*Process suggestions:*
  - Add a mid-week check-in (Wednesday) for dependency status
```

**{{ADVISOR}} (Advisor) posts:**
```
*{{ADVISOR}} — Sprint S-03 Retro*

*What went well:*
  - QA was smooth — staging deploys were stable
  - Slack commands (pause/fallback) worked perfectly when needed

*What didn't go well:*
  - QA'd ROOT-051 too late — should have tested Wednesday not Friday
  - Missed the daily report on Thursday (was busy)

*What can be improved:*
  - QA staging within 24 hours of deploy, not end of sprint
  - Set a daily reminder to read PO report

*Action items I'm taking (as Scrum Master):*
  - Will QA within 24 hours of "deployed to staging" Slack message
  - Will update retro template to include mid-week dependency check
```

#### Step 2 — PO compiles the retro summary

```
*Sprint S-03 Retrospective Summary*

*Sprint Goal: Push notifications delivered — ACHIEVED*
*Velocity: 16/19 pts (84%)*

┌─────────────────────────────────────────────┐
│  WHAT WENT WELL                              │
├─────────────────────────────────────────────┤
│  ✓ Sprint goal achieved                      │
│  ✓ Sunday tech spec grooming saved time       │
│  ✓ PR review turnaround <2 hours             │
│  ✓ Collision guard: zero conflicts            │
│  ✓ Slack commands worked for fallback         │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  WHAT CAN BE IMPROVED                        │
├─────────────────────────────────────────────┤
│  △ Estimation accuracy for error-handling     │
│  △ Dependency epics should complete mid-week  │
│  △ ACs need walkthrough at Sunday kickoff      │
│  △ {{ADVISOR}} QA within 24 hours of deploy         │
│  △ Burndown should flag dependency risks      │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  ACTION ITEMS ({{ADVISOR}} owns as Scrum Master)   │
├─────────────────────────────────────────────┤
│  [AI-001] Add dependency check to Wed standup │
│    Owner: {{ADVISOR}} | Due: Sprint S-04 Day 1      │
│    Status: NEW                                │
│                                               │
│  [AI-002] Add AC walkthrough to Mon kickoff   │
│    Owner: {{ADVISOR}} | Due: Sprint S-04 Day 1      │
│    Status: NEW                                │
│                                               │
│  [AI-003] QA within 24hr of staging deploy    │
│    Owner: {{ADVISOR}} | Due: Ongoing                │
│    Status: NEW                                │
│                                               │
│  [AI-004] Burndown: flag "at risk" when       │
│    dependency exists and blocker unresolved    │
│    Owner: {{ADVISOR}} → PO implements | Due: S-04   │
│    Status: NEW                                │
└─────────────────────────────────────────────┘

Previous sprint action items:
  [AI-prev-001] Reduce standup verbosity — DONE (applied in S-03)
  [AI-prev-002] Add token usage to daily report — DONE
```

### 3. Action Item Tracking

Action items persist across sprints until resolved. Tracked in `sprints/action-items.md`.

```markdown
# Action Items — Running Tracker
# Owner: {{ADVISOR}} (Scrum Master)
# Updated: every retro

| ID | Action | Owner | Created | Due | Status |
|---|---|---|---|---|---|
| AI-001 | Add dependency check to Wed standup | {{ADVISOR}} | S-03 | S-04 Day 1 | NEW |
| AI-002 | Add AC walkthrough to Mon kickoff | {{ADVISOR}} | S-03 | S-04 Day 1 | NEW |
| AI-003 | QA within 24hr of staging deploy | {{ADVISOR}} | S-03 | Ongoing | NEW |
| AI-004 | Burndown flags dependency risks | {{ADVISOR}}→PO | S-03 | S-04 | NEW |
| AI-prev-001 | Reduce standup verbosity | {{ADVISOR}} | S-02 | S-03 | DONE |
| AI-prev-002 | Add token usage to daily report | PO | S-02 | S-03 | DONE |
```

**Rules:**
- {{ADVISOR}} owns ALL action items (as Scrum Master)
- {{ADVISOR}} can delegate implementation (e.g., "PO implements burndown change")
- Action items are reviewed at the START of every retro (what was done, what's still open)
- If an action item is open for 3+ sprints, it's escalated in the retro as a recurring problem
- Action items that change Agile methodology are applied by updating the Project Bible + relevant spec

### 4. Continuous Methodology Evolution

{{ADVISOR}} has the authority to evolve the Agile methodology at any time. Changes flow:

```
Retro finding → Action item → {{ADVISOR}} decides change
  → Update Project Bible (source of truth)
  → Update relevant spec (PLAT-006, coding-standards, etc.)
  → PO announces change in next Sprint Planning
  → Team follows updated process from next sprint onward
```

**What {{ADVISOR}} can change:**
- Ceremony timing, format, or frequency
- Story point rules or capacity calculations
- Definition of Ready / Definition of Done
- Work block schedules
- Epic category rules
- Any process described in the Project Bible

**What requires team feedback first:**
- Changes that affect developer productivity (work hours, token caps)
- Changes to PR review process
- Changes to testing requirements

### 5. Blameless Retros & Vegas Rule

The retro is the team's safety valve. It only works if people speak honestly,
which only happens if speaking honestly is safe. Two non-negotiable rules:

**Blameless Rule — focus on the system, not the person.**
- Post-mortems and retro notes cite ROLES (Lead Dev, PO, Associate), never
  individual humans, even when only one human exists.
- "The Lead Dev role missed the dependency" — OK.
- "{{ADVISOR}} missed the dependency" — NOT OK in written retro artifacts.
- Action items address process gaps ("add a Wednesday dependency check"),
  never assign blame ("X needs to pay more attention").
- If a recurring problem traces to one role, the fix is a process change
  (a checklist, a hook, a ceremony), not a personal call-out.
- This applies even when {{ADVISOR}} is the only human. Future contributors will
  read these retros — keep them blameless from day one.

**Vegas Rule — what's said in retro stays in retro.**
- Discussion content during the retro window (gripes, frustrations, half-formed
  ideas, "this is annoying" comments) is NOT quoted outside `#specag-dev` retro
  context. Not in standups, not in PRs, not in Slack DMs to {{ADVISOR}} later.
- The WRITTEN retro summary (what-went-well, what-improved, action items) IS
  public — it goes into `sprints/S-NN/retro.md` and is part of the audit trail.
- The distinction: action items are public, raw venting is not.
- This is what makes it safe to say "I think we're moving too fast" or "I'm
  not sure this approach is working" without it becoming a permanent record.
- If a piece of raw retro discussion needs to escalate (e.g., a blocker
  surfaced during venting), it gets re-raised as a formal item with consent
  from whoever raised it — not quoted from the retro chat log.

**What this is NOT:**
- Not a gag order. Action items, decisions, and metrics are fully public.
- Not a way to hide problems. Anything actionable surfaces in the written summary.
- Not optional during PC-01. We dogfood blameless retros from S00 onward.

### 6. Velocity Tracking — `sprints/velocity.json`

Velocity is a planning aid, NOT a performance metric. We track it to forecast
sprint capacity, never to grade individuals or compare sprints competitively.

**File:** `sprints/velocity.json` — append-only, written by PO at retro time.

```json
{
  "sprints": [
    {
      "sprint_id": "S00",
      "pc": 1,
      "planned_points": 18,
      "completed_points": 16,
      "rolled_over_points": 2,
      "cancelled": false,
      "notes": "VPS bring-up; Anthropic outage cost ~3 hours"
    },
    {
      "sprint_id": "S01",
      "pc": 1,
      "planned_points": 21,
      "completed_points": 20,
      "rolled_over_points": 1,
      "cancelled": false,
      "notes": null
    }
  ],
  "rolling_average_5": 18.0,
  "last_updated": "2026-04-25T15:30:00-05:00"
}
```

**Rules:**
- PO appends one entry per sprint at retro close — never edits prior entries.
- `rolling_average_5` = mean of `completed_points` for the last 5 NON-CANCELLED sprints.
- Cancelled sprints (per PLAT-013) are recorded with `cancelled: true` but EXCLUDED from the rolling average — a cancelled sprint is not a velocity data point.
- The first 5 sprints have no meaningful average; PO uses raw history instead and labels forecasts as "low confidence" until 5 non-cancelled sprints exist.
- Velocity is reported in retros and at Saturday Planning. It is NEVER used in standups, daily reports, or performance comparisons across team members.
- Velocity changes by >25% sprint-over-sprint trigger an estimation calibration review (see §8).

### 7. PC-Level Burndown — `year-{year}/PC-{pc}/burndown.md`

Each Cycle (PC) gets a burndown file that tracks total scope vs. completed
scope at the PC level. PO updates it every Saturday at retro close.

**File:** `year-2026/PC-01/burndown.md`

```markdown
# PC-01 Burndown — Platform Scaffolding & Discovery

| Sprint | Total Scope (pts) | Completed (cum) | Remaining | Added Mid-PC | Notes |
|---|---|---|---|---|---|
| S00 end | 95 | 16 | 79 | 0 | Baseline scope from PC-01 manifest |
| S01 end | 95 | 36 | 59 | 0 | On track |
| S02 end | 103 | 54 | 49 | +8 | Added PLAT-013 (sprint cancellation) mid-PC |
| S03 end | 103 | 72 | 31 | 0 | Burndown ahead of trendline |
| S04 end | 103 | — | — | — | Pending |
| S05 end | 103 | — | — | — | PC-01 close target |

## Forecast vs. Actual
- Linear trendline (S00→S05): **15.8 pts/sprint required** to close PC-01
- Actual rolling avg (5-sprint): **18.0 pts/sprint** — on track with buffer
- Forecast PC close: **S05 with ~5 pts cushion**

## Scope Changes Mid-PC
- 2026-04-25 (S02): Added PLAT-013 sprint cancellation spec (+8 pts) — reason: surfaced as gap in PC-01 audit
- (track every scope addition; mid-PC removals also tracked)

## Risks to Burndown
- S04 blocked_by: {{ADVISOR}} project documentation delivery (cascading SLA active if T+1)
- DeepSeek quota saturation could downgrade to emergency tier (slower output)
```

**Rules:**
- PO updates the burndown table at every Saturday retro close.
- "Total Scope" includes ALL approved epics in the PC manifest as of that Saturday — both original and any added mid-PC.
- "Added Mid-PC" column makes scope changes visible. PO is required to log a one-line reason for every addition.
- Forecast line ("on track" / "at risk" / "behind") goes into the daily report on Sundays.
- A burndown that shows "behind" for 2 consecutive sprints triggers a mid-PC re-plan conversation in `#specag-planning` — {{ADVISOR}} decides to descope, extend, or accept.
- Burndown is forecast, not contract. The point is to surface drift early, not to lock in commitments.

### 8. Estimation Calibration — `sprints/estimation-log.md`

We don't grade estimates as right or wrong. We TRACK them to learn where we
systematically over- or under-estimate, and adjust our planning accordingly.

**File:** `sprints/estimation-log.md` — append-only, written by PO at epic close.

```markdown
# Estimation Calibration Log
# Owner: PO Agent | Reviewed: every retro
# Purpose: surface systematic estimation drift, not grade individuals

| Epic | Category | Estimated | Actual | Drift % | Notes |
|---|---|---|---|---|---|
| PLAT-001 | Story | 5 | 5 | 0% | — |
| PLAT-002 | Story | 3 | 5 | +67% | Fallback chain edge cases under-scoped |
| PLAT-008 | Story | 3 | 3 | 0% | — |
| PLAT-013 | Story | 2 | 3 | +50% | Drill scenarios took longer than expected |
| BLOCK-001 | Blocker | 1 | 1 | 0% | — |
| ROOT-055 | Story | 3 | 5 | +67% | Retry logic underestimated |
```

**Rules:**
- PO logs every closed epic — estimated vs actual story points — at the moment {{ADVISOR}} accepts the epic.
- Drift % = `(actual - estimated) / estimated × 100`. Negative means we over-estimated.
- At retro, PO computes the **median absolute drift** for the last sprint and reports it: "Median estimation drift this sprint: 12% (target: <25%)."
- If median absolute drift exceeds **25%** in any single sprint, the retro MUST include a calibration discussion: which category (Story, Tech Maintenance, Blocker, etc.) is drifting, and what about the estimation process needs to change.
- If a category drifts >25% for 2 consecutive sprints, PO updates the story-point definitions in `agent.limits.yaml` (e.g., "for error-handling-heavy stories, add +1 pt buffer at planning").
- This log is NEVER used to grade an individual agent or human. It's a property of the team's planning process, not anyone's performance.

### 9. Retro Health Metrics (tracked over time)

PO tracks these sprint-over-sprint to measure improvement:

| Metric | How measured | Goal |
|---|---|---|
| Velocity trend | Points completed per sprint (trailing 5) | Stable or improving |
| Estimation accuracy | Planned pts vs completed pts (%) | ≥85% |
| Rollover rate | Rolled-over pts / planned pts (%) | ≤15% |
| Blocker frequency | Blockers reported per sprint | Decreasing |
| Action item closure | % of action items closed within 2 sprints | ≥80% |
| [skip-spec] usage | Times used per sprint | ≤3 |
| Fallback events | Times Tier 2/3 was needed per sprint | Decreasing |
| QA turnaround | Hours between staging deploy and {{ADVISOR}} QA | ≤24 hours |

### Files Touched
- `sprints/S-NN/retro.md` — per-sprint retro (enhanced format)
- `sprints/action-items.md` — running action item tracker (persists across sprints)
- `sprints/velocity.json` — append-only velocity history (PO writes at retro close)
- `sprints/estimation-log.md` — estimated vs actual points per epic (PO writes at epic close)
- `year-{year}/PC-{pc}/burndown.md` — PC-level burndown table (PO writes weekly)
- `/app/agents/sprint_retro.py` — retro facilitation script
- `specag_project_bible.md` — updated when methodology changes

## [STANDARDS]
- Every retro MUST have input from ALL team members (Lead Dev, Associate, PO, {{ADVISOR}})
- Retros are BLAMELESS — written artifacts cite roles, never individuals; action items address process gaps, never assign personal blame
- Vegas Rule — raw retro discussion is not quoted outside the retro; only the written summary and action items are public
- Action items MUST have an owner, due date, and status
- Action items are reviewed at the START of every retro
- Methodology changes MUST be documented in Project Bible + relevant spec
- Velocity is tracked in `sprints/velocity.json` as a planning aid only — NEVER used to grade individuals or compare team members
- Cancelled sprints are recorded but EXCLUDED from the rolling velocity average
- PC-level burndown updated every Saturday at retro close; "behind" for 2 consecutive sprints triggers a mid-PC re-plan
- Estimation drift logged per epic; median absolute drift >25% in a sprint MUST trigger a calibration discussion in the retro
- Retro health metrics tracked by PO sprint-over-sprint

## [ACCEPTANCE CRITERIA]
```
AC-001: Given it is Saturday retro time, when each agent posts their input, then
        the retro contains what-went-well, what-didn't, what-can-improve, and
        blockers from every team member.

AC-002: Given PO compiles the retro summary, then it includes action items with
        owner ({{ADVISOR}}), due date, and status.

AC-003: Given action item AI-001 was created in Sprint S-03, when Sprint S-04
        retro starts, then AI-001 status is reviewed (done/in-progress/open).

AC-004: Given an action item has been open for 3+ sprints, then PO flags it
        as "recurring problem" in the retro summary.

AC-005: Given {{ADVISOR}} decides to change a methodology rule (e.g., add Wednesday
        check-in), then Project Bible and relevant spec are updated before
        the next sprint starts.

AC-006: Given PO tracks retro health metrics, then sprint-over-sprint trends
        are included in the weekly cost report.

AC-007: Given a written retro summary or post-mortem is produced, when PO
        compiles it, then it cites only ROLES (Lead Dev, PO, Associate, Advisor)
        and contains no personal call-outs by name.

AC-008: Given a sprint closes, when PO writes the retro, then a new entry is
        appended to `sprints/velocity.json` with planned, completed, rolled-over,
        and cancelled fields, and the rolling 5-sprint average is recomputed
        excluding any cancelled sprints.

AC-009: Given a sprint is cancelled per PLAT-013, when PO appends its velocity
        entry, then `cancelled: true` is set and the sprint is NOT included in
        the rolling average.

AC-010: Given Saturday retro close, when PO updates `year-{year}/PC-{pc}/burndown.md`,
        then the table contains a row for that sprint with cumulative completed
        points, remaining points, and any mid-PC scope additions logged with reason.

AC-011: Given the PC burndown shows "behind" for 2 consecutive sprints, when
        the second sprint closes, then PO opens a mid-PC re-plan thread in
        `#specag-planning` and tags {{ADVISOR}} for a descope/extend/accept decision.

AC-012: Given an epic is accepted by {{ADVISOR}}, when PO closes it, then a row is
        appended to `sprints/estimation-log.md` with estimated vs actual points
        and computed drift %.

AC-013: Given the median absolute estimation drift for a sprint exceeds 25%,
        when the retro runs, then PO flags it and the retro summary includes
        a calibration discussion with at least one concrete action item.

AC-014: Given a category drifts >25% for 2 consecutive sprints, when PO detects
        it, then PO updates the story-point definitions in `agent.limits.yaml`
        before the next Sprint Planning.
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created
- 2026-04-11: Added §5 Blameless Retros & Vegas Rule (G-05, G-13). Added §6 velocity tracking via `sprints/velocity.json` with cancelled-sprint exclusion (G-08). Added §7 PC-level burndown via `year-{year}/PC-{pc}/burndown.md` with mid-PC re-plan trigger (G-09). Added §8 estimation calibration log with 25% drift threshold (G-10). Renumbered Retro Health Metrics to §9. Added STANDARDS for blameless/Vegas/velocity/burndown/estimation. Added AC-007..AC-014.
