# PLAT-003: Slack Command Interface & Agent Communication

## [SUMMARY]
- App: Rootine
- Epic owner: Datta (design), Lead Dev (implementation)
- Status: BACKLOG
- Sprint: PC-01 Sprint 1
- Related specs: PLAT-001, PLAT-002, PLAT-004
- Priority: S2 — Slack is Datta's only interface to the system

## [STORY]
As Datta (Advisor), I need to control my entire 3-agent dev team from a single
Slack channel using simple text commands — pause agents, switch models, check status,
approve decisions, and QA epics — without ever SSH-ing into the VPS.

## [TECH SPEC]

### Slack App Setup
| Field | Value |
|---|---|
| App name | Rootine Dev Bot |
| Workspace | Datta's Slack workspace |
| Channel | `#rootine-dev` |
| Bot token scope | `chat:write`, `channels:read`, `channels:history`, `users:read` |
| Event subscriptions | `message.channels` (listens to all messages in channel) |
| Library | `slack-bolt` (Python) |
| Process | Runs 24/7 as systemd service on VPS |

### Agent Identities in Slack
Each agent posts as a distinct identity so Datta sees a "team":

| Agent | Display Name | Icon |
|---|---|---|
| Lead Dev | Lead Dev Agent | :hammer_and_wrench: |
| Associate | Associate Dev Agent | :computer: |
| PO Agent | PO Agent | :clipboard: |
| Token Monitor | Token Monitor | :bell: |
| System | Rootine System | :gear: |

### Command Reference — Datta's Full Control Panel

#### Agent Control
| Command | Action | Response |
|---|---|---|
| `pause lead` | Pause Lead Dev until 08:00 tomorrow | "Lead Dev paused until tomorrow 08:00 CST." |
| `pause associate` | Pause Associate until 08:00 tomorrow | "Associate paused until tomorrow 08:00 CST." |
| `pause po` | Pause PO Agent until 08:00 tomorrow | "PO Agent paused until tomorrow 08:00 CST." |
| `pause all` | Pause all agents until 08:00 tomorrow | "All agents paused for today." |
| `resume lead` | Resume Lead Dev on primary model | "Lead Dev resumed on primary model." |
| `resume all` | Resume all agents on primary models | "All agents resumed." |

#### Model Switching
| Command | Action | Response |
|---|---|---|
| `fallback lead` | Switch Lead Dev to DeepSeek-V3 | "Lead Dev switched to DeepSeek-V3." |
| `fallback associate` | Switch Associate to DeepSeek-Coder | "Associate switched to DeepSeek-Coder." |
| `fallback all` | Switch all agents to Tier 2 models | "All agents switched to fallback models." |

#### Status & Reporting
| Command | Action | Response |
|---|---|---|
| `status` | Show all agents' state + today's usage | Formatted status table |
| `cost` | Show today's + week's + month's spend | Cost breakdown by provider |
| `sprint` | Show current sprint progress | Epic status summary |

#### Natural Language Shortcuts
| Phrase | Matched to |
|---|---|
| "stop all for today" / "shut down" | `pause all` |
| "how much spent" / "what's the cost" | `cost` |
| "green flag ROOT-NNN" | PO marks epic ACCEPTED |
| "approve" / "approved" | Process pending decision gate |
| "mvp: ..." | Seed new MVP statement into pc.manifest.yaml |

### Automatic Messages (agents → Slack)

#### PO Agent Posts
| When | Message |
|---|---|
| 08:05 daily | Morning triage summary — assignments for today |
| On epic assignment | "ROOT-NNN assigned to [Lead Dev/Associate]. Collision check: PASSED." |
| On PR merge | "ROOT-NNN merged. Preview: rootine-staging.app/[path]" |
| 18:00 daily | Full daily report (see Project Bible Section 13) |
| On rollover | "ROOT-NNN rolled over to next sprint. Reason: [reason]. Re-evaluated: S[N]." |

#### Lead Dev Posts
| When | Message |
|---|---|
| PR ready | "ROOT-NNN: PR ready. Branch: feat/ROOT-NNN-description. PR: [link]" |
| PR review done | "ROOT-NNN PR review: APPROVED/CHANGES REQUESTED. [details]" |
| S1 escalation | "@datta URGENT — ROOT-NNN: [description]. Production impacted." |
| Design meeting | "Design meeting recommendation ready: [link to agenda file]" |

#### Associate Posts
| When | Message |
|---|---|
| Epic started | "ROOT-NNN picked up. Starting implementation." |
| PR ready | "ROOT-NNN: PR raised. [link]" |
| Blocked | "BLOCKED on ROOT-NNN: [reason]. Waiting for [dependency]." |
| Fix pushed | "ROOT-NNN: Review feedback addressed. Updated PR pushed." |

#### Token Monitor Posts
| When | Message |
|---|---|
| Every 15 min (if threshold crossed) | Usage alert with action commands |
| Midnight | "Midnight Reset Complete. All agents resumed." |
| Sunday 11 PM | Weekly cost report |

### Decision Gate Flow (Slack-based)
```
PO or Lead Dev posts a decision gate question:
  → "@datta — Repo split recommended for notifications domain. Approve? (yes/no)"

Datta replies:
  → "approved" or "yes" or "approve"

System processes:
  → PO creates repo-split epic, assigns to Lead Dev
  → Confirms in Slack: "Repo split epic ROOT-NNN created. Assigned to Lead Dev."
```

### Files Touched
- `/app/agents/slack_bot.py` — main Slack listener (24/7 systemd service)
- `/app/agents/slack_commands.py` — command parsing and routing
- `/app/agents/slack_client.py` — helper to post as different agent identities
- `/app/.env` — `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`

### Systemd Service (keeps Slack bot alive 24/7)
```ini
# /etc/systemd/system/rootine-slack.service
[Unit]
Description=Rootine Slack Bot
After=network.target

[Service]
Type=simple
User=rootine
WorkingDirectory=/app
ExecStart=/app/venv/bin/python /app/agents/slack_bot.py
Restart=always
RestartSec=10
EnvironmentFile=/app/.env

[Install]
WantedBy=multi-user.target
```

## [STANDARDS]
- All Slack messages must be posted to `#rootine-dev` only — no DMs, no other channels
- Agent identities must be visually distinct (different display names + icons)
- Commands are case-insensitive
- Unknown commands receive: "Unknown command. Type `help` for available commands."
- Decision gate responses must be logged to `status.log` with timestamp
- Slack bot must auto-restart on crash (systemd Restart=always)

## [ACCEPTANCE CRITERIA]
```
AC-001: Given Datta types "pause all" in #rootine-dev, when the bot processes it,
        then all 3 agents are paused and confirmation is posted within 5 seconds.

AC-002: Given Datta types "status", when the bot processes it, then a formatted
        table showing all agents' state and today's token usage is posted.

AC-003: Given Lead Dev finishes a PR review, when it posts to Slack, then the
        message shows as "Lead Dev Agent" with the wrench icon.

AC-004: Given PO Agent sends the 6 PM daily report, then the report follows
        the exact format defined in Project Bible Section 13.

AC-005: Given Datta types "green flag ROOT-041", when processed, then PO marks
        the epic as ACCEPTED in status.log and moves spec to finished/.

AC-006: Given the Slack bot crashes, when systemd detects the exit, then the
        bot restarts within 10 seconds automatically.

AC-007: Given Datta types an unknown command, then the bot responds with
        "Unknown command. Type `help` for available commands."
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created
