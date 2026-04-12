# PLAT-008: Epic Categorization System

## [SUMMARY]
- App: Rootine
- Epic owner: PO Agent (categorizes), Lead Dev (validates)
- Status: BACKLOG
- Sprint: PC-01 Sprint 1
- Related specs: PLAT-006 (ceremonies), PLAT-005 (traceability)
- Priority: S2 — defines how all work is classified

## [STORY]
As a team, we need a clear categorization system for epics so that every piece of work
is typed correctly — enabling accurate velocity tracking, sprint loading, and reporting.
Different epic types have different rules for estimation, ownership, and due dates.

## [TECH SPEC]

### Epic Categories

#### 1. Task
> **Coding-required work. The most common type.**

| Field | Value |
|---|---|
| Label | `task` |
| What it is | An implementable unit of work requiring code changes |
| Examples | "Add reminder POST endpoint", "Fix timezone handling", "Add Zod validation" |
| Max story points | **5** |
| Estimation includes | Groom → tech spec → code → test → PR → review → deploy → demo → done |
| Default owner | Lead Dev (S1/S2, arch-heavy) or Associate (S3/S4, feature work) |
| Due date | Sprint end (implicit — must complete within assigned sprint) |
| Deliverable | Code merged to main, deployed to staging, demo passed |

#### 2. Story
> **Analysis/research work. No code output — produces a document or decision.**

| Field | Value |
|---|---|
| Label | `story` |
| What it is | Research, analysis, investigation, or decision-making work |
| Examples | "Evaluate push notification providers", "Design DB schema for recurring reminders", "Investigate iOS crash root cause" |
| Max story points | **5** |
| Estimation includes | Research → analysis → document/recommendation → review → approved |
| Default owner | Lead Dev preferred (requires wide context) |
| Due date | Sprint end |
| Deliverable | Document (recommendation, analysis, or design doc) — NOT code |
| Output location | `epics/ROOT-NNN/analysis.md` or `design-meetings/` |

**Key rule:** A Story often PRECEDES a Task. Example:
```
Story: ROOT-051 "Design push notification architecture" (2 pts, Sprint S-03)
  → produces: architecture doc with chosen provider + API design
Task:  ROOT-052 "Implement push notification service" (5 pts, Sprint S-03)
  → depends on ROOT-051's output
Task:  ROOT-053 "Implement iOS push integration" (3 pts, Sprint S-03)
  → depends on ROOT-052
```

#### 3. Prod Issue
> **Production bug. Has a mandatory due date. Highest urgency.**

| Field | Value |
|---|---|
| Label | `prod-issue` |
| What it is | Bug reported from production affecting real users |
| Examples | "iOS app crashes on reminder save", "Push notifications not delivering", "Login fails after password reset" |
| Max story points | **5** (if >5, split into hotfix + follow-up) |
| Estimation includes | Root cause analysis → fix → test → hotfix deploy → verify in prod |
| Default owner | **Lead Dev always** (S1/S2 severity) |
| Due date | **MANDATORY — set by PO based on severity** |
| Due date rules | S1: same day. S2: within 2 business days. S3: within sprint. |
| Deliverable | Fix merged, deployed to production (not just staging), verified |
| Branch naming | `hotfix/ROOT-NNN-short-description` |
| Spec location | `specs/interrupt/ROOT-NNN.spec.md` (auto-created) |

**Prod Issue due date matrix:**
| Severity | Max time to resolve | Escalation |
|---|---|---|
| S1 — Critical | Same day (within hours) | @datta immediately. Lead Dev drops everything. |
| S2 — High | 2 business days | Lead Dev picks up next. Daily Slack updates. |
| S3 — Medium | Within current sprint | Normal sprint flow. |

**Prod Issue flow:**
```
Bug reported → PO creates Prod Issue epic with due date
  → PO assigns to Lead Dev (always)
  → Lead Dev does root cause analysis
  → Lead Dev codes fix + tests
  → Hotfix branch → fast-track PR review
  → Deploy to production (not just staging)
  → Verify fix in production
  → PO updates status.log with resolution
  → Datta notified of resolution (S1/S2)
```

#### 4. TechMain (Technical Maintenance)
> **Tech debt, dependency upgrades, infrastructure work. Keeps the system healthy.**

