# PLAT-002: Tiered Model Fallback System

## [SUMMARY]
- App: SpecAg
- Epic owner: Lead Dev Agent (implementation), {{ADVISOR}} (tier selection approval)
- Status: BACKLOG
- Sprint: PC-01 Sprint 1
- Related specs: PLAT-001, PLAT-003
- Priority: S2 — required before agents start coding

## [STORY]
As the system, when a primary AI provider's token cap is reached or the API is down,
I need to automatically or manually (via {{ADVISOR}}'s Slack command) fall back to cheaper
alternative models so that development work is not completely halted.

## [TECH SPEC]

### Tiered Model Architecture
```
TIER 1: Primary (default)
  Best quality. Used for 80-90% of all work.
  Budget: ~$200-350/year

TIER 2: Cheap Cloud Fallback
  80-85% quality of primary. 10-15x cheaper.
  Activated by: {{ADVISOR}} Slack command OR auto on 100% cap hit
  Budget: ~$10-50/year additional

TIER 3: Local Emergency (Ollama)
  60-70% quality. $0 cost. Competes for VPS RAM.
  Activated by: ALL cloud APIs down/exhausted simultaneously
  Use for: PO tasks only — NOT complex code generation
```

### Model Assignment Per Tier

| Agent | Tier 1 (Primary) | Tier 2 (Fallback) | Tier 3 (Emergency) |
|---|---|---|---|
| Lead Dev | Claude Sonnet 4.6 (Anthropic) | DeepSeek-V3 API | Qwen2.5-Coder-7B (Ollama) |
| Associate | GPT-4.1 (OpenAI) | DeepSeek-Coder-V2 API | Qwen2.5-Coder-7B (Ollama) |
| PO Agent | GPT-4o mini (OpenAI) | Gemini 2.0 Flash (FREE) | Qwen2.5-Coder-7B (Ollama) |

### Cost Comparison Per Million Tokens

| Provider | Model | Input | Output | Relative to Primary |
|---|---|---|---|---|
| Anthropic | Claude Sonnet 4.6 | $3.00 | $15.00 | 1x (baseline) |
| OpenAI | GPT-4.1 | $2.00 | $8.00 | ~0.6x |
| OpenAI | GPT-4o mini | $0.15 | $0.60 | ~0.05x |
| DeepSeek | DeepSeek-V3 | $0.27 | $1.10 | ~0.08x |
| DeepSeek | DeepSeek-Coder-V2 | $0.14 | $0.28 | ~0.03x |
| Google | Gemini 2.0 Flash | FREE | FREE | $0 |
| Groq | Llama-3.1-70B | FREE | FREE | $0 |
| Local | Qwen2.5-Coder-7B | $0 | $0 | $0 (but uses VPS RAM) |

### Fallback Trigger Rules

| Trigger | Action | Who decides |
|---|---|---|
| {{ADVISOR}} types `fallback lead` | Lead Dev switches to DeepSeek-V3 | {{ADVISOR}} (manual) |
| {{ADVISOR}} types `fallback all` | All agents switch to Tier 2 | {{ADVISOR}} (manual) |
| 100% daily cap hit | Alert sent + agent paused. {{ADVISOR}} decides fallback or pause | {{ADVISOR}} (prompted) |
| 100% weekly cap hit | Full halt until Monday. No auto-fallback | System (automatic halt) |
| API returns 429 (rate limit) | Exponential backoff: 5s, 15s, 45s. If >3 min, checkpoint + pause | System (automatic) |
| API returns 5xx (outage) | 3 retries with backoff. Then switch to Tier 2 automatically | System (automatic) |
| ALL cloud APIs unreachable | Switch to Tier 3 (Ollama). PO tasks only. Pause code gen | System (automatic) |

### LiteLLM Integration (Universal API Wrapper)
The system uses LiteLLM as a unified interface to call any provider with the same API.
This avoids maintaining separate client code per provider.

```python
# All providers called through one interface:
from litellm import completion

# Tier 1
completion(model="anthropic/claude-sonnet-4-6", messages=[...])

# Tier 2 — same interface, different model string
completion(model="deepseek/deepseek-chat", messages=[...])

# Tier 3 — same interface, local model
completion(model="ollama/qwen2.5-coder:7b", messages=[...])
```

### Tier 3 Constraints (Local Model)
- Qwen2.5-Coder-7B (Q4 quantized) requires ~5 GB RAM
- MUST pause all builds/tests while Tier 3 is active (RAM conflict)
- ONLY suitable for PO-level tasks: triage, assignment, Slack reports
- NOT suitable for: code generation, PR review, architecture decisions
- Auto-revert to Tier 1/2 as soon as cloud APIs recover

### Provider Registration Required
| Provider | Signup URL | Free Tier? | API Key Env Var |
|---|---|---|---|
| Anthropic | console.anthropic.com | No | `ANTHROPIC_API_KEY` |
| OpenAI | platform.openai.com | No | `OPENAI_API_KEY` |
| DeepSeek | platform.deepseek.com | $5 free credit | `DEEPSEEK_API_KEY` |
| Google AI Studio | aistudio.google.com | Yes (generous) | `GOOGLE_API_KEY` |
| Groq | console.groq.com | Yes (free tier) | `GROQ_API_KEY` |

### Files Touched
- `/app/agents/model_router.py` — tier selection, fallback logic, LiteLLM calls
- `/app/config/agent_limits.yaml` — model names, caps, costs per tier
- `/app/.env` — all API keys (never committed)
- `/app/agents/token_tracker.py` — logs which tier was used per call

## [STANDARDS]
- Tier switch MUST be logged to status.log with reason and timestamp
- Tier 2 fallback MUST auto-revert to Tier 1 at midnight reset
- Tier 3 MUST NOT be used for code generation — PO tasks only
- All provider API keys stored in `.env`, never in code or config files
- LiteLLM is the only library that makes API calls — no direct provider SDKs

## [ACCEPTANCE CRITERIA]
```
AC-001: Given {{ADVISOR}} types "fallback lead" in Slack, when the command is processed,
        then Lead Dev's next API call uses DeepSeek-V3 instead of Sonnet 4.6.

AC-002: Given all agents are on Tier 2 fallback, when midnight reset runs,
        then all agents revert to Tier 1 primary models.

AC-003: Given Anthropic API returns 429, when 3 retries with backoff fail,
        then the system auto-switches Lead Dev to Tier 2 and notifies Slack.

AC-004: Given ALL cloud APIs are unreachable, when an agent needs to make a call,
        then system switches to Tier 3 (Ollama) for PO tasks only and pauses code gen.

AC-005: Given a Tier 2 call is made, when usage is logged, then the tier field
        reads "fallback" and the correct cheaper cost is recorded.

AC-006: Given Tier 3 is active, when a cloud API recovers, then system
        auto-reverts to the recovered provider within 5 minutes.
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created
