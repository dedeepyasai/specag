# Rootine AI Development Ecosystem
## Project Bible & System Design Document

**Roles:** Datta (Advisor/Admin) | Lead Dev Agent (Claude Sonnet 4.6) | Associate Dev Agent (GPT-4.1) | PO Agent (GPT-4o mini)

**Version 1.8 | April 2026 | Dallas, TX**

---

## Table of Contents

1. [Executive Overview](#1-executive-overview)
2. [Roles & Responsibilities](#2-roles--responsibilities)
3. [Year Structure — Project Contexts & Sprints](#3-year-structure--project-contexts--sprints)
4. [MVP Definition & Epic Generation](#4-mvp-definition--epic-generation)
5. [Severity & Priority System](#5-severity--priority-system)
6. [SDD Architecture & Folder Structure](#6-sdd-architecture--folder-structure)
7. [Coding Standards & Commit Rules](#7-coding-standards--commit-rules)
8. [Epic Acceptance & Demo Flow](#8-epic-acceptance--demo-flow)
9. [Multi-Provider Model Architecture](#9-multi-provider-model-architecture)
10. [Token Tracking & Limits Configuration](#10-token-tracking--limits-configuration)
11. [Sprint Kanban & Collision Guard](#11-sprint-kanban--collision-guard)
12. [Project Configuration Files](#12-project-configuration-files)
13. [PO Agent — Daily Slack Report Format](#13-po-agent--daily-slack-report-format)
14. [Scaling to 200 Agents](#14-scaling-to-200-agents)
15. [Mac Mini Runtime Setup](#15-mac-mini-runtime-setup)
16. [Closing PC Protocol (PC-11)](#16-closing-pc-protocol-pc-11)
17. [Quick Reference Summary](#17-quick-reference-summary)
18. [Infrastructure & Platform Specs](#18-infrastructure--platform-specs)
19. [Project File Structure](#19-project-file-structure)
20. [Sprint Ceremonies & Agile Framework](#20-sprint-ceremonies--agile-framework)
21. [Story Points & Work Schedules](#21-story-points--work-schedules)
22. [New Hire Onboarding](#22-new-hire-onboarding)
23. [Epic Categorization](#23-epic-categorization)
24. [Testing Standards & Quality Gate](#24-testing-standards--quality-gate)
25. [Continuous Improvement & Retrospective System](#25-continuous-improvement--retrospective-system)
26. [Environment Strategy & Deployment Pipeline](#26-environment-strategy--deployment-pipeline)
27. [Rollback Mechanism](#27-rollback-mechanism)

---

## 1. Executive Overview

This document is the complete reference for the Rootine AI-powered development ecosystem — a fully autonomous, multi-provider, spec-driven software delivery system designed to build and maintain a web application and iOS/Android mobile application with minimal human interruption.

The system is governed by the **SDD (Spec-Driven Development)** framework, orchestrated by **CrewAI** running continuously on a Mac Mini, and tracked through **GitHub**, **Slack**, and a multi-provider token management layer spanning Anthropic and OpenAI.

### 1.1 Working Software Is the Point — Documentation Serves It

This document is long. That is deliberate, and it is a tradeoff the reader should understand up front.

**AI agents need documented rules to behave consistently.** Every section of this Bible exists because an agent, not a human, is the primary reader. An agent cannot overhear a hallway conversation, cannot "just ask the team," and cannot read intent from tone. It needs written rules.

**Humans should prefer shipping over documenting.** When a human developer joins this project, the Bible is their onboarding reference, not their daily companion. Humans should:

- Prefer a working prototype to a written design doc when both would take the same time
- Accept that specs are scaffolding for agents, not gospel for humans
- Never add a section to this Bible unless an agent would behave wrongly without it
- Never expand an existing section unless a specific observed incident requires it

**The Agile Manifesto's first value applies to humans here: working software over comprehensive documentation.** The Bible exists because of a specific constraint (AI agents), not because documentation is intrinsically valuable. If the agents could be replaced by a telepathic team, most of this document would be deleted.

**Test:** If removing a paragraph from this Bible would NOT change agent behavior, that paragraph should be deleted.

### 1.2 Who Is the Customer?

Every Agile framework is built around serving a customer. This scaffolding does not yet have one.

- **During scaffolding phase (PC-01):** There is no end customer. The "customer" is the future user of the template — Datta or whoever adopts this repo. Sprint Reviews demonstrate framework features (rollback, cancellation, hooks) to Datta, not end users.
- **During real project phases (PC-02+):** Once a real product is being built on this scaffolding, the customer is the end user of that product. PO Agent represents the customer's interests. Sprint Reviews must include user-facing demos once real users exist. This section will be updated at PC-02 kickoff to name the actual customer and their feedback channel.
- **Gap acknowledged:** A customer feedback loop (user testing, analytics, support channels, interviews) is NOT yet defined. This is intentional — defining it before a real product exists produces make-believe process. It will be added in the first real project PC when there is something to get feedback on.

**Placeholder to replace at PC-02 kickoff:** name the product, name the customer persona, name the feedback channels, and update this section.

### System at a Glance

| Field | Value |
|---|---|
| Project name | Rootine — AI-powered daily task and reminder app |
| Platforms | Web (React/Next.js), iOS, Android (React Native) |
| Runtime | Mac Mini — always-on, cron-driven CrewAI orchestration |
| Framework | SDD (Spec-Driven Development) + GitHub + Slack |
| Year cadence | 11 PCs × 5 sprints (10 regular) + 1 closing PC × 2 sprints = 52 sprints/year |
| Total roles | 4 — Lead Dev Agent, Associate Dev Agent, PO Agent, Datta (Advisor) |
| Providers | Anthropic (Claude Sonnet 4.6) + OpenAI (GPT-4.1 + GPT-4o mini) |
| Datta's involvement | Decision gates only — not in the daily operational loop |

---

## 2. Roles & Responsibilities

The ecosystem has four distinct roles. Two are developers (both AI), one is the orchestration agent (AI), and one is the human advisor (Datta). Each has a clearly bounded authority scope.

### 2.1 Datta — Advisor / Admin

> **Datta is not in the daily operational loop. He is consulted exclusively at defined decision gates. The system runs autonomously between those gates.**

| Responsibility | Detail |
|---|---|
| Role | Advisor, final authority, QA tester, epic seeder |
| Daily touchpoint | Reads the PO's Slack report each evening at own pace |
| MVP definition | Writes 3-sentence MVP statement into `pc.manifest.yaml` at each PC start |
| Epic seeding | Creates high-level epic descriptions; PO decomposes into spec-ready epics |
| QA | Tests web app + iOS + Android on staging/TestFlight after each sprint; issues green flags |
| Decision gates | Repo decoupling approval, PC close sign-off, S1 escalation awareness, year-retro review |
| Design meetings | Reviews Lead Dev's recommendation doc every 2 sprints; approves or defers repo split |
| No involvement in | Epic assignment, severity scoring, daily agent management, token tracking |

### 2.2 Lead Dev Agent — Claude Sonnet 4.6 (Anthropic)

> **The Lead Dev is the senior technical authority in the system. It owns all decisions with systemic impact and is the only agent that reads wide context across multiple files.**

| Responsibility | Detail |
|---|---|
| Model | Claude Sonnet 4.6 — high context, deep reasoning |
| Owns | API contracts, DB schemas, repo structure, service boundaries, `interface-contract.md` |
| Epic types | S1 prod bugs, S2 Sonar CVEs, blocking epics, arch-heavy business epics |
| Context scope | Reads full spec files, sprint retros, architecture docs, `coding-standards.md` |
| PR authority | Reviews ALL PRs from Associate. Can veto with documented reason in `status.log` |
| Design meeting | Prepares 1-page recommendation doc every 2 sprints (file heat-map + split/stay rationale) |
| Escalation | Escalates to Datta only: repo split approval, S1 notifications, PC close review |
| Token provider | Anthropic — tracked in `anthropic_usage.db` |

### 2.3 Associate Dev Agent — GPT-4.1 (OpenAI)

> **The Associate operates in narrow context — reads one spec file at a time, never touches shared infrastructure, and works exclusively within its assigned epic boundary.**

| Responsibility | Detail |
|---|---|
| Model | GPT-4.1 — strong code generation, instruction-following, narrow-context tasks |
| Owns | Feature implementation within assigned epic, unit tests, PR description |
| Epic types | S3 business epics, S4 technical debt, non-blocking features |
| Context scope | Reads assigned epic spec only + `specs/INDEX.md` for routing. Zero cross-epic reading |
| When blocked | Writes `BLOCKED: reason` to `status.log`; PO re-routes at next check |
| PR flow | Raises PR using template; Lead Dev reviews; Associate addresses feedback |
| Growth path | PO can promote Associate to Lead authority on specific epics based on track record |
| Token provider | OpenAI — tracked in `openai_usage.db` |

### 2.4 PO Agent — GPT-4o mini (OpenAI)

> **The PO is the single assignment authority for the entire system. It is the only entity that writes to the epic assignment table and `specs/INDEX.md`. All agents read their assignments — they never self-assign.**

| Responsibility | Detail |
|---|---|
| Model | GPT-4o mini — cheap, efficient, structured text tasks |
| Epic assignment | Only entity that assigns epics to Lead Dev or Associate. Writes to `INDEX.md` |
| Severity triage | Runs S1–S4 severity scoring at PC start and every Monday morning |
| Collision check | Runs file-tree comparison before every assignment; writes no-collision note to `status.log` |
| Sprint loading | Distributes epics across 5 sprints; balances Lead Dev (arch-heavy) vs Associate (parallel features) |
| Daily Slack report | Sends structured report to `#rootine-dev` at 6pm every weekday via cron |
| Rollover handling | Labels rolled-over epics, re-evaluates severity, moves spec to `in-progress` |
| Tech upgrades scan | Weekly scan of `tech-stack.yaml` vs npm/pypi latest; writes to `tech-upgrades/suggestions.md` |
| PO queue fallback | If token cap hit mid-day, queues assignments to `agents/po_queue.json` for next reset |
| Token provider | OpenAI — tracked in `openai_usage.db` (separate from Associate) |

---

## 3. Year Structure — Project Contexts & Sprints

The year is divided into **Project Contexts (PCs)**. Each PC is a self-contained unit of work with its own MVP target, epic backlog, and folder structure. Context is passed between PCs via a single compressed summary file — never by re-reading the full previous PC.

### Year Cadence

| Field | Value |
|---|---|
| Total PCs per year | 11 |
| Regular PCs | 10 × 5 sprints = 50 sprints |
| Closing PC (PC-11) | 1 × 2 sprints = 2 sprints (tech debt + upgrades only) |
| Total sprints per year | 52 |
| Working days per year | 260 (52 weeks × 5 days) |
| Epics per sprint | ~6 total (3 per developer) |
| Epics capacity per year | ~300 feature epics + closing PC upgrades |
| PC-11 focus | No feature work — dependency upgrades, CVE patches, year retrospective, next-year seeding |

### 3.1 Regular PC Structure (PC-01 to PC-10)

| Sprint | Focus & Key Activities |
|---|---|
| Sprint 1 | Kick-off: Datta writes MVP + epic seeds. PO runs severity triage, assigns epics. Agents onboard to `pc.manifest.yaml`. Feature build begins. |
| Sprint 2 | Full velocity: both agents at capacity. Design meeting after Sprint 2 (Lead Dev recommends, Datta approves repo split or stay). Tech-upgrade scan. |
| Sprint 3 | Feature build + QA: Datta QA pass on all Sprint 1–2 epics. Bug fixes. Green flags issued per epic. |
| Sprint 4 | Hardening: edge cases, performance, mobile build optimisation. Second design meeting. Sonar scan. |
| Sprint 5 (PC close) | PO writes `context-summary.md` (max 200 lines) distilling all retros. Datta reviews + approves next PC seeds. `INDEX.md` frozen for archive. |

### 3.2 Closing PC Structure (PC-11)

| Sprint | Focus & Key Activities |
|---|---|
| Sprint 51 (S1 of PC-11) | Dependency audit: scan `package.json` + `requirements.txt` vs npm/pypi. Write `dep-audit.md`. Lead Dev implements approved upgrades. All CI green. |
| Sprint 52 (S2 of PC-11) | Full test suite post-upgrades. PO reads all 10 `context-summary.md` files sequentially (one at a time). Writes `year-retro.md` (1 page). Datta signs off. `upgrade-plan.md` seeds next year's PC-01. |

### 3.3 PC Handoff Rules

| What carries over | What resets |
|---|---|
| `context-summary.md` from prev PC (PO reads this one file on Day 1) | Epic backlog — Datta writes fresh for each PC |
| Open bug list from `status.log` entries | Token budget counters — reset at PC start |
| `tech-upgrades/suggestions.md` (appended, never rewritten) | Sprint retro files — archived, not carried forward |
| Rollover epics (re-evaluated for severity) | Assignment table — PO rebuilds from scratch each PC |

---

## 4. MVP Definition & Epic Generation

Every PC has exactly one **MVP target** — a clear, scoped deliverable that all epics in the PC contribute toward. The MVP is defined by Datta and decomposed by the PO agent into actionable epics.

### 4.1 MVP Definition Flow

1. **MVP session:** Datta writes a 3-sentence MVP statement into `pc.manifest.yaml`. Example: *"Users can create, schedule, and receive reminders on all platforms. The reminder system supports recurring patterns, push notifications, and cross-device sync. Auth, onboarding, and settings are complete."*
2. **PO reads** `pc.manifest.yaml` + prev `context-summary.md` (one file). Acknowledges MVP scope.
3. **Epic decomposition:** PO breaks MVP into Business Epics (user-facing features) and Technical Epics (infra, perf, security). Each gets a one-line description, type label, and complexity estimate (S/M/L).
4. **Interrupt slots reserved:** PO pre-reserves 2–3 blank GitHub Issues per sprint with labels only — no spec yet. These absorb prod bugs and Sonar findings without disrupting the planned board.
5. **Project code assignment:** Each epic gets a GitHub Issue with code `ROOT-NNN`, label, milestone (`PC-NN Sprint-NN`), assignee, and linked spec path.
6. **Spec skeleton auto-generated:** PO creates `spec.md` skeleton per epic. Lands in `specs/backlog/`. Status: `BACKLOG`. Lead Dev reviews technical epics for arch alignment before Sprint 1 begins.
7. **Sprint distribution:** PO loads epics across 5 sprints. Lead Dev gets blocking/arch-heavy epics first. Associate gets parallel feature epics. No two epics from different developers touch the same files.

### 4.2 Epic Categories (see Section 23 for full detail)

| Category | Label | Max Pts | Default Owner | Trigger |
|---|---|---|---|---|
| **Task** | `task` | 5 | Lead Dev or Associate | Coding-required work from backlog |
| **Story** | `story` | 5 | Lead Dev preferred | Analysis/research — produces document, not code |
| **Prod Issue** | `prod-issue` | 5 | Lead Dev always | Production bug (mandatory due date) |
| **TechMain** | `tech-maintenance` | 5 | Lead Dev preferred | Tech debt, dep upgrades, CVE fixes |
| **Feature** | `feature` | >10 (container) | Split across team | Large capability — child epics ≤5 pts each |
| Rollover | `rollover` | Original assignee | Uncommitted work from prev sprint (added to any category) |

---

## 5. Severity & Priority System

Priority is not fixed — it is **severity-scored** at the start of each PC by the PO and re-evaluated every Monday morning. The severity score drives sprint ordering for the entire PC, not just a single sprint.

| Severity | Label | Definition | PO Action |
|---|---|---|---|
| S1 — Critical | `p1` | Production broken, data loss risk, security breach, or blocks both developers simultaneously | Pause all lower-severity assignments. Alert Datta immediately via Slack @mention. Lead Dev drops everything. |
| S2 — High | `p2` | High CVE (CVSS >= 7), blocking epic (other dev waiting on contract/schema), rollover that now blocks new sprint work | Lead Dev picks next after any active S1. Associate continues planned work uninterrupted. |
| S3 — Medium | `p3` | Business epics (MVP features), non-blocking rollovers, medium CVEs (CVSS 4–6.9) | Normal sprint work. PO assigns in sequence. Both developers work in parallel without collision. |
| S4 — Low | `p4` | Tech debt, low CVEs (CVSS < 4), refactors, documentation, minor enhancements | Fills remaining sprint capacity after S1–S3 assigned. Often deferred to Closing PC if sprint is full. |

### 5.1 Severity Re-evaluation Rules

- A rollover automatically gets +1 severity bump if it was blocked by a prod bug — the delay was not the dev's fault.
- A rollover that becomes blocking another dev's epic is immediately re-scored to S2 regardless of original score.
- Sonar severity follows CVSS: >= 9 = S1, 7–8.9 = S2, 4–6.9 = S3, < 4 = S4.
- PO re-runs triage every Monday. Re-evaluation note appended to epic's `status.log`. Datta sees the diff in weekly Slack summary.
- PO can suggest severity changes but cannot promote above S2 without Lead Dev confirmation, and cannot set S1 without Datta awareness.

### 5.2 Rollover Protocol

When an epic does not complete within its sprint, the PO executes the following:

1. Appends to `status.log`: `"ROLLOVER from S-NN. Reason: [prod-bug-interrupt | priority-shift | scope-underestimate | dep-blocked]. Original severity: S3. Re-evaluated: S2 (now blocks ROOT-042)."`
2. Spec file stays in `specs/in-progress/`. One-line addendum added noting rollover and any scope change. No full rewrite.
3. GitHub label updated: adds `rollover` label, updates milestone to next sprint. Original sprint milestone kept as secondary label for velocity tracking.
4. Original assignee picks rollover before any new epics of the same or lower severity in the next sprint.

---

## 6. SDD Architecture & Folder Structure

> **Core principle: every agent always reads exactly one entry point — `specs/INDEX.md` — which routes to a single spec file. No agent ever scans a directory. This is what makes the system scale from 2 to 200 developers without collision.**

### 6.1 Full Directory Layout

```
year-2026/
  .sdd/                              # global config, never changes between PCs
    project.config.yaml              # app name, team, agent limits, work windows
    agent.limits.yaml                # per-agent token caps, models, schedules
    coding-standards.md              # naming, linting, commit format, PR rules
    tech-stack.yaml                  # all dependencies + versions

  PC-01/                             # active PC
    pc.manifest.yaml                 # PC number, sprint range, MVP statement, prev context path
    mvp-statement.md                 # 3-sentence MVP definition from Datta
    context-summary.md               # written at PC close by PO (max 200 lines)
    design-meetings/
      PC-01-S02-agenda.md            # Lead Dev recommendation + Datta decision
      PC-01-S04-agenda.md
    sprints/
      S01/retro.md  S02/retro.md  ...  S05/retro.md
    epics/
      ROOT-041/
        spec.md                      # full spec with labeled sections
        acceptance-criteria.md       # Given/When/Then ACs, PO-written
        demo-script.md               # PO runs this before accepting epic
        status.log                   # timestamped state changes + notes
    specs/                           # spec lifecycle folder
      INDEX.md                       # routing table: ROOT-NNN -> folder/file path
      backlog/ROOT-NNN.spec.md       # not started
      in-progress/ROOT-NNN.spec.md   # active dev
      finished/ROOT-NNN.spec.md      # QA passed, archived
      interrupt/ROOT-NNN.spec.md     # prod bugs, sonar — auto-created
    tech-upgrades/
      suggestions.md                 # PO weekly scan, append-only

  PC-02/ ... PC-10/                  # same structure
  PC-11/                             # closing PC — no epics/ or specs/
    tech-debt/
      dep-audit.md                   # generated from package files
      upgrade-plan.md                # seeds next year's PC-01 epics
    year-retro.md                    # PO distills all 10 context-summaries (1 page)
```

### 6.2 specs/INDEX.md — The Scalability Anchor

Every agent reads this file first, every time. It tells the agent the exact file path for any epic ID. Updated by PO only, on every assignment and every spec state change.

```markdown
# Specs index — auto-updated on every assignment. Do not edit manually.

| Epic ID  | Folder      | Spec file path                           | State     | Owner    |
|----------|-------------|------------------------------------------|-----------|----------|
| ROOT-041 | finished    | specs/finished/ROOT-041.spec.md          | DONE      | Lead Dev |
| ROOT-042 | in-progress | specs/in-progress/ROOT-042.spec.md       | IN DEV    | Associate|
| ROOT-044 | interrupt   | specs/interrupt/ROOT-044.spec.md         | INTERRUPT | Lead Dev |
| ROOT-048 | backlog     | specs/backlog/ROOT-048.spec.md           | BACKLOG   | Associate|

## Directory map (agents read this, never the folders)
- specs/backlog/      # not started
- specs/in-progress/  # active dev
- specs/finished/     # QA passed, archived
- specs/interrupt/    # prod bugs, sonar
```

### 6.3 Epic Spec File Structure

Each `spec.md` has labeled sections so agents receive a targeted instruction to read only the section relevant to their task.

```markdown
# ROOT-041: Reminder scheduling UI

## [SUMMARY] — all agents read this section
- App: Rootine
- Epic owner: Datta + PO Agent
- Status: IN PROGRESS
- Sprint: PC-01 Sprint 1
- Related specs: specs/api/ROOT-041.api.md, specs/ui/ROOT-041.ui.md

## [STORY] — PO reads this
As a user I want to schedule reminders with date, time, and recurrence
so I can be notified across web and mobile devices automatically.

## [TECH SPEC] — dev agents read this
- Endpoint: POST /reminders, GET /reminders, PATCH /reminders/:id
- DB table: reminders (id, user_id, title, scheduled_at, recurrence, status)
- Mobile: React Native screens — ReminderCreate, ReminderList
- Files touched: src/api/reminders.ts, src/db/schema.ts, mobile/screens/Reminders/

## [STANDARDS] — reviewer reads this
- All endpoints must have Zod validation
- DB migrations required for schema changes
- Mobile components must have E2E Detox test

## [CHANGE LOG] — auto-appended on PR merge
- 2026-04-08: Initial spec created
- 2026-04-09: API endpoints updated to include PATCH
```

---

## 7. Coding Standards & Commit Rules

These standards apply to all agents (AI and human) and are stored in `.sdd/coding-standards.md`. The PR validation GitHub Action enforces them on every PR automatically.

### 7.1 Commit Message Format

```
type(EPIC-REF): short description

Examples:
  feat(ROOT-041): add reminder scheduling endpoint with Zod validation
  fix(ROOT-045): resolve iOS crash on reminder save — null pointer guard
  patch(ROOT-044): upgrade lodash to 4.17.22 — CVE-2026-1234
```

| Commit type | When to use |
|---|---|
| `feat` | New feature or user-facing functionality |
| `fix` | Bug fix (prod bug, test failure, edge case) |
| `patch` | Security patch from Sonar/CVE finding |
| `refactor` | Code restructure with no behavior change |
| `test` | Adding or fixing tests only |
| `docs` | Documentation, spec updates, README changes |
| `chore` | Dependency updates, config changes, build tweaks |
| `rollover` | Picking up uncommitted work from previous sprint |

### 7.2 Branch Naming

- Feature: `feat/ROOT-NNN-short-description`
- Bug fix: `fix/ROOT-NNN-short-description`
- Hotfix: `hotfix/ROOT-NNN-short-description`
- Rollover: `rollover/ROOT-NNN-from-S-NN`
- Repo split: `chore/repo-split-domain-name`

### 7.3 PR Requirements

The `pr-validation.yml` GitHub Actions workflow enforces all of the following before any PR can be merged:

1. Epic ref present: PR body must contain `ROOT-NNN`
2. Acceptance criteria linked: PR must list AC IDs being satisfied (e.g. `Satisfies: AC-001, AC-002, AC-003`)
3. Spec update present: PR must confirm `spec.md` `[CHANGE LOG]` was updated, or provide a reason why not
4. Coding standards checklist: all boxes checked in the PR template
5. No `console.log` / debug statements in diff
6. CI tests passing: unit tests green, no TypeScript errors, no lint failures
7. No secrets in diff: automated secret scanning via `git-secrets`

### 7.4 PR Template

```markdown
## PR Summary
**Epic ref**: ROOT-NNN
**Spec file updated**: [ ] Yes  [ ] No (explain below)

## What changed
<!-- 1-3 sentences max -->

## Acceptance criteria verified
<!-- Paste AC IDs this PR satisfies, e.g. AC-001, AC-002 -->

## Spec update note
<!-- If spec.md changed, briefly describe what changed in [TECH SPEC] -->
<!-- If no spec change needed, explain why -->

## Coding standards checklist
- [ ] Naming conventions followed (see coding-standards.md)
- [ ] No console.log / debug statements
- [ ] Tests added or updated
- [ ] No breaking changes to existing endpoints (or noted in spec)
- [ ] No secrets or credentials in code
```

---

## 8. Epic Acceptance & Demo Flow

No epic is marked DONE until it passes the PO's demo script AND Datta's QA review.

| Stage | Who + What |
|---|---|
| 1. Code complete | Developer agent raises PR. All CI checks pass. Branch merged to main. |
| 2. Staging deploy | GitHub Actions automatically deploys merged code to staging environment. |
| 3. Slack notification | PO sends Slack message: `"ROOT-NNN merged. Preview: rootine-staging.app/[path]"` |
| 4. PO demo script | PO agent reads `demo-script.md` and executes it against staging. Logs pass/fail per step. |
| 5. PO acceptance gate | If demo passes: PO marks epic as `DEMO_PASSED` in `status.log`. If fail: creates bug sub-task. |
| 6. Datta QA | Datta tests web + iOS sim + Android sim against `acceptance-criteria.md`. Issues green flag or flags issues. |
| 7. Epic ACCEPTED | PO updates `status.log`: `"ACCEPTED [date] — Datta QA green flag"`. `INDEX.md` updated to `finished/`. |
| 8. Next sprint unlock | PO's next morning check: if all current sprint epics accepted, unlocks next sprint epic assignments. |

### 8.1 Acceptance Criteria Format

```markdown
# Acceptance criteria — ROOT-041: Reminder scheduling UI

AC-001: Given a logged-in user, when they submit the reminder form with a valid
        date/time, then the reminder is saved and appears in their list.

AC-002: Given a scheduled reminder, when the time arrives, then a push
        notification is delivered on iOS and Android within 30 seconds.

AC-003: Given an invalid date (past), when the user submits, then a validation
        error is shown and no reminder is created.

## Demo checklist (PO runs before accepting)
- [ ] Postman collection passes all ACs
- [ ] Unit tests green in CI
- [ ] No hardcoded secrets in diff
- [ ] Spec changelog updated
- [ ] Mobile build available on TestFlight / internal track
```

---

## 9. Multi-Provider Model Architecture

The ecosystem deliberately splits work across two AI providers — Anthropic and OpenAI — to optimize cost, preserve quota independence, and match model capability to task type.

### 9.1 Model Assignment

| Role | Model | Provider | Cost approx. |
|---|---|---|---|
| Lead Dev Agent | Claude Sonnet 4.6 | Anthropic | $3/1M in · $15/1M out |
| Associate Dev Agent | GPT-4.1 | OpenAI | $2/1M in · $8/1M out |
| PO Agent | GPT-4o mini | OpenAI | $0.15/1M in · $0.60/1M out |
| Estimated/sprint total | All three agents | Both providers | ~$2.10/sprint |
| Estimated/year total | 52 sprints | Both providers | ~$109/year |

### 9.2 Task-to-Model Routing

| Task | Model used + reason |
|---|---|
| Epic spec review (arch alignment) | Sonnet 4.6 — systemic reasoning needed to catch schema conflicts |
| Feature code generation | GPT-4.1 — strong code gen, narrow context, saves Anthropic quota |
| PR review (standards + AC check) | Sonnet 4.6 — Lead Dev reads standards + AC, requires nuanced judgment |
| Severity triage (S1–S4 scoring) | GPT-4o mini — structured scoring, pattern-matching, cheap |
| Collision check (file list comparison) | GPT-4o mini — deterministic comparison, no deep reasoning needed |
| Daily Slack report generation | GPT-4o mini — pure summarization, cheapest model is ideal |
| Prod bug root cause analysis | Sonnet 4.6 — S1 interrupt, Lead Dev, full context needed |
| `context-summary.md` (PC close) | Sonnet 4.6 — distilling 5 retros requires synthesis, worth cost once/PC |
| Dependency upgrade implementation | GPT-4.1 — well-scoped code changes, narrow context |
| `year-retro.md` generation | Sonnet 4.6 — cross-PC synthesis, done once per year |

### 9.3 Provider Isolation Benefits

- If Anthropic quota is stressed mid-sprint, OpenAI agents continue uninterrupted.
- If OpenAI has a rate-limit wave, Lead Dev and PC-close tasks still run on Anthropic.
- Separate SQLite databases (`anthropic_usage.db` and `openai_usage.db`) keep accounting clean.
- No shared state between providers — each tracks its own daily/weekly caps and reset windows.

---

## 10. Token Tracking & Limits Configuration

### 10.1 agent.limits.yaml — Full Configuration

```yaml
providers:
  anthropic:
    db_file: "agents/anthropic_usage.db"
    alert_threshold: 0.80
    models:
      lead_dev:
        model: "claude-sonnet-4-6"
        daily_token_cap: 40000
        weekly_token_cap: 200000
        max_tokens_per_call: 4000
        work_window: "08:00-22:00 CST"

  openai:
    db_file: "agents/openai_usage.db"
    alert_threshold: 0.80
    models:
      associate_dev:
        model: "gpt-4.1"
        daily_token_cap: 80000
        weekly_token_cap: 400000
        max_tokens_per_call: 4000
        work_window: "08:00-22:00 CST"
      po_agent:
        model: "gpt-4o-mini"
        daily_token_cap: 20000
        weekly_token_cap: 100000
        max_tokens_per_call: 2000
        cron: "0 18 * * *"  # daily — 7 days/week

enforcement:
  on_daily_80pct:
    action: "slack_alert"
    channel: "#rootine-dev"
    mention: "@datta"
  on_daily_100pct:
    action: "pause_agent_and_notify"
  on_weekly_80pct:
    action: "slack_alert_weekly_summary"
  on_weekly_100pct:
    action: "halt_until_monday"

tracker:
  dashboard_refresh_mins: 5
  slack_daily_summary: true
  separate_db_per_provider: true
  unified_view: true
```

### 10.2 Failover Rules

| Condition | System Response |
|---|---|
| Anthropic daily cap hit (Lead Dev) | PO pauses all S1/S2 assignments for the day. No automatic failover to OpenAI — arch decisions must not run on a different model mid-task. Datta gets Slack ping. Resumes at midnight reset. |
| OpenAI daily cap hit (Associate) | PO marks Associate as paused. In-progress epic stays in `in-dev` state with `status.log` entry. Lead Dev continues independently. No cross-provider fallback. |
| OpenAI daily cap hit (PO) | PO queues all pending assignments to `agents/po_queue.json`. At midnight reset, PO processes queue in severity order. No work lost — just deferred. |
| Transient rate limit (429, any provider) | Exponential backoff: 5s, 15s, 45s, then notify PO. Delay logged to `status.log`. Does not count against token budget. Retries transparently. |
| Anthropic backoff exceeds 3 minutes | Lead Dev writes current progress to a checkpoint file and pauses gracefully. Resumes from checkpoint on retry. |
| Weekly cap hit (either provider) | Full halt for that provider's agents until next sprint Saturday 08:00 CST. PO sends summary Slack report noting which epics are deferred. These become rollover candidates with severity re-evaluation. |

---

## 11. Sprint Kanban & Collision Guard

### 11.1 Kanban Columns & Transitions

| Column | Definition & Transition Rules |
|---|---|
| Backlog | Epics assigned to this sprint but not yet started. PO populates at sprint start. |
| In Dev | Agent has picked up the epic, opened a branch, and is actively coding. Branch: `feat/ROOT-NNN`. |
| Interrupt | Prod bug or Sonar CVE that entered mid-sprint. Assigned to Lead Dev. Gets its own `interrupt/` spec file. |
| PR / Review | Code complete. PR raised. `pr-validation.yml` running. Lead Dev reviewing Associate's work. |
| QA / Done | PR merged. Deployed to staging. Awaiting Datta's green flag. After green flag: ACCEPTED. |

### 11.2 PO Collision Check Protocol

Runs before every single epic assignment. Prevents two agents from ever writing to the same file simultaneously.

1. PO reads the epic's `spec.md` `[TECH SPEC]` section — specifically the `files touched` field.
2. PO compares against all in-progress specs' `files touched` fields.
3. If overlap found: PO serialises — one epic must be fully merged before the other is assigned.
4. If contract dependency found (Epic A defines a DB table that Epic B needs): Epic A elevated to S2 Blocking until merged.
5. `pr-validation.yml` also checks: does this branch's diff touch any file that another open branch modifies? If yes, CI flags it for Lead Dev review.
6. PO writes to `status.log`: `"Assigned to [LD|AA]. Collision check passed: no shared files with ROOT-NNN. Safe to proceed."`

### 11.3 Design Meeting — Every 2 Sprints

| Element | Detail |
|---|---|
| Trigger | Automatically after Sprint 2 and Sprint 4 of each PC. PO creates agenda file. |
| Lead Dev prepares | Reads `specs/INDEX.md` + last 2 sprint retros only. Writes 1-page recommendation: file ownership heat-map, build time trend, domain boundary signals, split/stay recommendation with rationale. |
| Decoupling triggers | Any one of: (a) two devs touched same file in 3+ PRs, (b) build time > 8 min, (c) clear domain boundary emerging. |
| Datta's role | Reads recommendation doc only (not retros, not specs). Approves, defers, or asks one clarifying question. Decision logged to agenda file. |
| If split approved | PO creates `Repo split` epic (ROOT-NNN, S2 severity), assigns to Lead Dev next sprint. Associate continues in original repo until split complete. |
| Interface contract first | Before any repo split PR: `interface-contract.md` filed in `specs/backlog/`. Defines API surface, event contracts, shared types. Both sides read this — nothing else. |

---

## 12. Project Configuration Files

### 12.1 project.config.yaml

```yaml
app:
  name: "Rootine"
  type: ["web", "ios", "android"]
  repo: "https://github.com/your-org/rootine"

team:
  admin: "Datta"
  slack_channel: "#rootine-dev"
  po_report_time: "18:00"      # 6pm CST daily cron
  timezone: "America/Chicago"

year:
  total_pcs: 11
  regular_pc_sprints: 5
  closing_pc_sprints: 2
  total_sprints: 52
```

### 12.2 pc.manifest.yaml (per PC)

```yaml
pc: 2
year: 2026
type: regular              # or: closing
sprint_range: [6, 10]
prev_context: ../PC-01/context-summary.md   # ONE file agents carry forward
epics_target: 30
focus: "Feature build — reminders, push notifications, settings"
mvp: |
  Users can create, schedule, and receive reminders across all platforms.
  Recurring patterns, push notifications, and cross-device sync are complete.
  Auth, onboarding, and settings are fully functional.
```

### 12.3 tech-stack.yaml

```yaml
frontend:
  framework: Next.js
  version: 14.2.0
  language: TypeScript 5.4

mobile:
  framework: React Native
  version: 0.73.2
  language: TypeScript 5.4

backend:
  runtime: Node.js 20 LTS
  framework: Express 4.19
  orm: Drizzle 0.30
  database: PostgreSQL 16

infrastructure:
  ci: GitHub Actions
  staging: Vercel (web) + Expo EAS (mobile)
  monitoring: SonarQube
```

---

## 13. PO Agent — Daily Slack Report Format

Sent every weekday at 6pm CST to `#rootine-dev`. Structured so Datta can scan it in under 60 seconds.

```
*PO Daily Report — [Day, Date]*

*Sprint S-NN | PC-NN | Day N of 5*

*Completed today:*
- ROOT-041 (Scheduling UI): MERGED + deployed to staging
- ROOT-039 (Settings sync rollover): MERGED + staged

*In progress:*
- ROOT-042 (Push delivery): ~60% — Associate, on track
- ROOT-045 (iOS crash fix): ~90% — Lead Dev, PR tomorrow

*Interrupts:*
- ROOT-044 (CVE lodash S2): Lead Dev queued after ROOT-045

*Token budget:*
- Anthropic: 52% daily / 41% weekly
- OpenAI: 68% daily / 55% weekly

*Datta action needed:*
- QA ROOT-041 on staging: rootine-staging.app/reminders
- QA ROOT-039 on staging: rootine-staging.app/settings
- No decisions required today
```

> When Datta action IS required (decision gate or S1 escalation), the PO uses `@datta` mention and adds a **URGENT** prefix to the message.

---

## 14. Scaling to 200 Agents

The architecture is designed to scale without workflow disruption. The core invariants that make this possible do not change at any team size.

### 14.1 Invariants That Hold at Any Scale

- Epic ownership is always 1:1 — one epic, one agent at a time. GitHub project code + assignee field is the lock.
- File-level isolation via spec paths — agents only read their own spec file. `INDEX.md` is read-only to agents.
- Branch-per-epic enforced by CI — `feat/ROOT-NNN` naming, `pr-validation.yml` flags file conflicts across open branches.
- PO is the single assignment authority — agents never self-assign or pick from a pool unsupervised.
- `INDEX.md` is the scalability multiplier — one file, under 100 lines, routes any agent to its exact spec file.

### 14.2 Squad Structure at Scale

| Tier | Structure & Responsibilities |
|---|---|
| Squad (2–10 agents) | 1 Lead Dev Agent + N Associate Dev Agents + 1 Squad PO Agent. Squad PO owns assignment within squad. All members follow the same SDD file discipline. |
| Domain (2–5 squads) | Domain PO coordinates between squads. Owns the domain repo's `INDEX.md`. Routes cross-squad blocking epics. Handles repo split decisions within domain. |
| Project (all domains) | Master PO Agent (GPT-4o mini) reads domain context-summaries only — never individual epic specs. Reports to Datta. The information pyramid compresses correctly upward. |
| Datta (Advisor) | Same role regardless of team size — decision gates only. Workload does not increase with team size. Still reads one PO summary per evening. |

### 14.3 Repo Decoupling Trigger Criteria

The Lead Dev monitors these signals and writes a recommendation when any one is met:

- Two developers touched the same file in 3 or more PRs within one PC.
- Build time exceeds 8 minutes on the CI pipeline.
- A clear domain boundary is emerging (e.g. notifications vs core reminders vs user management).
- A new squad is being added whose work is entirely independent of the current repo's domain.

---

## 15. Mac Mini Runtime Setup

| Field | Value |
|---|---|
| Hardware | Any M-series Mac Mini (M1 or later). Runs 24/7 with minimal idle power. |
| OS | macOS Sequoia 15+ with Xcode CLI tools installed |
| Python | Python 3.11+ with CrewAI, anthropic, openai packages |
| Node.js | Node.js 20 LTS for web app dev server and CI tooling |
| Docker Desktop | For local preview deployments and database containers |
| Ollama (optional) | Local LLM fallback for offline testing — does not replace cloud models in production |
| Git + GitHub CLI | Authenticated with project repo for PR automation |
| Cron | macOS launchd for scheduled PO agent tasks (6pm report, Monday triage, weekly scan) |

### 15.1 Key Cron Jobs

| Schedule | Job |
|---|---|
| Daily 08:00 CST | PO agent work window opens — agents active (7 days/week) |
| Daily 18:00 CST | PO sends daily Slack report to `#rootine-dev` (7 days/week) |
| Daily 22:00 CST | Agent work window closes — no new task assignments |
| Every Monday 08:00 | PO runs severity re-triage on all active epics |
| Every Sunday night | Token budget counters reset (weekly caps refresh) |
| Every Friday 17:00 | PO runs tech-upgrades scan (npm/pypi version check) |
| PC start (Sprint 1, Day 1) | PO reads `pc.manifest.yaml` + prev `context-summary.md` — kicks off PC |
| PC close (Sprint 5, Day 5) | PO writes `context-summary.md` (max 200 lines) — PC archived |

---

## 16. Closing PC Protocol (PC-11)

The Closing PC is structurally different from regular PCs. It contains no features, no business epics, and no `specs/` or `epics/` folders. Its sole purpose is **technical hygiene** and **institutional memory preservation**.

### 16.1 Sprint 51 — Dependency Audit & Upgrades

1. Lead Dev runs dep-audit agent: scans `package.json` and `requirements.txt` vs npm/pypi latest versions.
2. `dep-audit.md` generated — lists all outdated packages with CVSS scores and breaking-change risk.
3. Datta reviews `upgrade-plan.md` (derived from `dep-audit`). Approves which upgrades to implement.
4. Lead Dev and Associate implement approved upgrades. All CI green before Sprint 52 begins.

### 16.2 Sprint 52 — Retrospective & Year Seeding

1. Full test suite run post-upgrades. Any regressions fixed before year-retro begins.
2. PO reads all 10 `context-summary.md` files sequentially — one at a time, rolling summary approach. Never holds all 10 in memory simultaneously.
3. PO writes `year-retro.md` (maximum 1 page). Contains: shipped features summary, recurring blockers, tech debt resolved, upgrade history, top insights.
4. Datta reviews `year-retro.md` and signs off.
5. `upgrade-plan.md` entries that were deferred become seed epics for next year's PC-01.
6. All PC folders for the year are archived. New `year-YYYY/` root created. Ready for PC-01 kickoff.

---

## 17. Quick Reference Summary

| Question | Answer |
|---|---|
| How many PCs per year? | 11 (10 regular + 1 closing) |
| Sprints per regular PC? | 5 |
| Sprints in closing PC? | 2 |
| Total sprints per year? | 52 |
| Epics per sprint? | ~6 (3 per developer) |
| Who assigns epics? | PO Agent only — no self-assignment |
| Who reviews PRs? | Lead Dev Agent — always |
| Who approves repo splits? | Lead Dev recommends, Datta approves |
| Who defines the MVP? | Datta (3-sentence statement per PC) |
| Who runs severity triage? | PO Agent at PC start + every Monday |
| What is INDEX.md? | The routing table all agents read first — routes to exact spec file |
| What is context-summary.md? | Max 200-line PC close summary — the only file agents read from prev PC |
| Lead Dev model? | Claude Sonnet 4.6 (Anthropic) |
| Associate model? | GPT-4.1 (OpenAI) |
| PO model? | GPT-4o mini (OpenAI) |
| Token alert threshold? | 80% of daily/weekly cap — Slack alert to Datta |
| What triggers a rollover? | Epic not completed in sprint — PO labels and re-queues |
| What triggers a design meeting? | Every 2 sprints automatically (after S2 and S4) |
| Estimated cost per year? | ~$350-500 (VPS + APIs + fallback) |
| Closing PC focus? | Tech debt, dep upgrades, CVE patches, year-retro only — no features |
| Max story points per epic? | 5 — PO must split if larger |
| AI agent work hours/day? | 5 hours (1hr ON / 3hr BREAK pattern), 7 days/week = 35 hrs/sprint |
| Human agent work hours/day? | 6 hours (flexible schedule) |
| Story point = how many hours (AI)? | 1 point = ~1 hour |
| Story point = how many hours (human)? | 3 points = 1 day, 5 points = 2 days |
| Sprint runs? | Saturday to Friday (7-day cycle, AI agents work all 7 days) |
| When is Sprint Review + Deploy? | Saturday 3:00 PM (sprint end) |
| When is Sprint Retro? | Saturday 3:30 PM |
| When is Sprint Planning? | Saturday 4:00 PM (PO assigns, Datta approves) |
| When is Sunday Kickoff? | Sunday 10:00-11:00 AM (tech spec grooming, Datta participates) |
| When is Daily Standup? | Every day 8:05 AM (7 days/week) |
| Why weekends for ceremonies? | Datta works day job weekdays — weekends let him attend all major events |
| Slack channels? | `#rootine-dev` (daily ops) + `#rootine-planning` (planning + kickoff) |
| Definition of Ready? | Business spec + tech spec approved + points assigned + ACs defined |
| Definition of Done? | Code + tests + PR + review + deploy + demo + Datta QA green flag |
| Single backlog rule? | ONE backlog, PO owns it, epics enter sprint only via Saturday planning |
| Blocker epic? | Impediment → assigned to Datta, cascading 1/3/7 day SLA, BLOCK-NNN prefix |
| Blocker SLA cascade? | T+1 nudge → T+3 priority bump + downstream impact report → T+7 HARD PAUSE (zero LLM spend) |
| What happens at T+7 hard pause? | Dependent epics frozen, token tracker rejects LLM calls on those paths, agents reassigned or idle |
| Dev environment URL? | `dev.rootine.app` (auto-deploy on merge to main) |
| Prod environment URL? | `rootine.app` (manual promotion, Datta approves) |
| QA delay? | 1-sprint — Sprint N features QA'd in Sprint N+1, promoted end of N+1 |
| Versioning? | Semantic: vMAJOR.MINOR.PATCH (MAJOR=PC, MINOR=sprint, PATCH=hotfix) |
| Rollback trigger? | Datta types `rollback production` in Slack — never automatic |
| Sprint 0? | Infra-only sprint before S01 — VPS, environments, CI/CD, no feature code |
| Retro action items owned by? | Datta (as Scrum Master) — tracked in `sprints/action-items.md` |
| Action item stale threshold? | Open 3+ sprints = escalated as recurring problem |
| Who can cancel a sprint? | Datta only — Slack `cancel sprint` is user-ID restricted (PLAT-013) |
| Max sprint cancellations per PC? | 1 — second requires PC viability review |
| Cancelled sprint velocity? | NOT counted in rolling velocity average |
| Mid-sprint scope swap rule? | 1-in-1-out, equal-or-smaller points, outgoing epic must have zero commits (Section 28.3) |
| Max swaps per sprint? | 2 — a third indicates bad planning, triggers retro action item |
| Who decides technical architecture? | Lead Dev |
| Who decides product scope? | PO Agent |
| Who decides everything else? | Datta (escalation target, final say) — see Section 29.2 |
| Escalation SLA? | Level 2 (owner) 4h, Level 3 (Datta) 24h |
| Decision log location? | `sprints/S-NN/decisions.md` — every Level 3 escalation logged |
| Empirical process control? | Decisions cite data first; gut calls are labelled and revisited next retro (§29.9) |
| Sustainable pace ceiling? | AI 35 hrs/sprint, human 30 hrs/sprint, Datta ≤10 hrs/week — overtime is never the fix (§21.5) |
| Definition of Done (canonical)? | Bible §30 — 14-item checklist + category additions + anti-patterns |
| Definition of Ready (canonical)? | Bible §31 — 12-item checklist + DoR gate pseudocode |
| Who is the customer? | Placeholder during scaffolding phase — to be set at PC-02 kickoff (§1.2) |
| Sprint commitment vs forecast? | We use FORECAST language — sprint scope is a forecast, not a contract (§31, PLAT-006) |
| Backlog refinement cadence? | Async — PO posts a refinement batch every Wednesday 14:00 CST in `#rootine-planning` (PLAT-006 §3.6.5) |
| Retro rule — blameless? | Written retros cite ROLES, never individuals (PLAT-010 §5) |
| Retro rule — Vegas? | Raw retro discussion stays in retro; only the written summary + action items are public (PLAT-010 §5) |
| Velocity tracking file? | `sprints/velocity.json` — append-only, cancelled sprints excluded from rolling avg (PLAT-010 §6) |
| PC-level burndown? | `year-{year}/PC-{pc}/burndown.md` — updated every Saturday by PO (PLAT-010 §7) |
| Estimation calibration? | `sprints/estimation-log.md` — median drift >25% triggers retro discussion (PLAT-010 §8) |
| Demo template? | `year-{year}/.sdd/templates/demo-script.md` — every epic gets a 5-min structured demo |
| Tech debt register? | `year-{year}/tech-debt.md` — append-only, PO scans Mondays, promotes to TechMain epics |

---

## 18. Infrastructure & Platform Specs

The following specs were created during the infrastructure planning phase (April 2026). They define the VPS setup, token monitoring, model fallback, Slack command interface, and agent state management. These are pre-requisites — they must be implemented before agents begin coding Rootine features.

### 18.1 Spec Index

| Spec ID | Title | Location | Priority | Owner |
|---|---|---|---|---|
| INFRA-001 | VPS Infrastructure Setup | `specs/infrastructure/INFRA-001-vps-setup.spec.md` | S2 | Datta |
| PLAT-001 | Token Usage Monitoring & Alerts | `specs/platform/PLAT-001-token-monitoring.spec.md` | S2 | Lead Dev |
| PLAT-002 | Tiered Model Fallback System | `specs/platform/PLAT-002-model-fallback.spec.md` | S2 | Lead Dev |
| PLAT-003 | Slack Command Interface & Agent Communication | `specs/platform/PLAT-003-slack-commands.spec.md` | S2 | Lead Dev |
| PLAT-004 | Agent State Management | `specs/platform/PLAT-004-agent-state.spec.md` | S2 | Lead Dev |
| PLAT-005 | Epic Traceability & Spec-Code Sync | `specs/platform/PLAT-005-traceability.spec.md` | S2 | Lead Dev |
| PLAT-006 | Sprint Ceremonies, Story Points & Work Schedules | `specs/platform/PLAT-006-sprint-ceremonies.spec.md` | S1 | PO Agent |
| PLAT-007 | New Hire Onboarding System | `specs/platform/PLAT-007-onboarding.spec.md` | S2 | PO Agent |
| PLAT-008 | Epic Categorization System | `specs/platform/PLAT-008-epic-categories.spec.md` | S2 | PO Agent |
| PLAT-009 | Testing Standards & SonarQube Quality Gate | `specs/platform/PLAT-009-testing-quality.spec.md` | S2 | Lead Dev |
| PLAT-010 | Continuous Improvement & Enhanced Retrospective | `specs/platform/PLAT-010-continuous-improvement.spec.md` | S1 | Datta/PO |
| PLAT-011 | Environment Strategy & Deployment Pipeline | `specs/platform/PLAT-011-environments.spec.md` | S1 | Lead Dev |
| PLAT-012 | Rollback Mechanism | `specs/platform/PLAT-012-rollback.spec.md` | S1 | Lead Dev |

### 18.2 Dependency Order
```
INFRA-001 (VPS Setup)
    └── PLAT-004 (Agent State) — needs VPS running
        └── PLAT-001 (Token Monitoring) — needs state manager
        └── PLAT-002 (Model Fallback) — needs state manager + token tracker
            └── PLAT-003 (Slack Commands) — needs all above to control
    └── PLAT-005 (Traceability) — git hooks + CI checks, independent of agent stack
```

### 18.6 Traceability Rules (PLAT-005)

Every change in the system is traceable to an epic. Enforced at 3 layers:

| Layer | What it checks | When |
|---|---|---|
| **Git hook** (`commit-msg`) | Commit has epic ref: `type(ROOT-NNN): desc` | Every commit (local) |
| **GitHub Actions** (`pr-validation.yml`) | All commits have refs, branch has ref, spec updated | Every PR (CI) |
| **PO Agent audit** | Spec files-touched matches actual git changes | Daily at 08:00 |

**Spec-Code Sync Rule:** If code files change in a PR, the epic's spec `[CHANGE LOG]` must also be updated in the same PR. Escape hatch: `[skip-spec] <reason>` in PR body (monitored — flagged if used >3x per sprint).

**Tracing commands:**
```bash
git log --grep="ROOT-041" --oneline          # all commits for an epic
git log --grep="ROOT-041" --name-only        # all files touched by an epic
git log --oneline -- src/api/reminders.ts    # which epics touched a file
```

### 18.3 VPS Decision Summary

| Option considered | Cost/mo | Decision |
|---|---|---|
| 1 vCPU / 4 GB RAM | $6 | Too small — OOM during concurrent builds |
| 2 vCPU / 8 GB RAM | $8.50 | Tight — risky during SonarQube scan |
| **4 vCPU / 16 GB RAM** | **$12** | **Selected** — handles builds + tests + SonarQube comfortably |
| 3 separate VPS (1 per agent) | $18 | Rejected — breaks shared filesystem required by SDD |

### 18.4 Tiered Fallback Summary

| Tier | Models | Cost | Quality | Trigger |
|---|---|---|---|---|
| Tier 1 (Primary) | Sonnet 4.6 + GPT-4.1 + GPT-4o mini | ~$250/yr | 100% | Default |
| Tier 2 (Fallback) | DeepSeek-V3 + Gemini Flash | ~$30/yr | 80-85% | Datta command or daily cap hit |
| Tier 3 (Emergency) | Qwen2.5-Coder-7B (local Ollama) | $0 | 60-70% | All cloud APIs down |

### 18.5 Annual Budget Estimate

| Item | Cost/year |
|---|---|
| VPS (Hostinger 4vCPU/16GB) | $144 |
| API — Tier 1 primary | $200–350 |
| API — Tier 2 fallback | $10–50 |
| GitHub Actions | Free (2000 min/mo) |
| Expo EAS builds | Free (30 builds/mo) |
| Vercel hosting | Free tier |
| **Total** | **$354–544/year (~$30–45/month)** |

---

## 19. Project File Structure

The project has two layers: a **planning layer** (this machine) and a **runtime layer** (VPS + GitHub). The runtime layer's PCs, epics, and timeline are NOT pre-scaffolded — they are created when Datta provides project documentation (tech diagrams, workflows, business docs) and approves the PC scope.

```
Project Crew/                            # Planning & reference (this machine)
├── rootine_project_bible.md             # This document
├── Datta Project Crew.pdf               # Original PDF
└── specs/                               # Platform & infra specs (shared across all PCs)
    ├── infrastructure/
    │   └── INFRA-001-vps-setup.spec.md
    └── platform/
        ├── PLAT-001 through PLAT-012    # Platform specs (ceremonies, testing, etc.)

{project-repo}/                          # Deployed to VPS + GitHub (created per project)
├── .sdd/
│   ├── project.config.yaml
│   ├── agent.limits.yaml
│   ├── coding-standards.md
│   ├── tech-stack.yaml
│   └── onboarding/                      # Role-specific onboarding guides
├── .github/
│   ├── ISSUE_TEMPLATE/epic.md
│   ├── PULL_REQUEST_TEMPLATE/
│   └── workflows/                       # CI/CD pipelines
├── .env.template
├── .gitignore
└── PC-NN/                               # Created when Datta provides project docs
    ├── pc.manifest.yaml                 # PC scope, sprint goals, deliverables
    ├── mvp-statement.md                 # Datta's 3-sentence MVP
    ├── context-summary.md               # Written at PC close (max 200 lines)
    ├── design-meetings/
    ├── sprints/S01/retro.md ... SNN/retro.md
    ├── epics/
    ├── specs/
    │   ├── INDEX.md                     # Routing table — PO updates only
    │   ├── backlog/
    │   ├── in-progress/
    │   ├── finished/
    │   └── interrupt/
    └── tech-upgrades/suggestions.md
```

**How a PC starts:** Datta provides project documentation (business requirements, tech diagrams, workflows) → PO + Lead Dev decompose into epics → PO creates `pc.manifest.yaml` with sprint goals → Datta approves → Sprint 0 (infra setup if first PC) → Sprint 1 begins.

---

## 20. Sprint Ceremonies & Agile Framework

The system follows a complete Agile/Scrum framework adapted for AI + human teams. All ceremonies are conducted asynchronously via Slack.

### 20.1 Ceremony Calendar (Sprint: Sunday → Saturday)

| Day | Time | Ceremony | Channel | Participants |
|---|---|---|---|---|
| **Saturday** (sprint end) | 3:00 PM | Sprint Review + Demos + Deploy | `#rootine-dev` | PO presents, Datta reviews |
| **Saturday** (sprint end) | 3:30 PM | Sprint Retrospective | `#rootine-dev` | All team, Datta owns action items |
| **Saturday** (sprint end) | 4:00 PM | Sprint Planning (next sprint) | `#rootine-planning` | PO assigns, Datta approves |
| **Sunday** (sprint start) | 10:00–11:00 AM | Sunday Kickoff (tech spec grooming) | `#rootine-planning` | All agents + Datta |
| **Every day** | 8:05 AM | Daily Standup | `#rootine-dev` | All agents post, Datta reads |
| **Every day** | 6:00 PM | Daily Report + Burndown | `#rootine-dev` | PO posts |

**Why weekends for ceremonies?** Datta (Advisor) works a separate day job on weekdays. Saturday/Sunday ceremonies let him participate in all major Agile events — reviews, retros, planning, and grooming. AI agents work all 7 days of the sprint.

### 20.2 Sprint Planning Flow (Saturday 4:00 PM)

1. **PO prepares** — selects epics from single backlog, writes business spec per epic, proposes sprint goal
2. **PO posts to `#rootine-planning`** — sprint goal, epic table (ID, title, points, owner), total points vs trailing velocity
3. **Lead Dev reviews** — validates technical feasibility, flags >5pt epics for splitting, confirms dependency order
4. **Datta reviews** — confirms sprint goal aligns with PC MVP, approves or adjusts
5. **PO finalizes** — updates INDEX.md, creates spec skeletons, posts final sprint forecast (a forecast, not a commitment — modern Scrum language)

### 20.3 Sunday Kickoff / Technical Grooming (Sunday 10:00–11:00 AM)

1. Each agent reads their assigned epics' business spec (from Saturday planning)
2. Each agent writes/updates the technical spec (≤1 hour)
3. Lead Dev reviews ALL tech specs — approves or requests changes
4. Datta participates — approves direction, asks clarifying questions
5. PO approves business alignment
6. **No agent writes code until tech spec is approved by Lead Dev AND PO**

### 20.4 Daily Standup Format (Every day 8:05 AM)

Each agent posts:
```
*[Agent Name] — Daily Standup*
  Yesterday: [what was completed]
  Today: [what's planned]
  Blockers: [any blockers or "None"]
  Hours worked yesterday: N/5
```

PO follows with burndown summary:
```
*PO Standup Summary*
  Sprint S-NN | Day N of 5 | Goal: [sprint goal]
  Burndown: X pts planned → Y pts remaining → [ON TRACK / AT RISK / BEHIND]
  Blockers: [count and details]
```

### 20.5 Sprint Review (Saturday 3:00 PM)

PO posts completed epics with demo links, rolled-over epics with reasons, velocity achieved vs planned, and burndown chart. Datta reviews and issues green flags for completed work.

### 20.6 Single Backlog Rule

- ONE backlog for the entire project — `specs/backlog/`
- PO is the sole owner
- Epics enter a sprint ONLY during Saturday Sprint Planning
- Mid-sprint additions only for S1 (prod bugs) and S2 (blocking) via interrupt slots
- No agent may self-assign from the backlog

### 20.7 Slack Channels

| Channel | Purpose |
|---|---|
| `#rootine-dev` | Standups, daily reports, reviews, retros, alerts, Datta commands |
| `#rootine-planning` | Sprint planning (Saturday), Sunday kickoff, tech spec reviews, epic discussions |

---

## 21. Story Points & Work Schedules

### 21.1 AI Agent Work Schedule — 5 hours/day, 7 days/week

```
08:00–09:00  Work block 1 (1 hour)
09:00–12:00  BREAK (3 hours — no API calls)
12:00–13:00  Work block 2 (1 hour)
13:00–16:00  BREAK (3 hours)
16:00–17:00  Work block 3 (1 hour)
17:00–20:00  BREAK (3 hours)
20:00–21:00  Work block 4 (1 hour)
21:00–22:00  Work block 5 (1 hour — wrap-up)
22:00        Work window closes

Total: 5 effective hours/day × 7 days = 35 hours/sprint
```

### 21.2 Human Agent Work Schedule — 6 hours/day
- Flexible schedule, no enforced blocks
- 6 hours/day when actively developing, 30 hours/sprint
- Primary role (Datta) remains Advisor — develops only when choosing to

### 21.3 Story Point Scale

| Points | AI Agent Time | Human Agent Time | Complexity |
|---|---|---|---|
| 1 | ~1 hour | ~2-3 hours | Trivial — config change, copy fix, small bug |
| 2 | ~2 hours | ~half day | Small — single endpoint, simple UI component |
| 3 | ~3 hours | ~1 day | Medium — feature with tests, multi-file change |
| 5 | ~5 hours (1 full day) | ~2 days | Large — full feature end-to-end |

### 21.4 Epic Sizing Rules

- **Maximum 5 points per epic — no exceptions**
- If >5 points → PO MUST split into independently deliverable sub-epics
- Points include full lifecycle: groom → tech spec → code → test → PR → review → deploy → demo → acceptance → done
- Velocity = completed points/sprint (rollovers don't count)
- PO uses trailing 3-sprint average velocity to forecast next sprint

### 21.5 Sustainable Pace — Capacity Is a Maximum, Not a Target

Agile Principle #8: "Agile processes promote sustainable development. The sponsors, developers, and users should be able to maintain a constant pace indefinitely."

This framework enforces that principle with hard rules, not hopes.

**Capacity ceilings (not goals):**

| Role | Ceiling | Rule |
|---|---|---|
| AI agent | 5 hrs/day × 7 days = 35 hrs/sprint | Token tracker HARD-STOPS calls past this. No overtime. |
| Human developer | 6 hrs/day flex = 30 hrs/sprint | Self-reported, honor system — but enforced by the rules below. |
| Datta (Advisor) | ≤10 hrs/week on framework work | Beyond this is a flag — your day job and life come first. |

**Anti-crunch rules (load-bearing):**

1. **Overtime is never a solution to over-scoping.** If a sprint needs >30 hr/human or >35 hr/agent to succeed, the sprint is over-scoped. The correct responses, in order:
   - Mid-sprint swap (§28.3) — drop one epic, pick a smaller one
   - Rollover — explicitly carry the epic to next sprint, no stigma
   - Sprint cancellation (PLAT-013) if the goal itself is unreachable
   - **Never:** "just one more push this weekend"

2. **No guilt-trip language.** Nobody in this framework may use phrases that pressure overwork — "can you just," "quick favor," "shouldn't take long," "only if you have time tonight." If PO Agent produces these in a daily report, it is a bug. File it as a Prod Issue.

3. **Weekend work is a warning, not a badge.** If a human developer logs weekend hours more than twice in a PC, retro flags it as a recurring problem. Either scope is too aggressive or estimates are too optimistic. Data goes in the estimation calibration log (PLAT-010).

4. **"Vacation" is not a dirty word.** Datta or any human developer can declare themselves unavailable for N days. The scheduler treats those days as zero capacity. Sprint scope shrinks accordingly. No guilt, no make-up.

5. **Agents have rest too — it's called the breaks.** The 1-hour-on / 3-hour-off pattern exists for a reason: it caps token burn and makes the system predictable. Removing breaks to "get more done" is a foot-gun. The pattern is locked unless changed in a retro via a data-backed proposal.

6. **Token cap is the final guardrail.** When an agent hits daily cap, it stops. No "just one more call." PLAT-001 enforces this; no one can override without a Slack command logged by Datta.

**Why this matters for the template:**
A starter template that quietly allows crunch will eventually be used by a solo founder pulling 80-hour weeks, blaming themselves for not keeping up. The rules above exist to make overwork visibly wrong, not quietly normal.

### 21.6 Definition of Ready / Definition of Done

Moved to canonical top-level sections:
- **Definition of Ready** → see [Section 31](#31-definition-of-ready)
- **Definition of Done** → see [Section 30](#30-definition-of-done)

These are now sprint-level gates enforced by PO Agent. Every epic must pass Section 31's checklist before entering a sprint, and every epic must pass Section 30's checklist before moving to `finished/`.

### 21.7 Epic Lifecycle (Full — from backlog to done)

```
SATURDAY (Sprint close + Planning):
  3:00 PM  Sprint Review (PO presents, Datta reviews + green flags)
  3:30 PM  Sprint Retro (all team, Datta owns action items)
  4:00 PM  Sprint Planning for next sprint
  PO selects from backlog → proposes in #rootine-planning
  Lead Dev validates feasibility → Datta approves sprint goal
  PO assigns, writes business specs, updates INDEX.md

SUNDAY (Kickoff — 10:00-11:00 AM):
  Agent reads business spec → writes technical spec (≤1 hour)
  Lead Dev reviews + approves tech spec
  Datta participates in grooming
  PO approves business alignment
  Status: READY FOR DEV

MON–THU (Development — work blocks):
  Agent codes per tech spec + standards
  Agent writes tests → raises PR
  Lead Dev reviews → agent addresses feedback
  PR merged → auto-deploy to staging
  Agent updates spec [CHANGE LOG]

THU–FRI (Demo + Acceptance):
  PO runs demo script → DEMO_PASSED or bug sub-task
  Datta QA on staging → green flag
  PO moves spec to finished/ → DONE

FRIDAY (Sprint Close):
  3:00 PM Sprint Review → 3:30 PM Retro → 4:00 PM Next Sprint Planning
  Unfinished epics → rollover protocol (severity re-evaluation)
```

---

## 22. New Hire Onboarding

Every role (AI or human) has a dedicated onboarding guide at `.sdd/onboarding/{role}.md`. Guides are structured in 4 phases and kept under 200 lines each.

### 22.1 Onboarding Guides

| Role | Guide File | Read Scope | First Action |
|---|---|---|---|
| Advisor (Datta) | `onboarding/advisor.md` | PC manifest, INDEX.md, PO report, budget | Review current sprint, QA staged epics |
| PO Agent | `onboarding/po-agent.md` | Full config, all specs, INDEX.md | Run severity triage, post daily report |
| Senior Developer | `onboarding/senior-developer.md` | Architecture, standards, all tech specs, retros | Review open PRs, verify INDEX.md |
| Associate Developer | `onboarding/associate-developer.md` | Own epic spec ONLY, INDEX.md, standards | Read assigned epic, write tech spec |
| Human Developer | `onboarding/human-developer.md` | Standards, tech stack, PC manifest | Set up local env, claim first epic |
| AI Agent (generic) | `onboarding/ai-agent.md` | Agent limits, work schedule, model routing | Verify API key, test first call |

### 22.2 Onboarding Phases (all roles)
1. **CONTEXT** (≤30 min) — read role-specific documents
2. **SETUP** (≤1-2 hours) — tools, access, API keys, Slack channels
3. **FIRST DAY** — produce a visible output (standup, spec review, or code)
4. **ONGOING** — daily/weekly/PC-boundary reference material

### 22.3 PO Verification
PO runs an onboarding checklist for every new team member and logs completion to `status.log`.

---

## 23. Epic Categorization

All work is classified into exactly one of 6 categories. This replaces the previous "Epic Types" section.

### 23.1 Categories

| Category | Label | Max Pts | Due Date? | Code Output? | Default Owner |
|---|---|---|---|---|---|
| **Task** | `task` | 5 | No (sprint end) | YES | Lead Dev or Associate |
| **Story** | `story` | 5 | No (sprint end) | NO (document) | Lead Dev preferred |
| **Prod Issue** | `prod-issue` | 5 | **YES (mandatory)** | YES (hotfix) | **Lead Dev always** |
| **TechMain** | `tech-maintenance` | 5 | No (sprint end) | YES | Lead Dev preferred |
| **Blocker** | `blocker` | 3 | **YES (≤3 days)** | Usually NO | **Datta always** |
| **Feature** | `feature` | **>10 (container)** | Optional | YES (children) | Split across team |

### 23.2 Key Rules

- **Task:** Most common. Coding-required. Full lifecycle: groom → spec → code → test → deploy → demo → done.
- **Story:** Analysis/research only. Produces a document or decision, NOT code. Often precedes a Task.
- **Prod Issue:** Production bug. **Must have a due date.** S1: same day. S2: 2 business days. S3: within sprint. Lead Dev always owns.
- **TechMain:** Tech debt, dependency upgrades, CVE fixes. Usually S4, elevated to S2 if CVSS ≥ 7.
- **Blocker:** Impediment that blocks a developer or PO. **Always assigned to Datta.** Due date ≤3 calendar days from creation. Datta resolves (decision, access, clarification). If unresolved in 3 days, Datta must provide a workaround. Flagged in retro if recurring.
- **Feature:** Container for multiple child epics. Total can exceed 10 pts, but each child epic is ≤5 pts and independently deliverable. Can span sprints.

### 23.3 Feature Decomposition Example
```
Feature: FEAT-001 "Push Notification System" (18 pts total)
  ├── Story:  ROOT-051 "Design push architecture"        (2 pts, Lead Dev, S-03)
  ├── Task:   ROOT-052 "Push notification service"        (5 pts, Lead Dev, S-03)
  ├── Task:   ROOT-053 "iOS push integration"             (3 pts, Associate, S-03)
  ├── Task:   ROOT-054 "Android push integration"         (3 pts, Associate, S-03)
  └── Task:   ROOT-055 "Push notification settings UI"    (5 pts, Associate, S-04)
```

### 23.4 Prod Issue Due Date Matrix
| Severity | Max Resolution Time | Escalation |
|---|---|---|
| S1 — Critical | Same day (hours) | @datta immediately. Lead Dev drops everything. |
| S2 — High | 2 business days | Lead Dev picks up next. Daily updates. |
| S3 — Medium | Within sprint | Normal sprint flow. |

---

## 24. Testing Standards & Quality Gate

Every PR must pass automated testing and SonarQube quality gate before merge.

### 24.1 Test Pyramid

| Layer | Tool | Scope | Runs When |
|---|---|---|---|
| Unit tests | Jest | Business logic, services, utils | Every PR (CI) |
| Integration tests | Supertest + Jest | API endpoints + real PostgreSQL | Every PR (CI) |
| UI component tests | React Testing Library | Interactive components | Every PR (CI) |
| E2E tests | Detox | Critical user flows (mobile) | Release builds only |

### 24.2 Coverage Requirements

| Metric | Threshold | Enforced by |
|---|---|---|
| Line coverage (new code) | **≥ 80%** | SonarQube quality gate |
| Branch coverage (new code) | **≥ 70%** | SonarQube quality gate |
| Duplicated lines (new code) | **≤ 3%** | SonarQube quality gate |
| New bugs | **0** | SonarQube quality gate |
| New vulnerabilities | **0** | SonarQube quality gate |
| New code smells | **0** (A rating) | SonarQube quality gate |

### 24.3 Test Requirements Per Epic Type

| Epic Type | Unit | Integration | UI | E2E | Regression |
|---|---|---|---|---|---|
| Task | Required (80%+) | All endpoints | All components | If critical flow | — |
| Story | N/A | N/A | N/A | N/A | — |
| Prod Issue | Required | Required | If UI-related | If critical flow | **Required** |
| TechMain | Update existing | Update if changed | Update if changed | — | — |
| Feature children | Per child rules | Per child rules | Per child rules | At least 1 E2E | — |

### 24.4 Required Test Cases Per Endpoint
| Method | Minimum Tests |
|---|---|
| POST | Happy path (201), validation error (400), auth failure (401) |
| GET | Happy path (200), not found (404), auth failure (401) |
| PATCH | Happy path (200), not found (404), validation error (400), auth (401) |
| DELETE | Happy path (200/204), not found (404), auth failure (401) |

### 24.5 Required Test Cases Per UI Component
| Component Type | Minimum Tests |
|---|---|
| Form | Render, validation errors, successful submit, loading state, server error |
| List | Render items, empty state, loading state |
| Modal | Open, close, confirm action, cancel |
| Auth-gated | Authenticated view, unauthenticated redirect |

### 24.6 SonarQube Setup
- Runs on VPS as Docker container (3 GB RAM allocated)
- PR-level scan: every PR via GitHub Actions
- Weekly full scan: Friday 5 PM — PO posts results to `#rootine-dev`
- CVSS scores from vulnerability findings feed into PO's severity triage

### 24.7 Integration Test Rule
**Never mock the database.** Integration tests use a real PostgreSQL container. This catches real query issues, migration problems, and constraint violations that mocks would hide.

---

## 25. Continuous Improvement & Retrospective System

The retrospective is the feedback loop that improves everything else. Datta serves as both Advisor AND Scrum Master — he owns all action items from retros.

### 25.1 Enhanced Retro Format (Saturday 3:30 PM)

Every team member posts retro input with: what-went-well, what-didn't, what-can-improve, blockers.
PO compiles into a summary with categorized findings and action items.

### 25.2 Action Item Tracking

- Action items persist across sprints in `sprints/action-items.md`
- Every action item has: ID (AI-NNN), owner (Datta), due date, status
- Reviewed at START of every retro
- Open for 3+ sprints = escalated as recurring problem
- Methodology changes are applied by updating Project Bible + relevant spec

### 25.3 Retro Health Metrics (tracked sprint-over-sprint)

| Metric | Goal |
|---|---|
| Velocity trend | Stable or improving |
| Estimation accuracy | ≥85% |
| Rollover rate | ≤15% |
| Blocker frequency | Decreasing |
| Action item closure (within 2 sprints) | ≥80% |
| QA turnaround (staging deploy → Datta QA) | ≤24 hours |

**Full spec:** `specs/platform/PLAT-010-continuous-improvement.spec.md`

---

## 26. Environment Strategy & Deployment Pipeline

### 26.1 Two Environments

| Field | Development | Production |
|---|---|---|
| URL | `dev.rootine.app` | `rootine.app` |
| API | `api-dev.rootine.app` | `api.rootine.app` |
| Deploy trigger | Auto on merge to `main` | Manual — Datta approves promotion |
| Git branch | `main` | `release/vN.N.N` (tagged) |
| Database | Seed/test data, can be wiped | Real user data, never wiped |

### 26.2 1-Sprint QA Delay

Code deploys to Dev in Sprint N → Datta QA's in Sprint N+1 → promotes to Production end of Sprint N+1. This delay is ALWAYS maintained — no shortcuts except the S1 hotfix path.

### 26.3 Semantic Versioning

```
vMAJOR.MINOR.PATCH
  MAJOR = PC boundary (v1.x.x = PC-01, v2.x.x = PC-02)
  MINOR = sprint promotion (v1.1.0 = Sprint 1, v1.2.0 = Sprint 2)
  PATCH = hotfix (v1.1.1 = hotfix on Sprint 1 release)
```

### 26.4 Hotfix Path (bypasses delay for S1 prod bugs)

Fix on `hotfix/ROOT-NNN` → fast-track PR → deploy to Dev → quick Datta QA (within hours) → cherry-pick to release branch → deploy to Prod → tag vX.X.PATCH.

**Full spec:** `specs/platform/PLAT-011-environments.spec.md`

---

## 27. Rollback Mechanism

### 27.1 Philosophy

Every production promotion creates a restore point. Rollback = revert to the previous release tag. Datta always approves — no automatic rollbacks.

### 27.2 Rollback by Layer

| Layer | Method | Time |
|---|---|---|
| Web (Vercel) | Instant rollback to previous deployment | < 1 min |
| API | Redeploy previous release tag | < 3 min |
| Mobile | OTA update to previous JS bundle (Expo Updates) | < 5 min |
| Database | Reverse migration OR backup restore | 5–15 min |

### 27.3 Triggers

- **Slack command:** Datta types `rollback production` → confirmation dialog → `confirm rollback`
- **Health check alert:** Automated post-deploy check alerts Datta if web/API return non-200
- **Critical bug report:** Datta decides after user report

### 27.4 Key Rules

- Every migration MUST have a `down()` function for reverse migration
- Pre-deploy backup is mandatory (PLAT-011)
- Pre-rollback backup is also taken (safety net for the rollback itself)
- Rollback is tagged with PATCH version increment (v1.2.0 → v1.2.1)
- All rollback events logged in CHANGELOG.md and sprint rollback log

**Full spec:** `specs/platform/PLAT-012-rollback.spec.md`

---

## 28. Sprint Cancellation & Mid-Sprint Scope Change

### 28.1 Two Different Protocols

Mid-sprint interruptions fall into two distinct categories. Picking the wrong one wastes work or masks a real problem.

| | **Sprint Cancellation** | **Scope Swap** |
|---|---|---|
| Used when | Sprint goal is invalid, dependency broken, >60% scope blocked | A single urgent epic needs to enter mid-sprint |
| Authority | Datta only | PO Agent (with Datta notified) |
| Scope | Whole sprint halts | One epic in, one epic out |
| Velocity impact | Excluded from average | Counted normally |
| Ceremony impact | No demo, no review, post-mortem only | Normal Saturday ceremonies |
| Frequency limit | Max 1 per PC | Max 2 swaps per sprint |

### 28.2 Sprint Cancellation (summary — full spec in PLAT-013)

- **Authority:** Datta only. Slack command `cancel sprint` is user-ID restricted.
- **Valid triggers:** sprint goal obsolete, critical dependency broken, S1 prod incident eating >2 days, scope collapse (>60% blocked), weekly token cap halt, Datta unavailable >3 days when gates are needed.
- **Invalid triggers:** single blocker (use Blocker epic), underestimation (use swap), one agent underperforming (reassign), priority reshuffle (use swap).
- **Flow:** recommendation in `#rootine-planning` → Datta accept/decline within 4h → PO halts agents → epics return to backlog → post-mortem within 24h → no demo/review/retro.
- **Velocity rule:** cancelled sprints are excluded from the rolling velocity average.
- **Max cancellations per PC:** 1. A second requires Datta to also review PC viability.

See `specs/platform/PLAT-013-sprint-cancellation.spec.md` for triggers, Slack command flows, post-mortem template, and audit trail format.

### 28.3 Mid-Sprint Scope Swap — The 1-in-1-out Rule

A swap is the ONLY way to add new scope to an in-flight sprint. You cannot add without removing. This prevents scope creep and protects the sprint goal.

**Rules:**
1. **Equal or smaller points.** The incoming epic's story points must be ≤ the outgoing epic's story points. Never swap a 2-point epic out for a 5-point epic.
2. **Outgoing epic must be untouched.** If work has started on an epic (any commit against it), it cannot be swapped out — it must be finished, extended into next sprint, or explicitly cancelled by Datta.
3. **Same category preferred.** Swap Task→Task, Story→Story. Cross-category swaps (e.g., Task→Prod Issue) require Datta's approval.
4. **Sprint goal unaffected.** If the swap would change the sprint goal, it is not a swap — it is a cancellation (Section 28.2).
5. **Max 2 swaps per sprint.** A third swap request indicates the sprint was poorly planned; trigger a retrospective action item instead.
6. **No swaps in the last 2 days** of a sprint. Use next sprint's planning instead.

**Flow:**
```
Step 1 — REQUEST
  Requester posts in #rootine-planning:
    "Swap request: IN = <new-epic-id> (N pts), OUT = <existing-epic-id> (N pts).
     Reason: <justification>. Sprint goal impact: <none | minor | major>."

Step 2 — PO VALIDATION (within 2 hours)
  PO Agent checks:
    ✓ Incoming points ≤ outgoing points
    ✓ Outgoing epic has zero commits against it
    ✓ Same category (or flag for Datta)
    ✓ Sprint goal unaffected
    ✓ Swap count < 2 for this sprint
    ✓ Not in the last 2 days of sprint
  If all pass → proceed to Step 3.
  If any fail → reject with reason, suggest correct protocol.

Step 3 — DATTA NOTIFICATION (not approval — notification)
  PO posts to #rootine-planning:
    "Swap approved: <in> replaces <out>. Capacity unchanged. @Datta FYI."
  Datta has 1 hour to veto. Silence = confirmed.

Step 4 — EXECUTION
  PO updates INDEX.md:
    - Outgoing epic: BACKLOG (note: "Swapped out of S-NN")
    - Incoming epic: IN_PROGRESS, owner assigned, tech spec grooming triggered
  PO posts assignment to the owner.
  PO appends to sprints/S-NN/swap-log.md:
      swap_n: 1
      date: YYYY-MM-DD
      in: <id> (N pts)
      out: <id> (N pts)
      reason: <text>
      approved_by: PO Agent (auto) | Datta (cross-category)
```

### 28.4 What a Swap Is NOT

- **Not a mid-sprint bug fix.** Prod bugs use the Prod Issue category (PLAT-008) and live in `specs/interrupt/`. They do not require a swap because they are tracked separately from the sprint forecast.
- **Not a replanning.** If multiple swaps are being requested, the sprint was wrong — cancel it.
- **Not a silent add.** Every swap MUST be logged in `swap-log.md` for the retro.

### 28.5 Swap Log Retrospective Signal

At every Saturday retro, the PO reports the total swap count across the sprint:

- **0 swaps:** Healthy planning. Continue.
- **1 swap:** Normal. Note the reason.
- **2 swaps:** Warning signal. Discuss root cause in retro.
- **3+ swap *requests*** (even if declined): Critical signal. Action item: improve planning accuracy in Saturday Sprint Planning ceremony.

---

## 29. Conflict Resolution & Escalation Matrix

### 29.1 Principle

Every decision has exactly one owner. Disagreements are resolved by the owner, not by consensus, vote, or debate. If two people disagree, the owner listens then decides. Work continues.

### 29.2 Decision Authority Matrix

| Decision type | Owner | Example |
|---|---|---|
| **Technical architecture** (stack choices, patterns, refactors) | Lead Dev | "Should we use Drizzle or Prisma?" |
| **Code review outcomes** (approve, reject, block) | Lead Dev | "This PR's abstraction is wrong." |
| **Product scope** (what ships, what doesn't, feature priorities) | PO Agent | "Reminders before categories, or after?" |
| **Epic assignment** (who works on what, when) | PO Agent | "Give PLAT-004 to Associate, not Lead Dev." |
| **Sprint scope** (what's in the sprint, what's out) | PO Agent | "Can we add PLAT-014 this sprint?" |
| **Sprint cancellation** | Datta | "Is this sprint still viable?" |
| **Cross-category swaps** | Datta | "Swap a Task for a Prod Issue?" |
| **PC goals & MVP definition** | Datta | "Is push notifications in scope for PC-01?" |
| **Budget / token limits** | Datta | "Raise daily token cap?" |
| **Tech stack additions** (new dependency, new service) | Lead Dev proposes, Datta approves | "Add Redis?" |
| **Agent model choices** (Sonnet vs GPT-4.1 vs Ollama) | Lead Dev | "Switch Associate to DeepSeek?" |
| **Deadlines** | PO Agent | "Sprint goal due Friday." |
| **Rollback trigger** | Datta | "Rollback prod now?" |
| **Hiring / role changes** | Datta | "Bring in a second human dev?" |
| **Repo structure & branching** | Lead Dev | "Monorepo vs split?" |
| **External integrations** (Slack, GitHub, Vercel settings) | Datta | "Change Slack webhook?" |
| **Retrospective action items** | Datta (Scrum Master role) | "Assign AI-007 to whom?" |

### 29.3 Escalation Path

```
Level 1 — DIRECT DISCUSSION (≤30 min)
  Two agents disagree. They discuss in the relevant Slack channel.
  If they reach alignment → done. No escalation.
  If they don't → Level 2.

Level 2 — OWNER DECIDES (≤4 hours)
  The owner from Section 29.2 makes the call.
  Posts decision in #rootine-planning with one-line rationale.
  Decision is final unless escalated to Level 3.
  Work resumes.

Level 3 — DATTA OVERRIDE (≤24 hours)
  Any agent can escalate to Datta if they believe the owner's decision
  violates the Project Bible or will harm the MVP.
  Escalation format in #rootine-planning:
    "Escalation to Datta. Decision: <what>. Owner: <who>. My concern: <why>.
     Bible reference: <section or spec>."
  Datta decides within 24 hours.
  Datta's decision is final and is logged as an ADR-like entry in
  sprints/S-NN/decisions.md.

Level 4 — DOES NOT EXIST
  There is no level above Datta. If Datta is unavailable and a decision is
  blocking, create a Blocker epic (PLAT-008) assigned to Datta. The Blocker
  follows the cascading 1/3/7 day SLA (see Section 29.8). Work on the blocked
  item pauses; team works on other epics where possible, and at T+7 the
  dependent epics are hard-paused with zero LLM spend.
```

### 29.4 Rules for the Owner

When you're the owner of a decision:

1. **Listen before deciding.** Read all arguments. Ask clarifying questions.
2. **Decide within the SLA.** 4 hours for most decisions; 24 hours for strategic.
3. **Explain in one sentence.** "We're going with X because Y." No essays.
4. **Post publicly.** In `#rootine-planning`, not in DMs. Everyone learns.
5. **Don't punt.** "Let's discuss more" is not a decision. If you need more info, name what info and by when.
6. **You can be wrong.** Reverse decisions when evidence shows you were wrong — that's not weakness, that's data-driven. Log the reversal.

### 29.5 Rules for the Disagreeing Party

When you disagree with an owner's decision:

1. **Disagree before the decision, not after.** Once the owner has posted the decision, you commit — even if you disagree.
2. **Escalate only for Bible or MVP violations.** Not for taste or style preferences.
3. **Bring evidence, not feelings.** "This violates PLAT-009 AC-004" is valid. "I don't like it" is not.
4. **Escalate in public.** Never in DMs to Datta. Datta wants the full context visible.
5. **Accept the final decision.** Once Datta rules at Level 3, the decision is final for this PC. You can propose it again at the next PC planning.

### 29.6 Tie-Breaker Rules for Edge Cases

| Situation | Resolution |
|---|---|
| Decision falls between two owners (e.g., architecture vs product) | Post in `#rootine-planning`, both owners tag each other, the one whose domain is *more* affected decides |
| Owner is unavailable (out, token-capped, etc.) | Escalate directly to Datta — skip Level 2 |
| Decision is urgent (S1 prod incident, <1 hour SLA) | Lead Dev decides immediately, tells Datta after |
| Decision contradicts Project Bible | Bible wins. Owner must update Bible FIRST before making the contradicting decision |
| Decision affects budget >$50/month | Escalate to Datta regardless of owner |
| Decision is irreversible (delete data, ship to App Store) | Always requires Datta approval regardless of owner |

### 29.7 Decision Log

Every Level 3 escalation produces an entry in `sprints/S-NN/decisions.md`:

```markdown
## Decision D-NN

- **Date:** YYYY-MM-DD
- **Escalated by:** <who>
- **Owner who made the disputed call:** <who>
- **Decision:** <what Datta decided>
- **Rationale:** <one paragraph>
- **Bible reference:** <section or spec>
- **Reversible?** yes | no
- **Effective:** immediate | next sprint | next PC
```

Decision logs are read at the next Saturday retro and feed into the PC close context summary.

### 29.8 Cascading SLA for Waiting on Decisions

Every blocker, escalation, or "waiting on a human" situation follows the same
cascading SLA. The total budget is 1 week. After that, work pauses until the
decision-maker responds — LLM spend on dependent paths goes to zero.

| Window | When | Action | Priority |
|---|---|---|---|
| **T+0** | Blocker / escalation raised | PO creates BLOCK-NNN, auto-assigns to owner (Datta or blocking party), due date = T+7. Immediate Slack ping. | P3 |
| **T+1 day** | 24h elapsed with no response | PO posts reminder in `#rootine-planning` tagging the owner. No priority change. | P3 |
| **T+3 days** | 72h elapsed with no resolution | PO computes downstream impact (dependent epics + sprints), broadcasts an impact report to the team. Priority bumped P3 → P2. Dependent epics flagged `at risk`. | **P2** |
| **T+7 days** | 1 week elapsed with no resolution | PO hard-pauses all dependent epics. Agents stop all LLM calls on those paths (token tracker rejects them). Priority bumped P2 → P1. If the sprint goal is now unachievable, PO recommends sprint cancellation per PLAT-013. | **P1** |

**Why the 1-week hard pause:**
Beyond 1 week without a decision from the human owner, no amount of further
agent "thinking" unblocks the work. The cheapest and most honest action is
to stop. Agents are reassigned to any unblocked epic; if none exist, they go
idle. This is a feature, not a failure — it protects the budget and makes
the blockage visible.

**Three situations that share this SLA:**
1. **Blocker epics** (PLAT-008) — developer or PO is impeded by a missing decision, access, or input
2. **Level 3 escalations** (Section 29.3) — formal disagreement escalated to Datta
3. **Dependency waits** — e.g., PC-01 S04 waiting on Datta to deliver project documentation

All three use the same tracker, same notification cadence, same hard-pause behavior at T+7. The token tracker (PLAT-001) is the enforcement point: it rejects LLM calls tagged to hard-paused epics.

### 29.9 Empirical Process Control — Decisions from Data

The framework's foundational stance: **decisions are made from observed data when data exists.** Opinion is the fallback, not the default. This is the Scrum pillar of Inspection applied to every decision in this document.

**Rules:**
1. **Data first.** Before making a decision that has existing data (velocity, burndown, token usage, SonarQube findings, retro metrics, estimation accuracy), the data must be consulted and cited.
2. **Gut calls are allowed, but labelled.** If no data exists yet, a gut-call decision is fine — but the decision log (`sprints/S-NN/decisions.md`) MUST record `"basis: gut-call"` and name what data would have been useful.
3. **Gut calls are revisited.** When relevant data arrives, every open gut-call decision is reviewed at the next retro. If data contradicts the decision, it is reversed or adjusted and logged.
4. **Opinions beat data only when the data is known-stale or known-biased.** In that case, the reasoning must be explicit: "the velocity number is misleading because sprint S-NN was cancelled, so we are using a trailing 3-sprint average that excludes it."
5. **Absence of data is not agreement.** Silence in a retro is not consent. PO facilitates to surface disagreement, not to declare unanimity.

**What this means in practice:**
- Sprint loading uses velocity history, not hope
- Epic estimation uses prior estimation accuracy, not confidence
- Rollback decisions use health check data, not feel
- Model fallback decisions use token usage + cost data, not speculation
- Retro action items use metrics, not anecdotes

If the framework cannot produce the data needed for a decision, that is itself a finding — create a Task or TechMain epic to add the measurement.

---

## 30. Definition of Done

> **Single canonical checklist. Every epic category refers here. "Done" is not negotiable.**

### 30.1 Principle

An epic is Done when a reasonable outsider could look at the artifact and agree it is shippable, reviewed, tested, and documented. "Done" does not mean "code written." It means the work is safe to release and the next person can understand it without asking the author.

### 30.2 Universal Definition of Done

Every epic — Task, Story, Prod Issue, TechMain, Blocker, Feature child — must satisfy ALL applicable items before moving to `finished/`:

```
☐ 1.  Code complete and follows .sdd/coding-standards.md
☐ 2.  All unit tests written, passing locally and in CI
☐ 3.  All integration tests passing in CI (where applicable)
☐ 4.  Test coverage meets the quality gate threshold (PLAT-009)
☐ 5.  SonarQube scan passes — zero new bugs, vulnerabilities, or critical smells
☐ 6.  PR raised with: epic ref, AC links, spec changelog updated
☐ 7.  PR reviewed and approved by the designated reviewer (Lead Dev for most)
☐ 8.  PR merged to main (squash-merge per coding standards)
☐ 9.  Auto-deploy to dev environment succeeded (PLAT-011)
☐ 10. Deployed artifact passes post-deploy health check (PLAT-012)
☐ 11. Demo script executed; all acceptance criteria demonstrated as passing
☐ 12. Owner QA approved (Datta for scaffolding; PO for Story epics)
☐ 13. Spec moved from `in-progress/` to `finished/` in INDEX.md
☐ 14. Epic status log updated: DONE, with timestamp and accepting party
```

### 30.3 Category-Specific Additions

Some categories have additional items layered on top of the universal list.

| Category | Additional DoD items |
|---|---|
| **Task** | None beyond universal |
| **Story** | Deliverable is a document (analysis, design, recommendation), stored at agreed location, reviewed by Lead Dev for technical accuracy |
| **Prod Issue** | Deployed to PRODUCTION (not just dev); verified in prod with a reproduction test; post-mortem entry added if severity ≥ S2 |
| **TechMain** | No regression in existing tests; performance baseline unchanged or improved (whichever is targeted); CVE database rescan passes if security-related |
| **Blocker** | Resolution notice posted in `#rootine-planning`; dependent epics unblocked and resumed; any affected paused-epic registry entries removed (PLAT-001 hook) |
| **Feature (parent)** | All child epics individually Done; feature-level integration tests green; end-to-end demo covers the whole flow |

### 30.4 What "Done" Is NOT

These are common fakes. None of them count as Done.

| Fake Done | Why it fails |
|---|---|
| "Code works on my machine" | No CI proof — fails rules 2, 3, 9 |
| "PR is open, just waiting on review" | PR is not merged — fails rules 7, 8 |
| "Merged to main" | No deploy verification — fails rules 9, 10 |
| "Tests are written but skipped" | Skipped tests don't count as passing — fails rules 2, 3 |
| "I'll document it later" | Spec changelog is part of the PR — fails rule 6 |
| "QA will happen next sprint" | Acceptance is part of this epic — fails rule 12 |
| "Moved to finished/ early to free the slot" | Untruthful INDEX — fails rule 13 |

### 30.5 Enforcement

- **Automated checks** (CI + GitHub branch protection) cover rules 1–9
- **Manual checks** (Lead Dev review, Datta QA, demo script) cover rules 7, 10, 11, 12
- **PO Agent audit** covers rules 13, 14 — PO refuses to move an epic to `finished/` without a DONE entry in the status log
- A Definition-of-Done violation discovered after move = the epic is clawed back to `in-progress/` and the missing items are completed. This is NOT punitive — it is the empirical process control principle (§29.9) applied to "done."

### 30.6 Dogfooding Rule

The framework's own rules evolve. When this section (§30) is updated, every open epic must be re-checked against the new DoD before its next state transition. Retrofitting is not required for already-finished epics unless the change is a fix to a bug in the previous version.

---

## 31. Definition of Ready

> **An epic cannot enter a sprint until it is Ready. Unready work is the #1 cause of swaps, rollovers, and cancelled sprints.**

### 31.1 Principle

Ready means: a developer (human or agent) could pick this up right now and start coding without asking a single clarifying question that the team has not already answered. If they would have to ask, the epic is not Ready — PO sends it back to grooming.

### 31.2 Universal Definition of Ready

Every epic must satisfy ALL items before PO Agent accepts it into a sprint at Saturday Planning:

```
☐ 1.  Business spec exists and is approved by PO
☐ 2.  Story points estimated (1, 2, 3, or 5 — nothing else)
☐ 3.  Category label assigned (task / story / prod-issue / tech-maintenance / blocker / feature)
☐ 4.  Severity/priority assigned (P1 / P2 / P3 / P4)
☐ 5.  Acceptance criteria written in Given/When/Then form, minimum 3 ACs
☐ 6.  Technical spec exists OR tech spec grooming is scheduled for Sunday Kickoff
☐ 7.  Dependencies identified and either resolved or explicitly listed as blockers
☐ 8.  No file collision with other committed epics (PO collision guard)
☐ 9.  Owner assigned by PO (no self-assignment)
☐ 10. Sprint assignment set (PC-NN-S-NN)
☐ 11. Points ≤ 5 (otherwise PO must split before accepting)
☐ 12. Epic does NOT depend on work that is not itself Ready
```

### 31.3 Category-Specific Additions

| Category | Additional DoR items |
|---|---|
| **Task** | Tech stack for this task matches `tech-stack.yaml`; no new dependency required (if new dep needed, create a Story first) |
| **Story** | Deliverable format explicit: "recommendation doc", "design doc", "analysis" — never "we'll figure it out" |
| **Prod Issue** | Severity set by PO (not guessed); reproduction steps documented; hotfix due date computed from severity table (PLAT-008) |
| **TechMain** | CVSS score if security-related; baseline metric captured if performance-related |
| **Blocker** | Owner identified (Datta or blocking party); cascading SLA start date noted; dependent epics listed |
| **Feature (parent)** | Child epics already drafted (even if not yet Ready individually); first child is Ready |

### 31.4 The Ready Gate at Saturday Planning

PO Agent runs this gate automatically:

```
For each proposed epic:
  if ALL DoR items satisfied:
    → accept into sprint
  elif tech spec scheduled for Sunday Kickoff:
    → accept with status "ready-after-kickoff"
    → PO Agent reschedules the DoR check for Sunday 11:00
    → if still not Ready by Sunday 11:00 → returned to backlog
  else:
    → rejected with reason list
    → returned to backlog
    → PO adds a grooming task for next sprint
```

### 31.5 What "Ready" Is NOT

| Fake Ready | Why it fails |
|---|---|
| "We'll figure out the ACs during coding" | No AC = no DoD match later — fails rule 5 |
| "Points are between 3 and 8, we'll see" | Points must be locked — fails rules 2, 11 |
| "Dependencies will probably be fine" | Unacknowledged deps are the #1 sprint risk — fails rule 7 |
| "Associate wants to pick this up" | Self-assignment is forbidden — fails rule 9 |
| "It's only 6 points, close enough" | Max 5 is absolute — fails rule 11 |
| "This depends on ROOT-NNN which is in grooming" | Transitively unready — fails rule 12 |

### 31.6 Ready ≠ Clear Path to Done

Ready means "we know what to build." Done means "we built it correctly." An epic can be fully Ready and still fail in execution (estimation miss, unforeseen tech problem, external vendor). That is retro material — not a DoR failure. DoR only checks what could be known at planning time.

### 31.7 Dogfooding Rule

This section (§31) is load-bearing for Saturday Planning. When updated, the PO Agent's `ready_gate` routine must be updated within the same sprint. The change is a process change and follows Bible §29.5 (rules for disagreement) and §29.9 (empirical — cite which prior sprint's data motivated the change).

---

> This document is the living reference for the SDD platform scaffolding. As the system evolves, update this document at each PC close. The PO agent should be instructed to flag any discrepancy between this document and actual system behaviour in the `context-summary.md`.

---

*Version 1.8 | April 2026 | Confidential — Datta Advisor Copy*
*v1.1: Added Sections 18–19 (Infrastructure specs, platform specs, project file structure, budget estimates)*
*v1.2: Added Sections 20–21 (Sprint ceremonies, story points, work schedules, Definition of Ready/Done, epic lifecycle)*
*v1.3: Added Sections 22–24 (Onboarding, epic categorization, testing standards, SonarQube quality gate)*
*v1.4: Added Sections 25–27 (Continuous improvement & retro, environment strategy, rollback mechanism)*
*v1.5: Sprint schedule changed to Saturday–Friday (ceremonies on weekends for Datta). Added Blocker epic category. Removed pre-built year structure — PCs/epics/timeline set from Datta's project documentation.*
*v1.6: Added Sections 28–29 (Sprint cancellation protocol, mid-sprint scope swap rules, conflict resolution & escalation matrix). New spec PLAT-013 created for sprint cancellation.*
*v1.7: Replaced flat 3-day Blocker SLA with cascading 1/3/7 day policy (Section 29.8). T+1 nudge, T+3 priority bump + downstream impact report, T+7 hard pause with zero LLM spend on dependent epics. Token tracker (PLAT-001) enforces the pause.*
*v1.8: Agile golden-rules audit pass (G-01..G-15). Added §1.1 Working Software Is the Point and §1.2 Customer placeholder. Added §21.5 Sustainable Pace ceiling + 6 anti-crunch rules. Added §29.9 Empirical Process Control. Added canonical §30 Definition of Done and §31 Definition of Ready. Bible Section 17 Quick Reference expanded with 15 new entries. Forecast vs commitment language sweep. PLAT-006 §3.6.5 added async backlog refinement. PLAT-010 expanded with §5 Blameless + Vegas, §6 velocity tracking JSON, §7 PC-level burndown, §8 estimation calibration log. New templates: `year-{year}/.sdd/templates/demo-script.md` and `year-{year}/tech-debt.md`.*
