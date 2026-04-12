# PLAT-006: Sprint Ceremonies, Story Points & Work Schedules

## [SUMMARY]
- App: SpecAg
- Epic owner: PO Agent (facilitation), {{ADVISOR}} (participation)
- Status: BACKLOG
- Sprint: PC-01 Sprint 1
- Related specs: All — this governs how every sprint operates
- Priority: S1 — defines the core Agile rhythm of the entire system

## [STORY]
As {{ADVISOR}} (Advisor), I need structured Agile ceremonies — sprint planning, daily standup,
kickoff, sprint review, and retro — so the team operates with clarity, predictability,
and full Scrum compliance. Every agent and human knows what to do, when, and how much.

## [TECH SPEC]

### 1. Work Schedules

#### AI Agents — 5 hours/day effective work
```
Work pattern: 1 hour ON → 3 hours BREAK → repeat
Total effective work: 5 hours/day
Purpose of break: token budget pacing, avoids burst exhaustion

Daily schedule (CST):
  08:00–09:00  Work block 1 (1 hour)
  09:00–12:00  Break (3 hours) — no API calls, no commits
  12:00–13:00  Work block 2 (1 hour)
  13:00–16:00  Break (3 hours)
  16:00–17:00  Work block 3 (1 hour)
  17:00–20:00  Break (3 hours)
  20:00–21:00  Work block 4 (1 hour)
  21:00–22:00  Work block 5 (1 hour) — final block, wrap-up
  22:00        Work window closes

Total: 5 work hours across 14-hour window
```

#### Human Agent ({{ADVISOR}}, or future human devs) — 6 hours/day
```
Flexible schedule — no enforced blocks
Available: up to 6 hours/day when participating as developer
Primary role remains Advisor (decision gates only)
When acting as developer: follows same epic flow as AI agents
```

#### Work Hours Per Sprint (1 week = Saturday to Friday, 7 days)
| Agent Type | Hours/Day | Work Days/Sprint | Hours/Sprint |
|---|---|---|---|
| AI Agent | 5 | 7 (all days, Sat–Fri) | 35 hours |
| Human Agent | 6 | flexible (weekends for ceremonies) | 30 hours |

**Note:** AI agents work ALL 7 days of the sprint. {{ADVISOR}} participates on weekends
for major ceremonies (review, retro, planning, kickoff).

---

### 2. Story Points System

#### Point Scale
| Points | AI Agent Time | Human Agent Time | Complexity |
|---|---|---|---|
| 1 | ~1 hour | ~2-3 hours | Trivial — config change, copy fix, small bug |
| 2 | ~2 hours | ~4-6 hours (half day) | Small — single endpoint, simple UI component |
| 3 | ~3 hours | ~1 day (6 hours) | Medium — feature with tests, multi-file change |
| 5 | ~5 hours (1 full day) | ~2 days (12 hours) | Large — full feature end-to-end with tests + deploy |

#### Hard Rules
- **Maximum 5 points per epic** — no exceptions
- If an epic estimates >5 points → PO MUST split it into multiple epics
- Each sub-epic must be independently deliverable (has its own AC, can be demoed)
- Story points include the FULL lifecycle:
  ```
  1. Technical grooming (Monday kickoff)
  2. Technical spec creation/update
  3. Code implementation
  4. Unit + integration tests
  5. PR + code review
  6. Deployment to staging
  7. Demo to PO
  8. Acceptance check
  9. Move to DONE
  ```
- If any step is incomplete, the epic is NOT done

#### Velocity Tracking
```
Sprint velocity = sum of story points COMPLETED (accepted by {{ADVISOR}})
Rolled-over epics do NOT count toward velocity

Example:
  Sprint S-03: Planned 18 pts → Completed 15 pts → Rolled over 3 pts
  Velocity: 15

Trailing 3-sprint average used for next sprint loading:
  S-01: 14, S-02: 16, S-03: 15 → Average: 15 → Load S-04 with ~15 pts
```

#### Capacity Per Sprint (7-day sprint)
| Agent | Max Points/Sprint | Rationale |
|---|---|---|
| Lead Dev (AI) | ~21 pts | 35 work hours / mix of 3pt and 5pt epics |
| Associate (AI) | ~21 pts | 35 work hours / feature-focused epics |
| Human (if active) | ~15 pts | 30 work hours / 5pt = 2 days, 3pt = 1 day |
| **Team total** | **~42-57 pts** | Depending on who's active |

---

### 3. Sprint Ceremonies

#### 3.1 Sprint Planning (Saturday — end of sprint)