| Field | Value |
|---|---|
| Label | `tech-maintenance` |
| What it is | Non-feature work that maintains system health |
| Examples | "Upgrade React Native to 0.74", "Fix SonarQube CVE findings", "Optimize Docker build time", "Refactor auth middleware" |
| Max story points | **5** |
| Estimation includes | Audit → plan → implement → test → verify CI green → deploy |
| Default owner | Lead Dev (infra, security) or Associate (simple upgrades) |
| Due date | Sprint end (unless CVE-driven — then follows Prod Issue due date rules) |
| Deliverable | System improvement verified — all CI green, no regressions |
| Priority | Usually S4 (fills remaining capacity). Elevated to S2 if CVSS ≥ 7. |

**TechMain sources:**
- `tech-upgrades/suggestions.md` (PO weekly scan)
- SonarQube findings (weekly scan)
- Sprint retro action items
- PC-11 (Closing PC) is entirely TechMain

#### 5. Blocker
> **Impediment blocking a developer or PO. Assigned to Datta (or the blocking party). Has a cascading 1/3/7 day SLA.**

| Field | Value |
|---|---|
| Label | `blocker` |
| What it is | An impediment that prevents a developer or PO from continuing their work |
| Examples | "Need Datta decision on auth provider", "Waiting for API key from external service", "VPS access not working", "Unclear acceptance criteria on ROOT-055", "Waiting for Datta to deliver project documentation" |
| Max story points | **3** (blockers should be resolved quickly) |
| Estimation includes | Investigation → decision/action → unblock team → verify work resumes |
| Default owner | **Datta always** (as Advisor/Scrum Master, he removes impediments) |
| Alt owner | Another human/party if they are the blocker (e.g., external vendor) — still tracked by Datta |
| Due date | **MANDATORY — cascading SLA below** |
| Deliverable | Decision made, access granted, or impediment removed — blocked epic resumes |
| Spec location | `specs/interrupt/BLOCK-NNN.spec.md` |

**Cascading Blocker SLA — 1 / 3 / 7 days**

This policy applies to every Blocker epic. Each window triggers a specific
action. The total budget is 1 week; after that, dependent work is hard-paused
until Datta responds (no LLM spend on blocked paths).

| Window | When | Priority | Action | Notification |
|---|---|---|---|---|
| **T+0** | Blocker created | P3 | BLOCK-NNN created, auto-assigned to Datta (or blocking party), due date = T+7 | PO posts in `#rootine-planning` tagging owner; Datta gets direct Slack ping |
| **T+1 day — Response window** | No response in 24h | P3 | PO bumps reminder in `#rootine-planning` | "@datta BLOCK-NNN awaiting first response — 24h elapsed" |
| **T+3 days — Escalation window** | No resolution in 72h | **P2** (bumped) | PO broadcasts downstream impact to team | Impact report: "BLOCK-NNN will delay epics [IDs] and sprints [S-NN+1, S-NN+2]. Dependent agents may pause LLM usage if not resolved by T+7." |
| **T+7 days — Hard pause** | Still unresolved after 1 week | **P1** (bumped) | PO hard-pauses all dependent epics. Agents stop LLM work on those paths. Sprint may need cancellation (PLAT-013) | "🛑 BLOCK-NNN HARD PAUSE. Dependent epics [IDs] frozen. Agents idle on these paths. Waiting for Datta. No further LLM spend until resolved." |

**Why the 7-day hard pause:**
Beyond 1 week, continuing to "nudge" the agents or let them speculate on the
blocker burns tokens without progress. The decision belongs to Datta. The
cheapest and most honest action is to stop work and wait. Agents can be
reassigned to unblocked epics if any exist.

**Blocker creation flow:**
```
Developer, PO, or Lead Dev encounters impediment they cannot resolve
  → Posts in #rootine-dev: "blocker ROOT-NNN: [description]"
  → PO creates Blocker epic (BLOCK-NNN) in specs/interrupt/
  → Auto-assigned to Datta (or blocking party)
  → Due date = T+7 (hard pause threshold)
  → Datta receives Slack direct ping immediately (T+0)
  → Tracker schedules 3 wake-ups: T+1 (nudge), T+3 (escalate), T+7 (hard pause)
  → Datta resolves blocker at any point → PO marks BLOCK-NNN as DONE → dependent epics resume

If T+1 passes with no response:
  → PO posts reminder in #rootine-planning tagging Datta
  → Priority unchanged (P3)

If T+3 passes with no response:
  → PO computes downstream impact (which epics and sprints depend on this)
  → PO posts impact report in #rootine-planning and #rootine-dev
  → Priority bumped P3 → P2
  → Dependent epics flagged "at risk" in INDEX.md
  → If the blocker owner is someone other than Datta, Datta is also notified
    so he can intervene with the blocking party

If T+7 passes with no response:
  → PO hard-pauses all dependent epics (status: PAUSED-BLOCKED)
  → Agents are instructed to stop ALL LLM calls on paused epics
  → Agents reassigned to any unblocked work, otherwise idle
  → Priority bumped P2 → P1
  → PO posts hard-pause notice in #rootine-dev and #rootine-planning
  → Blocker is flagged in the next retro as a critical process failure
  → If paused epics would cause the sprint goal to become unachievable,
    PO recommends sprint cancellation per PLAT-013
```

