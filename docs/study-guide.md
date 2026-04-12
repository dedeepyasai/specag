# Study Guide — Learning SpecAg from Zero

This is a structured learning path. Follow it in order. Each section builds on the previous one and tells you exactly what to read, what to understand, and what to try.

**Estimated total study time: 3-4 hours** (spread across 2-3 sessions).

---

## Level 1: The Why (30 minutes)

### Read

1. **[README.md](../README.md)** — the pitch, the team structure, the honest comparison table
2. **[Roadmap](roadmap.md)** — what exists today vs. what's planned

### Understand

- Why "spec-driven" matters for AI agents (they have no memory between sessions)
- Why cost enforcement is the moat (every other tool observes; SpecAg stops)
- Why tiers exist (stakes-based, not user-count-based)
- The 4 roles: Advisor (human), Lead Dev (AI), Associate (AI), PO Agent (AI)

### Try

```bash
pip install specag
specag --help
```

Read the help output. Don't run anything yet — just see what commands exist.

---

## Level 2: The Process (45 minutes)

### Read

1. **[Bible](bible.md) Sections 1-7** — philosophy, team structure, coding standards
2. **[Bible](bible.md) Section 17** — Quick Reference (the cheat sheet — skim this first, then read the sections it references)
3. **[Bible](bible.md) Sections 20-21** — Sprint ceremonies, story points, sustainable pace

### Understand

- The sprint cycle: Saturday Planning → Sunday Kickoff → Daily Standups → Saturday Review → Retro
- Saturday-to-Friday sprints (weekends for ceremonies so the human can attend)
- 5 story-point maximum per epic — why this matters
- Sustainable pace: AI 35 hrs/week, Human 10 hrs/week — overtime is never a solution
- The spec lifecycle: business spec → tech spec → code → tests → PR → demo → acceptance

### Try

```bash
mkdir study-project && cd study-project
specag init
# Choose "starter" tier
# Explore the generated files
```

Look at every file `specag init` created. Read the comments in `specag.config.yaml`.

---

## Level 3: The Specs (45 minutes)

### Read

1. **[Bible](bible.md) Section 30** — Definition of Done (the 14-item checklist)
2. **[Bible](bible.md) Section 31** — Definition of Ready (the 12-item checklist)
3. **One full PLAT spec** — start with `templates/shared/specs/platform/PLAT-001-token-monitoring.spec.md`

### Understand

- The spec structure: SUMMARY → STORY → TECH SPEC → STANDARDS → ACCEPTANCE CRITERIA → CHANGE LOG
- How acceptance criteria are written (Given/When/Then)
- The difference between "Ready" (can enter a sprint) and "Done" (can be accepted)
- Why the change log in each spec matters (traceability)

### Try

Write a practice spec for a simple feature (e.g., "user can reset their password"). Follow the template:

```markdown
# ROOT-002: Password Reset

## [SUMMARY]
- App: study-project
- Epic owner: Lead Dev
- Status: DRAFT
- Story points: 2

## [STORY]
As a user who forgot their password...

## [TECH SPEC]
...

## [ACCEPTANCE CRITERIA]
AC-001: Given...
```

Run `specag sprint prepare` — does your spec pass the DoR check?

---

## Level 4: Cost Enforcement (45 minutes)

### Read

1. **`templates/shared/specs/platform/PLAT-001-token-monitoring.spec.md`** — the full token monitoring spec
2. **`templates/shared/specs/platform/PLAT-002-model-fallback.spec.md`** — the fallback chain
3. **`specag.config.example.yaml`** — the hooks section

### Understand

- The pre-call hook chain: what hooks exist, what order they run, what ALLOW/REJECT/DOWNGRADE means
- Daily and weekly token caps — how they're calculated, what happens at 50%/80%/100%
- The PausedRegistryHook — how blocker hard-pause at T+7 zeroes LLM spend
- The fallback chain: primary model → cheap cloud → local emergency
- Why hooks are pluggable (so you can add your own without touching core code)

### Try

```bash
specag stats
# Even with no usage, this shows your configured caps and active hooks
```

Edit `specag.config.yaml` — change the daily_token_cap to something tiny (like 100), then imagine what would happen if an agent hit that cap mid-task.

---

## Level 5: The Tier System (30 minutes)

### Read

1. **[Tier Matrix](tier-matrix.md)** — the full strictness breakdown
2. **[Bible](bible.md) Section 29** — Conflict resolution and escalation

### Understand

- T1 (Starter): almost everything optional, only cost enforcement is strict
- T2 (Personal): ceremonies recommended, specs recommended, cost strict
- T3 (Medium): everything required — this is "production mode"
- Why cost enforcement is REQ at every tier (it's the moat)
- How to upgrade T1 → T2 → T3 as your project grows

### Try

```bash
specag tier show
# Shows current tier + what's enforced

specag tier set medium
# Upgrades to T3 — see what new requirements activate
```

---

## Level 6: Advanced (30 minutes)

### Read

1. **[Bible](bible.md) Section 28** — Mid-sprint swap rules, sprint cancellation
2. **[Bible](bible.md) Section 29.8** — Cascading Blocker SLA (1/3/7 days)
3. **[Bible](bible.md) Section 29.9** — Empirical process control
4. **[Architecture](architecture.md)** — how the pieces fit together technically

### Understand

- The 1-in-1-out swap rule (no free additions mid-sprint)
- Blocker SLA cascade: T+1 nudge → T+3 escalation → T+7 hard pause
- "Decisions from data, not gut. Gut calls are labelled and revisited."
- How SpecAg's architecture separates framework (templates) from project (your code)

### Try

Create a fake blocker spec:

```markdown
# BLOCK-001: Waiting on API key from vendor

## [SUMMARY]
- Blocking: ROOT-003
- Owner: Advisor (human)
- Created: 2026-04-12
- SLA clock starts: 2026-04-12
```

Think through: what happens at T+1? T+3? T+7? What would the PO Agent post in Slack? What would the token tracker do?

---

## Level 7: Contributing (15 minutes)

### Read

1. **[CONTRIBUTING.md](../CONTRIBUTING.md)**
2. **[Roadmap](roadmap.md)** — "What's Next" section

### Understand

- How to add a new hook (implement the PreCallHook interface)
- How to add a new tier profile
- How to contribute an example project

### Try

Pick one small thing from the roadmap that interests you. Fork the repo, make the change, open a PR.

---

## After the Study Guide

You now understand SpecAg well enough to:

1. **Use it** — initialize a real project, write specs, run sprints
2. **Customize it** — adjust your tier, add hooks, change ceremony schedules
3. **Contribute** — fix bugs, add features, improve docs
4. **Teach it** — explain to someone else why spec-driven + cost enforcement matters

The best next step is to **use it on a real project**. Even a small one. The framework only makes sense when it's running — reading about Agile is not the same as doing Agile.

```bash
specag init
# Pick your project. Write your first spec. Ship your first sprint.
```