| Field | Value |
|---|---|
| When | Saturday 4:00 PM CST (last day of current sprint) |
| Where | Slack `#specag-planning` channel |
| Who | PO (facilitates), Lead Dev, {{ADVISOR}} |
| Duration | ~30-45 minutes (async Slack, not a call) |
| Output | Sprint forecast set, epics assigned, sprint goal agreed |

**Flow:**
```
Step 1 — PO prepares (before the meeting)
  • PO reviews single backlog, selects candidate epics for next sprint
  • PO writes business spec for each candidate epic
  • PO proposes sprint goal (1 sentence)
  • PO posts to #specag-planning:

    "*Sprint S-04 Planning — PC-01*
    
    *Sprint Goal:* Push notifications delivered on iOS and Android
    
    *Proposed Backlog:*
    | Epic | Title | Points | Proposed Owner | Business Spec |
    |------|-------|--------|----------------|---------------|
    | ROOT-051 | Push notification service | 5 | Lead Dev | [link] |
    | ROOT-052 | iOS push integration | 3 | Associate | [link] |
    | ROOT-053 | Android push integration | 3 | Associate | [link] |
    | ROOT-054 | Push notification settings UI | 3 | Associate | [link] |
    | ROOT-055 | Push retry + failure handling | 5 | Lead Dev | [link] |
    | ROOT-056 | Notification history screen | 3 | Lead Dev | [link] |
    
    *Total: 22 pts (Lead Dev: 13, Associate: 9)*
    *Trailing velocity: 15 pts/sprint*
    
    @lead-dev @datta — Please review and confirm."

Step 2 — Lead Dev reviews
  • Checks technical feasibility
  • Flags if any epic is >5 pts and needs splitting
  • Flags dependency order (e.g., ROOT-051 must finish before ROOT-052)
  • Confirms or suggests reassignment
  • Posts response in #specag-planning

Step 3 — {{ADVISOR}} reviews
  • Confirms sprint goal aligns with PC MVP
  • Approves or adjusts epic selection
  • Posts: "Approved" or "Move ROOT-056 to next sprint, focus on push delivery"

Step 4 — PO finalizes
  • Updates INDEX.md with assignments
  • Creates spec skeletons for new epics
  • Posts final sprint forecast:
    "Sprint S-04 forecast set. Goal: Push notifications delivered. 19 pts loaded.
     (Forecast, not a commitment — we'll re-plan if reality diverges.)"
```

#### 3.2 Sunday Kickoff / Technical Grooming

| Field | Value |
|---|---|
| When | Sunday 10:00–11:00 AM CST (sprint start) |
| Where | Slack `#specag-planning` channel |
| Who | Lead Dev, Associate, PO, {{ADVISOR}} |
| Duration | ≤1 hour |
| Output | Technical specs ready for all assigned epics |

**Flow:**
```
Step 1 — Each agent reads their assigned epics' business spec (written by PO on Saturday)

Step 2 — Each agent writes/updates the technical spec:
  • [TECH SPEC] section: endpoints, DB changes, files touched, dependencies
  • Posts to #specag-planning: "ROOT-051 tech spec ready for review"

Step 3 — Lead Dev reviews ALL tech specs (own + Associate's)
  • Checks for architecture alignment
  • Checks for collision (files touched overlap)
  • Approves or requests changes
  • Posts: "ROOT-051 tech spec approved" or "ROOT-052: change DB schema approach, see comment"

Step 4 — PO approves business alignment
  • Confirms tech spec serves the business spec / acceptance criteria
  • Posts: "All tech specs approved. Sprint S-04 kickoff complete."

Step 5 — Agents begin coding (second work block onward)
```

**Rule:** No agent writes code until their tech spec is approved by Lead Dev AND PO.

#### 3.3 Daily Standup

| Field | Value |
|---|---|
| When | Every day 08:05 CST (7 days/week) |
| Where | Slack `#specag-dev` |
| Who | All agents post, {{ADVISOR}} reads |
| Duration | Auto-posted, <1 minute to read |

**Format (each agent posts):**
```
*Lead Dev — Daily Standup*
  Yesterday: ROOT-051 push service — 80% complete, API + tests done
  Today: ROOT-051 deployment + demo. Start ROOT-055 grooming
  Blockers: None
  Hours worked yesterday: 5/5

*Associate — Daily Standup*
  Yesterday: ROOT-052 iOS push — PR raised
  Today: Address review feedback, start ROOT-053 Android push
  Blockers: Waiting on ROOT-051 API contract (Lead Dev, ETA today)
  Hours worked yesterday: 5/5
```

