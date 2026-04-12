# Roadmap

## What's Built (v0.1.0)

| Component | Status | Notes |
|---|---|---|
| Project Bible (complete methodology) | Done | ~2000 lines, 31 sections |
| 13 PLAT specs (PLAT-001 through PLAT-013) | Done | Token monitoring, fallback, Slack, ceremonies, traceability, etc. |
| 1 INFRA spec (INFRA-001 VPS setup) | Done | |
| Tier definitions (T1/T2/T3) | Done | Stakes-based, not user-count |
| Tier strictness matrix | Done | 40+ dimensions × 3 tiers |
| Pre-call hook chain design (6 hooks) | Done | Interface + default implementations spec'd |
| Cascading Blocker SLA (1/3/7) | Done | With hard-pause at T+7 |
| Definition of Done (14-item checklist) | Done | Universal + category-specific |
| Definition of Ready (12-item checklist) | Done | With DoR gate pseudocode |
| Sustainable pace ceiling | Done | AI 35h/wk, Human 10h/wk, 6 anti-crunch rules |
| Empirical process control rules | Done | Bible §29.9 |
| Blameless retro + Vegas rule | Done | PLAT-010 §5 |
| Velocity tracking design | Done | `sprints/velocity.json` spec'd |
| PC-level burndown design | Done | `year-{year}/PC-{pc}/burndown.md` spec'd |
| Estimation calibration log | Done | `sprints/estimation-log.md` spec'd |
| Sprint cancellation protocol | Done | PLAT-013, Datta-only authority |
| Demo script template | Done | 5-min structured demo |
| Tech debt register template | Done | Append-only, PO weekly scan |
| `specag.config.example.yaml` | Done | Unified config |
| CLI skeleton (`specag init`) | Done | Basic scaffolding |

## What's Next (v0.2.0 — target: after first real project)

| Component | Priority | Notes |
|---|---|---|
| `specag init` — full interactive setup | High | Tier picker, provider config, Slack setup |
| `specag sprint prepare` — DoR validation | High | Validates specs against Definition of Ready |
| `specag sprint kickoff` — state transition | High | draft → planned → active |
| `specag stats` — cost summary CLI | High | Per-provider, per-agent, per-epic cost breakdown |
| `specag tier set` — tier migration | High | Upgrade/downgrade with diff |
| Token tracker implementation | High | SQLite, hook chain, real enforcement |
| Slack bot implementation | Medium | Ceremony posts, alerts, commands |
| Cron job setup automation | Medium | Auto-install ceremony crons |
| `specag sprint descope` — structured descope | Medium | Reason, classification, cost impact |
| Backlog folder structure | Low | `active/paused/blocked/deprioritized/` |
| Spec quality linter | Low | Auto-score against DoR checklist |
| Example project (todo-app) | High | Real project built with SpecAg, full audit trail |

## What's Deferred (no timeline)

| Component | Reason |
|---|---|
| T4 Enterprise tier (RBAC, SSO, compliance hooks, audit export) | No enterprise customer yet. Build when asked + paid. |
| Web dashboard | CLI + Slack is enough. Dashboard is Cloud-only (Path B). |
| Jira / Linear / GitHub integrations | Hook system supports this architecturally. Build when asked. |
| Plugin system formalization | Hooks ARE the plugin system. Don't over-abstract. |
| Multi-tenant / multi-user | Solo-founder tool. Premature. |

## Release Strategy

| Version | What ships | When |
|---|---|---|
| **v0.1.0** | Framework docs + specs + templates + CLI skeleton | Now |
| **v0.2.0** | Working CLI (`init`, `sprint`, `stats`, `tier`) + token tracker | After PC-02 (first real project) |
| **v0.3.0** | Slack bot + ceremony automation + example project | 1-2 months after v0.2.0 |
| **v1.0.0** | Battle-tested on 2+ real projects, all T1/T2/T3 features stable | 3-6 months |

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md). The highest-impact contributions right now:

1. **Try it** — use SpecAg on a project and report what broke
2. **Write an example project** — build something real with SpecAg, submit it to `examples/`
3. **Add a hook** — implement a custom PreCallHook for a use case we haven't thought of
4. **Improve docs** — fix unclear sections, add diagrams, translate
