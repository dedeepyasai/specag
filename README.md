# SpecAg

**Run an AI-powered engineering team with full cost control and traceability.**

SpecAg is an open-source, opinionated framework for running real software projects with AI agents doing the development work — using proper Agile ceremonies, spec-driven development, and hard budget guardrails. Built for solo founders and small teams who want AI leverage without AI chaos.

```bash
pip install specag
specag init
```

---

## What SpecAg Does

Most AI coding tools solve the **typing** problem. SpecAg solves the **engineering process** problem.

| Without SpecAg | With SpecAg |
|---|---|
| AI burns $200 overnight on a feature you didn't ask for | Hard daily/weekly token caps with automatic pause |
| No spec, no tests, no review | Every line of code traces back to an approved spec |
| "What did the AI do while I was at work?" | Full audit trail: spec + prompt + output + cost |
| Blocked on a human decision? AI keeps burning tokens. | Cascading 1/3/7 day SLA — T+7 = hard pause, zero spend |
| One-size-fits-all process | Stakes-based tiers: Starter → Personal → Medium → Enterprise |

## The Team

SpecAg gives you a 4-role team. 1 human, 3 AI agents.

| Role | Who | What they do |
|---|---|---|
| **Advisor** | You (human) | Vision, architecture, QA, final say. ~10 hrs/week. |
| **Lead Dev** | AI agent | Architecture, complex features, PR reviews |
| **Associate** | AI agent | Smaller features, tests, infra scripts |
| **PO Agent** | AI agent | Backlog, ceremonies, daily reports, process glue |

All coordination happens over Slack. No meetings. No Jira.

## Quick Start

```bash
# Install
pip install specag

# Initialize a new project (interactive tier picker)
specag init

# Prepare next sprint (Saturday)
specag sprint prepare

# Kick off sprint (Sunday)
specag sprint kickoff

# Check cost and token usage
specag stats
```

See [Quick Start Guide](docs/quick-start.md) for the full 10-minute walkthrough.

## Stakes-Based Tiers

SpecAg tiers projects by **stakes, not user count**. A HIPAA app with 20 users needs more rigor than a meme app with 10M users.

| Tier | When to use | Ceremonies | Spec required | Cost enforcement |
|---|---|---|---|---|
| **T1 Starter** | Learning, experiments, tutorials | Optional | Optional | Always on |
| **T2 Personal** | Real side project, solo owner | Recommended | Recommended | Always on |
| **T3 Medium** | Paying users, real revenue | Required | Required | Always on |

> **Cost enforcement is strict at every tier.** That's the point. Even a hello-world project gets token caps, because the point is to prevent runaway spend.

Set your tier in `specag.config.yaml`:

```yaml
project:
  name: "my-project"
  tier: personal    # starter | personal | medium
```

See [Tier Matrix](docs/tier-matrix.md) for the full strictness breakdown.

## Cost Enforcement (The Moat)

Every AI coding tool watches your spend. **SpecAg stops it.**

### Pre-Call Hook Chain

Before any LLM API call, a chain of hooks runs. First non-ALLOW decision wins:

| Hook | What it does |
|---|---|
| `DailyCapHook` | Reject if daily token cap reached |
| `WeeklyCapHook` | Reject if weekly cap reached |
| `WorkWindowHook` | Reject if outside work hours |
| `PausedRegistryHook` | Reject if epic is hard-paused (blocker T+7) |
| `PCModeHook` | Downgrade to cheaper model during discovery phases |
| `BudgetGuardHook` | Reject if estimated cost exceeds remaining budget |

Hooks are pluggable. Swap, add, or remove by editing `hooks.yaml` — no code changes.

### Cascading Blocker SLA

When work is blocked on a human decision:

| Day | What happens |
|---|---|
| **T+1** | PO Agent nudges in Slack |
| **T+3** | Priority bumps. Downstream impact broadcast. |
| **T+7** | **HARD PAUSE.** Token tracker rejects ALL LLM calls on blocked paths. Zero spend until human responds. |

Most tools observe. SpecAg enforces.

## Spec-Driven Development

No code without a spec. No commit without a spec reference. No PR without a spec update.

```
Spec (business + technical + acceptance criteria)
  → AI implements against the spec
  → Commit references the spec (git hook enforces)
  → PR updates the spec changelog (CI enforces)
  → Demo proves the spec works
  → Human accepts
```

AI agents have no memory between conversations. **The spec IS their memory.**

## Honest Comparison

SpecAg is inspired by and builds on ideas from [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD), [GitHub Spec Kit](https://github.com/github/spec-kit), and [MetaGPT](https://github.com/FoundationAgents/MetaGPT). Here's what's different:

| Feature | BMAD | Spec Kit | MetaGPT | **SpecAg** |
|---|---|---|---|---|
| Agent roles (PM, Dev, etc.) | Yes | No | Yes | Yes |
| Spec-driven development | Yes | Yes | Partial | Yes |
| Token cost enforcement (hard stop) | No | No | No | **Yes** |
| Cascading blocker SLA (T+7 hard pause) | No | No | No | **Yes** |
| Stakes-based tier system | No | No | No | **Yes** |
| Sustainable pace ceiling | No | No | No | **Yes** |
| Pluggable hook architecture | No | Partial | No | **Yes** |
| Solo-founder-with-day-job persona | No | No | No | **Yes** |

We don't pretend to be unique in every dimension. We're unique where it matters: **cost control + human-compatible pacing.**

## Documentation

| Doc | What it covers |
|---|---|
| [Quick Start](docs/quick-start.md) | Zero to first spec in 10 minutes |
| [Study Guide](docs/study-guide.md) | Learning path for understanding the full framework |
| [Project Bible](docs/bible.md) | The complete methodology reference (~2000 lines) |
| [Tier Matrix](docs/tier-matrix.md) | What's strict/lenient at each tier |
| [Architecture](docs/architecture.md) | How the pieces fit together |
| [Roadmap](docs/roadmap.md) | What's built, what's next |

## Who This Is For

- **Solo founders with a day job** who want AI leverage without full-time babysitting
- **Small teams (2-5)** adopting AI agents for real production work
- **Anyone burned by "vibe coding"** who wants the discipline layer back

## Who This Is NOT For

- Teams that want fully autonomous AI (try [Devin](https://devin.ai))
- Teams that just need code completion (try [Cursor](https://cursor.sh) or [Copilot](https://github.com/features/copilot))
- Enterprise teams that need Jira/Linear integration today (that's on the roadmap, not shipped)

## Estimated Cost

Running a full SpecAg team (1 human + 3 AI agents) for a year:

| Item | Annual cost |
|---|---|
| VPS (4 vCPU / 16GB) | ~$144 |
| AI APIs (primary + fallback) | ~$280 |
| **Total** | **~$424/year ($35/month)** |

The framework is designed to stay under $500/year total. Cost enforcement makes this a ceiling, not a guess.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). We welcome:
- Bug reports and feature requests
- Documentation improvements
- New hook implementations
- Tier profile contributions
- Example projects

## License

MIT. Use it, fork it, sell products built with it. See [LICENSE](LICENSE).

---

*Built by [Dedeepya Sai Gondi](https://github.com/dedeepyasai) in Dallas, TX. Dogfooded on real projects.*