**PO posts summary after agents:**
```
*PO Standup Summary*
  Sprint S-04 | Day 2 of 5 | Goal: Push notifications delivered
  Burndown: 19 pts planned → 14 pts remaining → ON TRACK
  Blockers: 1 (ROOT-052 waiting on ROOT-051 — resolves today)
  Token budget: Anthropic 32% daily / OpenAI 45% daily
```

#### 3.4 Daily Report (end of day)

| Field | Value |
|---|---|
| When | Every day 6:00 PM CST (7 days/week) |
| Where | Slack `#specag-dev` |
| Who | PO posts |
| Format | Existing format from Project Bible Section 13 |

**Updated to include burndown:**
```
*PO Daily Report — Tuesday, Apr 15*

*Sprint S-04 | PC-01 | Day 2 of 5*
*Sprint Goal: Push notifications delivered on iOS and Android*

*Burndown:*
  Day 1: ██████████████████░░ 19 pts → 14 remaining
  Day 2: ████████████░░░░░░░░ 14 pts → 9 remaining  ← ON TRACK

*Completed today:*
  - ROOT-051 (Push service, 5pts): MERGED + deployed to staging

*In progress:*
  - ROOT-052 (iOS push, 3pts): ~60% — Associate
  - ROOT-055 (Push retry, 5pts): ~20% — Lead Dev, started today

*Token budget:*
  Anthropic: 52% daily / 41% weekly
  OpenAI: 68% daily / 55% weekly

*{{ADVISOR}} action needed:*
  - QA ROOT-051 on staging: specag-staging.app/api/push
```

#### 3.5 Sprint Review (Saturday 3:00 PM — before Planning)

| Field | Value |
|---|---|
| When | Saturday 3:00 PM CST (last day of sprint) |
| Where | Slack `#specag-dev` |
| Who | PO presents, {{ADVISOR}} reviews |
| Duration | ~15 minutes to read |

**Format:**
```
*Sprint S-04 Review — PC-01*

*Sprint Goal: Push notifications delivered on iOS and Android*
*Goal Status: ACHIEVED*

*Completed Epics:*
| Epic | Title | Points | Owner | Demo Link |
|------|-------|--------|-------|-----------|
| ROOT-051 | Push notification service | 5 | Lead Dev | staging.app/api/push |
| ROOT-052 | iOS push integration | 3 | Associate | TestFlight build 42 |
| ROOT-053 | Android push integration | 3 | Associate | Internal track 42 |
| ROOT-055 | Push retry + failure handling | 5 | Lead Dev | staging.app/api/push |

*Rolled Over:*
| Epic | Title | Points | Reason | New Sprint |
|------|-------|--------|--------|------------|
| ROOT-054 | Push settings UI | 3 | Blocked by ROOT-051 late merge | S-05 |

*Velocity:*
  Planned: 19 pts | Completed: 16 pts | Rolled: 3 pts
  Velocity this sprint: 16
  Trailing 3-sprint avg: 15.3

*{{ADVISOR}}: Please review completed epics and issue green flags.*
```

#### 3.6.5 Backlog Refinement (Async — continuous)

| Field | Value |
|---|---|
| When | Continuous, async — PO posts a refinement batch every Wednesday 14:00 CST |
| Where | Slack `#specag-planning` thread per batch |
| Who | PO drives, Lead Dev + Associate respond async, {{ADVISOR}} reads |
| Duration | No meeting — async responses by Thursday 12:00 CST |
| Output | Backlog epics groomed, sized, and READY (per DoR §31) for the next 1–2 sprints |

**Why async, not a sync meeting:**
The team is global-async by default — {{ADVISOR}} is the only human, agents work
across all 7 days, and pulling everyone into a sync ceremony for backlog talk
burns calendar time and tokens for low-bandwidth work. Refinement is mostly
reading and short comments — perfect for async. We sync ONLY when a thread
stalls or genuinely needs a discussion (escalated to Saturday Planning).

