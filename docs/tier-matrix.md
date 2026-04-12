# Tier Strictness Matrix

SpecAg tiers projects by **stakes, not user count**. A HIPAA app with 20 users needs enterprise rigor. A meme generator with 10M users might not.

## Tier Definitions

| Tier | Code | When to use | Example |
|---|---|---|---|
| **Starter** | `T1` | Learning, experiments, tutorials, throwaway hacks | "I'm trying SpecAg for the first time" |
| **Personal** | `T2` | Real side project, solo owner, intended to ship | "My personal app — I want to use it daily" |
| **Medium** | `T3` | Real users, revenue possible, reputation on the line | "Early-stage SaaS with 50 paying customers" |

> **Enterprise (T4)** is on the roadmap but not shipped. If you need RBAC, compliance hooks, SSO, or audit export, [open an issue](https://github.com/dedeepyasai/specag/issues).

## How to Set Your Tier

```yaml
# specag.config.yaml
project:
  tier: personal    # starter | personal | medium
```

Or via CLI:

```bash
specag tier set medium
```

## Strictness Levels

- **OFF** — not loaded, not available
- **OPT** — available but not enforced; no warning if skipped
- **REC** — recommended; warning if skipped, but won't block
- **REQ** — required; hard-blocked if missing

## The Matrix

### Spec & Traceability

| Dimension | T1 Starter | T2 Personal | T3 Medium |
|---|---|---|---|
| Business spec before code | OPT | REC | REQ |
| Tech spec before code | OPT | REC | REQ |
| Commit epic-ref hook | OFF | OPT | REQ |
| PR updates spec changelog | OFF | OPT | REQ |
| Daily PO spec-code sync audit | OFF | OFF | REC |

### Ceremonies

| Dimension | T1 Starter | T2 Personal | T3 Medium |
|---|---|---|---|
| Saturday Sprint Planning | OPT | REC | REQ |
| Sunday Kickoff / grooming | OPT | REC | REQ |
| Daily standup | OFF | OPT | REQ |
| Daily report (PO) | OFF | OPT | REQ |
| Saturday Sprint Review | OPT | REC | REQ |
| Saturday Retro | OPT | REC | REQ |
| Wednesday async backlog refinement | OFF | OPT | REQ |

### Quality & Acceptance

| Dimension | T1 Starter | T2 Personal | T3 Medium |
|---|---|---|---|
| Definition of Ready | OPT | REC | REQ |
| Definition of Done | OPT | REC | REQ |
| Test coverage requirement | OPT | REC | REQ |
| SonarQube / quality gate | OFF | OFF | REC |
| PR review required | OPT | REC | REQ |
| 5-min demo per epic | OPT | REC | REQ |

### Budget & Safety (strict at every tier)

| Dimension | T1 Starter | T2 Personal | T3 Medium |
|---|---|---|---|
| Token daily/weekly caps | **REQ** | **REQ** | **REQ** |
| Pre-call hook chain | **REQ** | **REQ** | **REQ** |
| PausedRegistryHook (T+7 hard pause) | REC | REQ | REQ |
| Fallback model chain | REQ | REQ | REQ |
| Weekly cost report | OPT | REC | REQ |

### Process & Governance

| Dimension | T1 Starter | T2 Personal | T3 Medium |
|---|---|---|---|
| Cascading Blocker SLA (1/3/7) | OFF | REC | REQ |
| Sprint cancellation protocol | OFF | OPT | REQ |
| Mid-sprint 1-in-1-out swap rule | OFF | OPT | REQ |
| Single backlog rule | OPT | REC | REQ |
| Sustainable pace ceiling | OPT | REC | REQ |
| Blameless retro + Vegas rule | OPT | REC | REQ |
| Velocity tracking | OFF | OPT | REQ |
| PC-level burndown | OFF | OPT | REQ |
| Estimation calibration log | OFF | OFF | REC |
| Tech debt register | OFF | OPT | REQ |

### Environments & Ops

| Dimension | T1 Starter | T2 Personal | T3 Medium |
|---|---|---|---|
| Dev / Prod environment separation | OPT | REC | REQ |
| Rollback mechanism | OPT | REC | REQ |
| 1-sprint staging QA delay | OFF | OPT | REQ |
| Secrets in .env (never committed) | REC | REQ | REQ |
| Backup cadence | OFF | REC | REQ |

## Reading the Matrix

- **Budget & Safety is REQ at every tier.** This is SpecAg's core value. Even a tutorial project gets token caps. Without this, SpecAg is just another Agile template.
- **Ceremonies scale with stakes.** T1 has almost no ceremonies. T3 has all of them. The framework is the same; the volume knob is different.
- **Upgrading is safe.** Moving T1 → T2 → T3 only adds requirements — it never removes files or breaks existing work. The CLI warns you about new requirements when you upgrade.
- **Downgrading warns.** Moving T3 → T2 loosens enforcement. The CLI lists what will no longer be enforced so you can make an informed decision.

## Tier Upgrade Path

```bash
# See what changes when upgrading
specag tier diff medium

# Upgrade
specag tier set medium

# Downgrade (with warning)
specag tier set starter
# WARNING: The following will no longer be enforced:
#   - Commit epic-ref hook
#   - PR spec changelog update
#   - Daily standup
#   - ...
# Proceed? [y/N]
```