**Cost rationale:**
During a hard pause, agents must not re-read the blocker, re-draft options,
or "think ahead" — this burns tokens without unblocking anything. The answer
is a human decision that no amount of LLM work can substitute for. Idle is
the correct state.

**Blocker vs Prod Issue:**
| | Blocker | Prod Issue |
|---|---|---|
| Source | Internal impediment | Production bug |
| Owner | Datta always | Lead Dev always |
| Affects | Developer/PO productivity | End users |
| Code output | Usually NO (decision/access) | YES (hotfix) |
| Due date | Cascading 1/3/7 days | Based on severity (S1 same-day, S2 2 days, S3 within sprint) |
| LLM usage while open | Continues until T+7, then HARD PAUSE | Continues — prod bugs are urgent, not budget-sensitive |

#### 6. Feature
> **Large feature spanning multiple epics. The parent container.**

| Field | Value |
|---|---|
| Label | `feature` |
| What it is | A user-facing capability that's too large for a single epic |
| Examples | "Push notification system" (needs: architecture Story + service Task + iOS Task + Android Task + settings UI Task) |
| Total story points | **Can exceed 10+ points** (it's a container, not a single epic) |
| Individual epics within | Each child epic is ≤5 points and independently deliverable |
| Default owner | Split across Lead Dev + Associate |
| Due date | Spans multiple sprints if needed |
| Tracking | Feature label groups child epics. PO tracks % complete at feature level. |

**Feature decomposition rule:**
```
Feature: "Push Notification System" (total: 18 pts across 5 epics)
  │
  ├── Story:  ROOT-051 "Design push architecture"        (2 pts, Lead Dev, S-03)
  ├── Task:   ROOT-052 "Push notification service"        (5 pts, Lead Dev, S-03)
  ├── Task:   ROOT-053 "iOS push integration"             (3 pts, Associate, S-03)
  ├── Task:   ROOT-054 "Android push integration"         (3 pts, Associate, S-03)
  └── Task:   ROOT-055 "Push notification settings UI"    (5 pts, Associate, S-04)

Each child epic:
  - Has its own spec, AC, branch, PR
  - Is independently deliverable
  - Is ≤5 points
  - Can be in different sprints
```

**Feature in Slack daily report:**
```
*Feature: Push Notification System (18 pts)*
  Completed: ROOT-051 (2), ROOT-052 (5) = 7 pts (39%)
  In progress: ROOT-053 (3), ROOT-054 (3) = 6 pts
  Remaining: ROOT-055 (5) = 5 pts (Sprint S-04)
```

### Summary Table

| Type | Label | Max Pts | Has Due Date? | Default Owner | Code Output? | Can Span Sprints? |
|---|---|---|---|---|---|---|
| Task | `task` | 5 | No (sprint end) | Lead Dev or Associate | YES | No |
| Story | `story` | 5 | No (sprint end) | Lead Dev preferred | NO (document) | No |
| Prod Issue | `prod-issue` | 5 | **YES (mandatory)** | **Lead Dev always** | YES (hotfix) | No (urgent) |
| TechMain | `tech-maintenance` | 5 | No (sprint end) | Lead Dev preferred | YES | No |
| Blocker | `blocker` | 3 | **YES (cascading 1/3/7 days — hard pause at T+7)** | **Datta always** | Usually NO | No (urgent) |
| Feature | `feature` | **>10 (container)** | Optional | Split across team | YES (children) | **YES** |

### GitHub Labels

Each epic gets exactly ONE category label + severity label + sprint label:

```
Category labels:  task, story, prod-issue, tech-maintenance, blocker, feature
Severity labels:  p1, p2, p3, p4
Sprint labels:    PC-01-S01, PC-01-S02, etc.
Status labels:    backlog, in-progress, review, done, rollover
Special labels:   blocking, rollover, interrupt
```

### Epic ID Prefixes

| Type | ID Pattern | Example |
|---|---|---|
| Task | ROOT-NNN | ROOT-041 |
| Story | ROOT-NNN | ROOT-051 (same prefix, differentiated by label) |
| Prod Issue | ROOT-NNN | ROOT-060 |
| TechMain | ROOT-NNN | ROOT-070 |
| Blocker | BLOCK-NNN | BLOCK-001 (impediment assigned to Datta) |
| Feature (parent) | FEAT-NNN | FEAT-001 (groups child ROOT-NNN epics) |
| Platform work | PLAT-NNN | PLAT-001 |
| Infrastructure | INFRA-NNN | INFRA-001 |

### Updated GitHub Issue Template

```markdown
## Epic: ROOT-NNN — [Title]

**Category:** [ ] Task  [ ] Story  [ ] Prod Issue  [ ] TechMain  [ ] Blocker  [ ] Feature
**Severity:** S__
**Story Points:** __
**Sprint:** PC-NN Sprint S-NN
**Parent Feature (if applicable):** FEAT-NNN
**Due Date (Prod Issue only):** YYYY-MM-DD

**Assigned to:** [Lead Dev / Associate / Human Dev]
```

### Files Touched
- `.github/ISSUE_TEMPLATE/epic.md` — updated with category field
- `specs/INDEX.md` — PO adds category column
- `.sdd/coding-standards.md` — branch naming per category
- PO daily report — groups by category

## [STANDARDS]
- Every epic MUST have exactly one category label
- Prod Issues MUST have a due date — PO sets it based on severity
- Blockers follow the cascading 1/3/7 day SLA — auto-nudged at T+1, escalated with downstream impact report at T+3, hard-paused at T+7
- Blockers are always assigned to Datta (or the blocking party with Datta tracking)
- Hard-paused blockers trigger ZERO LLM spend on dependent epics until Datta responds
- Features MUST be decomposed into child epics ≤5 points each
- Stories MUST produce a document — if it produces code, it's a Task
- TechMain is default S4 unless CVE-driven (then follows CVSS → severity mapping)
- No epic exists without a category — PO validates at assignment time

## [ACCEPTANCE CRITERIA]
```
AC-001: Given PO creates a new epic, when it's added to INDEX.md, then it has
        exactly one category label (task/story/prod-issue/tech-maintenance/feature).

AC-002: Given a Prod Issue is created with S1 severity, when PO assigns it, then
        it has a due date of "today" and Lead Dev is immediately notified.

AC-003: Given a Feature "Push Notifications" has 5 child epics totaling 18 pts,
        when PO tracks it, then the daily report shows feature-level progress (%).

AC-004: Given a Story is completed, then its deliverable is a document (not code),
        and it's stored in epics/ROOT-NNN/ or design-meetings/.

AC-005: Given an epic is estimated at 8 points, when PO categorizes it as Task,
        then PO must split it into two Tasks (e.g., 5+3) before assignment.

AC-006: Given a Feature has child epics in Sprint S-03 and S-04, when Sprint S-03
        review runs, then only S-03 children count toward S-03 velocity.

AC-007: Given a developer posts "blocker ROOT-055: waiting on Datta decision for
        auth provider", when PO creates BLOCK-001, then it is assigned to Datta
        with a due date of T+7 (hard pause threshold) and the tracker schedules
        three wake-ups at T+1, T+3, and T+7.

AC-008: Given BLOCK-001 reaches T+1 (24h) with no response, when the tracker
        fires, then PO posts a reminder in #rootine-planning tagging the owner.
        Priority remains P3.

AC-009: Given BLOCK-001 reaches T+3 (72h) with no resolution, when the tracker
        fires, then PO computes downstream impact (list of dependent epics and
        sprints), posts an impact report, bumps priority P3 → P2, and flags
        dependent epics as "at risk" in INDEX.md.

AC-010: Given BLOCK-001 reaches T+7 (1 week) with no resolution, when the
        tracker fires, then PO sets all dependent epics to PAUSED-BLOCKED,
        instructs agents to stop ALL LLM calls on those paths, bumps priority
        P2 → P1, and posts a hard-pause notice. Agents reassigned to
        unblocked work if any exists.

AC-011: Given epics are in PAUSED-BLOCKED state, when an agent attempts an LLM
        call on a paused epic, then the call is rejected at the token tracker
        layer (PLAT-001) with reason "blocker hard-pause active".

AC-012: Given a hard-paused blocker makes the current sprint goal unachievable,
        when PO assesses viability, then PO recommends sprint cancellation per
        PLAT-013 in #rootine-planning.
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created — 5 epic types defined with rules
- 2026-04-10: Added Blocker category (6th type) — assigned to Datta, ≤3-day due date
- 2026-04-11: Replaced flat 3-day Blocker SLA with cascading 1/3/7 day policy — nudge at T+1, downstream impact escalation at T+3, hard pause with zero LLM spend at T+7. Added AC-008 through AC-012.
