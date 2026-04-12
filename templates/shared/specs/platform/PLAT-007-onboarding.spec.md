# PLAT-007: New Hire Onboarding System

## [SUMMARY]
- App: Rootine
- Epic owner: PO Agent (maintains), Lead Dev (tech content review)
- Status: BACKLOG
- Sprint: PC-01 Sprint 1
- Related specs: All — onboarding references the entire system
- Priority: S2 — must exist before scaling beyond founding team

## [STORY]
As a new team member (AI agent or human), when I join the Rootine project, I need a
role-specific onboarding guide that tells me exactly what to read, what tools to set up,
what I own, what I don't touch, and how to start my first epic — so I can be productive
from day one without asking questions that are already documented.

## [TECH SPEC]

### Onboarding Guide Structure

Each role gets its own onboarding file at `.sdd/onboarding/{role}.md`.
Guides are structured in 4 phases: Context → Setup → First Day → Ongoing.

### Role-Specific Guides

| Role | File | Read Scope | First Action |
|---|---|---|---|
| Advisor (Datta) | `onboarding/advisor.md` | Project Bible, MVP, budget, decision gates | Review current PC manifest, read PO daily report |
| PO Agent | `onboarding/po-agent.md` | Full system config, all specs, INDEX.md | Run severity triage, post first daily report |
| Senior Developer (Lead) | `onboarding/senior-developer.md` | Architecture, coding standards, all tech specs, retros | Review open PRs, verify INDEX.md, prepare design meeting |
| Associate Developer | `onboarding/associate-developer.md` | Assigned epic spec ONLY, INDEX.md, coding standards | Read assigned epic, write tech spec, start coding |
| Human Developer | `onboarding/human-developer.md` | Coding standards, tech stack, active PC manifest | Set up local dev env, claim first epic in planning |
| AI Agent (generic) | `onboarding/ai-agent.md` | Agent limits, work schedule, model routing, state management | Verify API key, test first API call, confirm Slack identity |

### Onboarding Phase Structure (all roles)

```
Phase 1: CONTEXT (understand the project) — ≤30 min
  Read list specific to role — never the full Project Bible

Phase 2: SETUP (tools and access) — ≤1 hour
  Tool installation, API keys, repo access, Slack channel join

Phase 3: FIRST DAY (do something real) — Day 1
  Role-specific first task that produces a visible output

Phase 4: ONGOING (reference material)
  What to check daily, weekly, and at PC boundaries
```

### What Each Role Reads During Onboarding

| Document | Advisor | PO | Senior Dev | Associate | Human Dev | AI Agent |
|---|---|---|---|---|---|---|
| Project Bible (Sections 1-2: Overview + Roles) | YES | YES | YES | Summary only | YES | Summary only |
| Current `pc.manifest.yaml` | YES | YES | YES | Sprint goal only | YES | Sprint goal only |
| `.sdd/project.config.yaml` | NO | YES | YES | NO | YES | NO |
| `.sdd/agent.limits.yaml` | Budget section | YES | Token caps | Own caps only | NO | Own caps only |
| `.sdd/coding-standards.md` | NO | NO | YES | YES | YES | YES |
| `.sdd/tech-stack.yaml` | NO | NO | YES | Relevant parts | YES | NO |
| `specs/INDEX.md` | NO | YES (owns it) | YES | YES (read only) | YES | YES (read only) |
| Current sprint retros | NO | YES | YES | NO | Last 2 only | NO |
| `context-summary.md` (prev PC) | At PC start | YES | YES | NO | YES | NO |
| Decision gate history | YES | YES | NO | NO | NO | NO |
| Active epic specs | QA-related only | All | All in-progress | Own epic ONLY | Own epic ONLY | Own epic ONLY |

### Onboarding Verification Checklist

PO runs this checklist when any new team member (AI or human) joins:

```markdown
## Onboarding Checklist — [Role] — [Name/ID]
Date: YYYY-MM-DD

### Phase 1: Context
- [ ] Read assigned onboarding guide
- [ ] Understand current PC and sprint goal
- [ ] Know who owns what (role boundaries)

### Phase 2: Setup
- [ ] Repo access (GitHub)
- [ ] Slack channels joined (#rootine-dev, #rootine-planning)
- [ ] API keys configured (AI agents)
- [ ] Local dev environment working (human devs)
- [ ] Can push to feature branch
- [ ] Commit hook working (epic ref enforced)

### Phase 3: First Day
- [ ] First visible output produced (see role guide)
- [ ] Posted first standup message
- [ ] Confirmed understanding of Definition of Ready / Definition of Done

### Phase 4: Ongoing
- [ ] Knows where to find daily standup schedule
- [ ] Knows escalation path (blocked → status.log → PO re-routes)
- [ ] Knows sprint ceremony schedule (Friday planning, Monday kickoff)
```

### Files Touched
- `.sdd/onboarding/advisor.md`
- `.sdd/onboarding/po-agent.md`
- `.sdd/onboarding/senior-developer.md`
- `.sdd/onboarding/associate-developer.md`
- `.sdd/onboarding/human-developer.md`
- `.sdd/onboarding/ai-agent.md`

## [STANDARDS]
- Onboarding guides are updated at every PC close (PO responsibility)
- Every guide must include the "current state" section pointing to live INDEX.md and pc.manifest.yaml
- No guide should exceed 200 lines — concise, actionable, not a textbook
- New role additions require a new onboarding guide before the role becomes active
- PO verifies onboarding checklist for every new team member

## [ACCEPTANCE CRITERIA]
```
AC-001: Given a new Associate Developer agent joins, when it reads
        onboarding/associate-developer.md, then it knows its epic assignment,
        coding standards, and how to raise its first PR within 1 hour.

AC-002: Given a new human developer joins, when they follow onboarding/human-developer.md,
        then they have local dev env running, repo access, and commit hook working
        within 2 hours.

AC-003: Given a new PO Agent is initialized, when it reads onboarding/po-agent.md,
        then it can run severity triage and post a daily report on its first day.

AC-004: Given Datta onboards to a new PC, when he reads onboarding/advisor.md,
        then he knows current sprint goal, pending QA items, and next decision gate
        within 30 minutes.

AC-005: Given any role's onboarding guide, then it does not exceed 200 lines and
        contains all 4 phases (Context, Setup, First Day, Ongoing).

AC-006: Given a new team member completes onboarding, then PO has a filled
        onboarding checklist saved to status.log.
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created — 6 role-specific guides defined
