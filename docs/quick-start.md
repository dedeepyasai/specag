# Quick Start — Zero to First Spec in 10 Minutes

## Prerequisites

- Python 3.10+
- A GitHub repo for your project
- A Slack workspace with 2 channels (`#dev`, `#planning`)
- At least one LLM API key (Anthropic, OpenAI, DeepSeek, or Google)

## Step 1: Install SpecAg (1 minute)

```bash
pip install specag
```

Or with pipx (recommended for CLI tools):

```bash
pipx install specag
```

## Step 2: Initialize Your Project (2 minutes)

```bash
cd your-project
specag init
```

The interactive setup asks:

```
Project name: my-saas-app
Your name: Datta
Timezone [America/Chicago]:
Tier (starter/personal/medium) [personal]: personal
Primary LLM provider for Lead Dev (anthropic/openai/deepseek) [anthropic]:
```

This creates:

```
your-project/
├── specag.config.yaml      ← your project config
├── specs/
│   └── platform/            ← PLAT-001 through PLAT-013 (framework specs)
├── agents/
│   ├── hooks/               ← pre-call hook chain
│   └── state/               ← paused epic registry
├── sprints/
│   ├── velocity.json        ← velocity tracking (empty)
│   └── estimation-log.md    ← estimation calibration (empty)
├── docs/
│   └── bible.md             ← your project's copy of the SpecAg Bible
└── .sdd/
    ├── coding-standards.md
    ├── templates/
    │   └── demo-script.md
    └── onboarding/
```

## Step 3: Write Your First Spec (5 minutes)

Create `specs/ROOT-001-user-login.spec.md`:

```markdown
# ROOT-001: User Login

## [SUMMARY]
- App: my-saas-app
- Epic owner: Lead Dev
- Status: READY
- Priority: S1

## [STORY]
As a user, I can log in with email and password so I can access my account.

## [TECH SPEC]
- POST /api/auth/login — accepts email + password, returns JWT
- POST /api/auth/logout — invalidates token
- Password hashed with bcrypt, min 8 chars
- JWT expires in 24 hours
- Rate limit: 5 attempts per minute per IP

### Files Touched
- src/api/auth.py
- src/models/user.py
- tests/test_auth.py

## [ACCEPTANCE CRITERIA]
AC-001: Given valid credentials, when POST /api/auth/login, then 200 + JWT returned.
AC-002: Given invalid password, when POST /api/auth/login, then 401 returned.
AC-003: Given 6 rapid attempts, when POST /api/auth/login, then 429 returned.

## [CHANGE LOG]
- 2026-04-12: Initial spec created
```

## Step 4: Prepare Your First Sprint (2 minutes)

```bash
specag sprint prepare
```

This validates your specs against the Definition of Ready:

```
Checking ROOT-001-user-login.spec.md...
  ✓ Business spec present
  ✓ Tech spec present
  ✓ Acceptance criteria defined (3 ACs)
  ✓ Files touched listed
  ✓ Owner assigned (Lead Dev)
  ✗ Story points not assigned — add to [SUMMARY]

1 issue found. Fix and re-run.
```

Add `- Story points: 3` to the SUMMARY section, then re-run.

## Step 5: Check Your Budget (30 seconds)

```bash
specag stats
```

```
SpecAg Cost Summary — my-saas-app (T2 Personal)

  Today:    $0.00 / $0.18 daily cap (0%)
  This week: $0.00 / $0.90 weekly cap (0%)

  Provider     Agent      Model              Tokens    Cost
  ─────────────────────────────────────────────────────────
  (no usage yet)

  Hooks active: daily_cap, weekly_cap, work_window, paused_registry, budget_guard
  Next alert at: 50% daily cap ($0.09)
```

## What's Next?

1. **Read the [Study Guide](study-guide.md)** to understand the full framework
2. **Read the [Tier Matrix](tier-matrix.md)** to see what's enforced at your tier
3. **Set up Slack** — configure your bot token in `.env`
4. **Write more specs** — one per feature, max 5 story points each
5. **Run your first sprint** — `specag sprint kickoff` on Sunday

## Frequently Asked Questions

**Do I need all 3 AI agents?**
No. Start with just Lead Dev if you want. PO Agent and Associate are optional at T1/T2.

**Can I use Cursor / Claude Code / Copilot for the actual coding?**
Yes. SpecAg doesn't generate code — it provides the process, specs, and cost guardrails. Use whatever AI coding tool you prefer.

**What if I don't use Slack?**
Slack is recommended but not required. At T1/T2, you can run ceremonies manually and check costs via `specag stats`.

**Is this just for Python projects?**
No. SpecAg is language- and stack-agnostic. The CLI and hooks are Python, but your project can be any language.