**Flow:**
```
Step 1 — Wednesday 14:00 CST: PO posts a refinement batch to #specag-planning
  • PO selects 4–8 backlog epics that are likely to enter the next 1–2 sprints
  • For each, PO posts a thread with: business spec link, current size, open questions
  • PO tags @lead-dev and @associate with specific questions (not blanket pings)

Step 2 — Wednesday 14:00 → Thursday 12:00 CST: Async responses
  • Lead Dev / Associate reply in-thread with: tech feasibility, sizing pushback,
    splitting suggestions, dependency notes, DoR gaps
  • Replies happen during normal work blocks — no extra ceremony time required
  • If a thread surfaces a real disagreement, anyone can escalate it with
    `escalate to planning` and it becomes a Saturday Planning agenda item

Step 3 — Thursday 12:00 CST: PO closes the batch
  • PO updates each epic with new size, splits, or DoR additions
  • PO marks epics that hit DoR as `ready: true` in the spec frontmatter
  • PO posts a one-line summary: "Refinement batch closed. 6/8 epics now READY for S-NN+1."

Step 4 — Saturday Planning consumes only READY epics
  • At Saturday Planning, PO proposes only epics that passed refinement and are READY
  • Non-READY epics stay in the backlog until a future refinement batch lifts them
```

**Rules:**
- Refinement is ASYNC by default. Sync conversation is the exception, triggered by `escalate to planning`.
- No epic enters a sprint at Saturday Planning unless it has been through at least one refinement batch and meets DoR (Bible §31).
- PO MUST run a refinement batch every Wednesday — even a small one — so the backlog never goes more than 7 days without grooming attention.
- Refinement threads count as work blocks for token tracking — same hooks, same caps, same logging.
- Refinement is NOT a place for blocker resolution. Blockers go to the Blocker epic flow (PLAT-008), not refinement threads.

#### 3.7 Sprint Retrospective (Saturday — after Review, before Planning)

| Field | Value |
|---|---|
| When | Saturday 3:30 PM CST (after Review) |
| Where | Saved to `sprints/S-NN/retro.md` + posted to `#specag-dev` |
| Who | PO facilitates, all agents contribute, {{ADVISOR}} participates |
| Duration | Auto-generated |

**Saturday afternoon sequence:**
```
3:00 PM  Sprint Review (PO posts, {{ADVISOR}} reviews)
3:30 PM  Sprint Retro (all team members post, {{ADVISOR}} owns action items)
4:00 PM  Sprint Planning for next sprint (PO facilitates, {{ADVISOR}} approves)
5:00 PM  Sprint officially ends
```

**Sunday morning:**
```
10:00 AM  Sunday Kickoff — tech spec grooming ({{ADVISOR}} participates)
11:00 AM  Grooming complete — agents begin coding Monday
```

---

### 4. Slack Channels

| Channel | Purpose | Who posts |
|---|---|---|
| `#specag-dev` | Daily standups, daily reports, sprint reviews, retros, alerts | All agents, {{ADVISOR}} reads |
| `#specag-planning` | Sprint planning, kickoff, tech spec reviews, epic discussions | PO, Lead Dev, {{ADVISOR}} |

---

### 5. Single Backlog Rule

- There is ONE backlog for the entire project — stored in `specs/backlog/`
- PO is the sole owner of the backlog
- Epics are pulled FROM the backlog INTO a sprint ONLY during Sprint Planning (Saturday)
- Mid-sprint additions are only allowed for S1 (prod bugs) and S2 (blocking) via interrupt slots
- No agent may self-assign from the backlog
- Backlog is groomed continuously by PO (severity re-evaluation every Monday)

```
Single Backlog
  ↓ Sprint Planning (Friday)
Sprint Backlog (forecast)
  ↓ Monday Kickoff (tech spec grooming)
In Development
  ↓ PR + Review + Deploy
Demo / QA
  ↓ {{ADVISOR}} green flag
DONE
```

---

### 6. Epic Lifecycle (Full)

```
Saturday (Sprint close — {{ADVISOR}}'s ceremony day):
  3:00 PM  Sprint Review (PO presents, {{ADVISOR}} reviews + green flags)
  3:30 PM  Sprint Retro (all team, {{ADVISOR}} owns action items)
  4:00 PM  Sprint Planning for next sprint (PO facilitates, {{ADVISOR}} approves)
  PO assigns epics, writes business specs, updates INDEX.md
  Unfinished epics → rollover protocol

Sunday (Kickoff — {{ADVISOR}}'s grooming day):
  10:00 AM  Tech spec grooming
  Agent reads business spec → writes technical spec (≤1 hour)
  Lead Dev reviews + approves tech spec
  {{ADVISOR}} participates in grooming, approves direction
  Status: READY FOR DEV

Sun–Fri (Development — all 7 days):
  Agent codes according to tech spec + coding standards
  Agent writes tests
  Agent raises PR (must reference epic, update spec changelog)
  Lead Dev reviews PR
  Agent addresses feedback
  PR merged → auto-deploy to staging
  Status: IN REVIEW → MERGED

Thu–Fri (Demo + Acceptance):
  PO runs demo script against staging
  Status: DEMO_PASSED or DEMO_FAILED (bug sub-task created)
  {{ADVISOR}} QA on staging (web + mobile)
  {{ADVISOR}} issues green flag
  Status: ACCEPTED → DONE
  PO moves spec to finished/
```

