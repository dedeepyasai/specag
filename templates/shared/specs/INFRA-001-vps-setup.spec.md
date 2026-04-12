# INFRA-001: VPS Infrastructure Setup

## [SUMMARY]
- App: Rootine
- Epic owner: Datta
- Status: BACKLOG
- Sprint: PC-01 Sprint 1 (pre-requisite — must be complete before agents go live)
- Related specs: INFRA-002, PLAT-001, PLAT-002, PLAT-003

## [STORY]
As Datta (Advisor), I need a reliable, always-on VPS that runs the full agent ecosystem —
orchestration, builds, tests, CI/CD, Slack bot, and database — so that the 3 AI agents
can operate autonomously within a controlled budget.

## [TECH SPEC]

### Selected Plan
| Field | Value |
|---|---|
| Provider | Hostinger |
| Location | USA |
| Plan | KVM 2 |
| Cost | $12/month ($144/year) |
| CPU | 4 vCPU Core |
| RAM | 16 GB |
| Disk | 200 GB NVMe |
| Bandwidth | 16 TB |
| OS | Ubuntu 22.04 LTS |
| Backups | Weekly (included) |
| Snapshot | 1 included |

### Why this plan (not smaller)
Agents don't just make API calls — they build code, run tests, lint, and compile.
Peak memory during simultaneous builds + tests + SonarQube = ~9-10 GB.
The $6/mo (4GB) plan would OOM during concurrent builds.

### Resource Budget (Peak)
```
CrewAI agents (3):              1.5 GB
Slack bot (24/7):               0.1 GB
PostgreSQL (Docker):            0.5 GB
Next.js build (agent 1):       1.5 GB   ← simultaneous
Jest tests (agent 2):           1.0 GB   ← simultaneous
TypeScript + ESLint:            0.5 GB
Docker daemon:                  0.5 GB
OS overhead:                    0.5 GB
SonarQube (weekly scan):       +3.0 GB   ← weekly spike
─────────────────────────────────────
Normal peak:                    6.1 GB
With SonarQube:                 9.1 GB
Available headroom:             6.9 GB (normal) / 3.9 GB (scan day)
```

### Initial Setup Commands
```bash
# System
sudo apt update && sudo apt upgrade -y

# Python + CrewAI
sudo apt install -y python3.11 python3.11-venv python3-pip
python3.11 -m venv /app/venv
source /app/venv/bin/activate
pip install crewai anthropic openai litellm slack-bolt pyyaml

# Node.js 20 LTS (for web app builds + CI tooling)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Docker (for PostgreSQL + service containers)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# GitHub CLI (for PR automation)
sudo apt install -y gh
gh auth login

# Ollama (emergency local model fallback — Tier 3 only)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5-coder:7b
```

### Directory Structure on VPS
```
/app/
├── venv/                        # Python virtual environment
├── config/
│   ├── agent_limits.yaml        # Token caps, models, schedules
│   ├── project.config.yaml      # App name, team, Slack channel
│   └── pc.manifest.yaml         # Current PC config
├── agents/
│   ├── orchestrator.py          # CrewAI main entry point
│   ├── lead_dev/                # Lead Dev agent scripts
│   ├── associate/               # Associate agent scripts
│   ├── po_agent/                # PO agent scripts
│   ├── token_tracker.py         # SQLite usage tracking
│   ├── token_monitor.py         # Alert system (runs via cron)
│   ├── model_router.py          # Tiered fallback routing
│   ├── agent_state.json         # Current pause/resume/fallback state
│   ├── slack_bot.py             # Slack listener (24/7 process)
│   ├── slack_commands.py        # Datta's command handler
│   ├── midnight_reset.py        # Auto-resume at midnight
│   └── token_usage.db           # SQLite — all provider usage
├── year-2026/                   # Shared repo (all agents read/write)
│   ├── .sdd/
│   ├── PC-01/
│   └── specs/INDEX.md
├── docker-compose.yml           # PostgreSQL + any services
└── logs/
    ├── crewai.log
    ├── slack_bot.log
    └── token_alerts.log
```

### Docker Compose
```yaml
version: "3.8"
services:
  postgres:
    image: postgres:16
    restart: always
    environment:
      POSTGRES_DB: rootine
      POSTGRES_USER: rootine
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    deploy:
      resources:
        limits:
          memory: 512M

volumes:
  pgdata:
```

### Cron Jobs (crontab)
```bash
# Agent work window
0 8 * * 1-5    /app/venv/bin/python /app/agents/po_morning_triage.py
0 18 * * 1-5   /app/venv/bin/python /app/agents/po_daily_report.py
0 22 * * 1-5   /app/venv/bin/python /app/agents/work_window_close.py

# Token monitoring — every 15 minutes during work hours
*/15 8-22 * * 1-5  /app/venv/bin/python /app/agents/token_monitor.py

# Midnight reset — resume agents, switch to primary models
0 0 * * *      /app/venv/bin/python /app/agents/midnight_reset.py

# Weekly jobs
0 8 * * 1      /app/venv/bin/python /app/agents/po_severity_retriage.py
0 17 * * 5     /app/venv/bin/python /app/agents/po_tech_scan.py
0 23 * * 0     /app/venv/bin/python /app/agents/weekly_cost_report.py
```

### What CANNOT run on this VPS
| Item | Why | Alternative |
|---|---|---|
| iOS Simulator | Requires macOS + Xcode | Expo EAS Build (cloud, free 30 builds/mo) |
| Android Emulator | Needs KVM, most VPS don't support | Expo EAS Build / BrowserStack |
| Mobile E2E tests (Detox) | Needs simulator/emulator | Cloud device farms (BrowserStack, Appetize) |

### Security Hardening
- [ ] SSH key-only auth (disable password login)
- [ ] UFW firewall: allow 22 (SSH), 443 (HTTPS), deny all else
- [ ] Fail2ban installed for brute-force protection
- [ ] All API keys stored in `/app/.env` (never committed to git)
- [ ] `.env` added to `.gitignore` globally
- [ ] Automatic security updates: `sudo apt install unattended-upgrades`

## [STANDARDS]
- All secrets in `.env` file, never hardcoded
- Docker containers must have memory limits set
- Weekly VPS snapshot before any major upgrade
- Logs rotated weekly (logrotate config)

## [ACCEPTANCE CRITERIA]
```
AC-001: Given a fresh VPS, when setup script completes, then Python 3.11,
        Node.js 20, Docker, and GitHub CLI are all installed and functional.

AC-002: Given the VPS is running, when all 3 agents + Slack bot + PostgreSQL
        are active simultaneously, then RAM usage stays below 80% (12.8 GB).

AC-003: Given cron jobs are configured, when 08:00 CST arrives on a weekday,
        then PO morning triage runs automatically.

AC-004: Given a Next.js build runs concurrently with Jest tests, then neither
        process is OOM-killed and both complete successfully.

AC-005: Given SonarQube scan runs on its weekly schedule, then total RAM usage
        including scan stays below 16 GB.
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created based on infrastructure analysis