---

### 7. Cron Schedule for Ceremonies

```bash
# Sunday Kickoff reminder (sprint start)
0 10 * * 0    /app/venv/bin/python /app/agents/kickoff_reminder.py

# Daily standup (every day — 7 days/week)
5 8 * * *     /app/venv/bin/python /app/agents/daily_standup.py

# Daily report (every day — 7 days/week)
0 18 * * *    /app/venv/bin/python /app/agents/po_daily_report.py

# Saturday ceremonies (Sprint Review → Retro → Planning)
0 15 * * 6    /app/venv/bin/python /app/agents/sprint_review.py
30 15 * * 6   /app/venv/bin/python /app/agents/sprint_retro.py
0 16 * * 6    /app/venv/bin/python /app/agents/sprint_planning.py

# Work block enforcement (AI agents — every day, 7 days/week)
0 9 * * *     /app/venv/bin/python /app/agents/work_block_pause.py   # block 1 ends
0 12 * * *    /app/venv/bin/python /app/agents/work_block_resume.py  # block 2 starts
0 13 * * *    /app/venv/bin/python /app/agents/work_block_pause.py   # block 2 ends
0 16 * * *    /app/venv/bin/python /app/agents/work_block_resume.py  # block 3 starts
0 17 * * *    /app/venv/bin/python /app/agents/work_block_pause.py   # block 3 ends
0 20 * * *    /app/venv/bin/python /app/agents/work_block_resume.py  # block 4 starts
0 21 * * *    /app/venv/bin/python /app/agents/work_block_resume.py  # block 5 starts (continuous)
0 22 * * *    /app/venv/bin/python /app/agents/work_window_close.py  # day ends
```

### Files Touched
- `/app/agents/sprint_planning.py` — Friday planning facilitation
- `/app/agents/kickoff_reminder.py` — Monday kickoff trigger
- `/app/agents/daily_standup.py` — Morning standup posts
- `/app/agents/sprint_review.py` — Friday sprint review generation
- `/app/agents/sprint_retro.py` — Friday retro generation
- `/app/agents/work_block_pause.py` — Pause agents during break periods
- `/app/agents/work_block_resume.py` — Resume agents for work blocks
- `/app/config/agent_limits.yaml` — work block schedules
- `#specag-planning` Slack channel — new channel for planning + kickoff

## [STANDARDS]
- No code is written until tech spec is approved by Lead Dev AND PO
- No epic exceeds 5 story points — PO must split if estimated >5
- Story points include full lifecycle (groom → code → test → deploy → demo → done)
- Sprint Planning happens EVERY Saturday — no exceptions, no skipping
- Sunday Kickoff grooming takes ≤1 hour per agent
- Single backlog — PO is sole owner, epics enter sprint only via Saturday planning
- Velocity is tracked per sprint and used for future sprint loading
- Work blocks enforced — AI agents do NOT make API calls during break periods

## [ACCEPTANCE CRITERIA]
```
AC-001: Given it is Saturday 4:00 PM, when sprint_planning.py runs, then PO posts
        the next sprint's proposed backlog to #specag-planning with sprint goal,
        epic list, points, and owners.

AC-002: Given it is Sunday 10:00 AM, when kickoff_reminder.py runs, then each agent
        receives a reminder to groom their assigned epics and write tech specs.

AC-003: Given an agent completes tech spec grooming, when Lead Dev reviews it,
        then approval/rejection is posted to #specag-planning within the Sunday
        10:00-11:00 grooming window.

AC-004: Given an epic is estimated at 7 points, when PO tries to add it to sprint,
        then PO must split it into two epics (e.g., 5+2 or 3+4) before assignment.

AC-005: Given it is 09:00 CST (end of work block 1), when work_block_pause.py runs,
        then all AI agents are paused until 12:00 CST (next work block).

AC-006: Given it is Saturday 3:00 PM, when sprint_review.py runs, then a formatted
        review with completed epics, velocity, and burndown is posted to #specag-dev.

AC-007: Given daily standup runs at 08:05, then each agent posts yesterday/today/blockers
        and PO posts burndown summary within 5 minutes.

AC-008: Given Sprint S-03 had velocity 15, S-02 had 14, S-01 had 16, when PO loads
        Sprint S-04, then total points loaded is approximately 15 (trailing average).
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created — full Agile ceremony suite, story points, work schedules
