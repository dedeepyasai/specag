# SpecAg — Coding Standards

**Applies to:** All agents (Lead Dev, Associate, human contributors)
**Enforced by:** `pr-validation.yml` GitHub Actions workflow + `commit-msg` git hook
**Version:** 1.1 | April 2026

---

## 1. Language & Framework Standards

### TypeScript (Web + Mobile)
- Strict mode enabled (`"strict": true` in tsconfig.json)
- No `any` type — use `unknown` + type guards when type is uncertain
- All function parameters and return types explicitly typed
- Prefer `interface` over `type` for object shapes
- Use `const` by default, `let` only when reassignment is necessary, never `var`

### React / Next.js (Web)
- Functional components only — no class components
- Use Next.js App Router (not Pages Router)
- Server components by default, `"use client"` only when needed
- All API routes use Zod validation on request body

### React Native (Mobile)
- Shared types with web via `packages/shared/types/`
- Use React Navigation for routing
- E2E tests with Detox for critical user flows
- No platform-specific code outside `*.ios.ts` / `*.android.ts` files

### Node.js / Express (API)
- Express 4.19+ with TypeScript
- Drizzle ORM for all database operations — no raw SQL
- All endpoints return consistent response shape:
  ```json
  { "data": {}, "error": null, "meta": {} }
  ```
- Zod validation on every endpoint input

---

## 2. Naming Conventions

| Item | Convention | Example |
|---|---|---|
| Files (components) | PascalCase | `ReminderList.tsx` |
| Files (utilities) | camelCase | `formatDate.ts` |
| Files (API routes) | kebab-case | `reminder-scheduling.ts` |
| Variables | camelCase | `reminderCount` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES` |
| Types / Interfaces | PascalCase | `ReminderPayload` |
| Database tables | snake_case | `user_reminders` |
| Database columns | snake_case | `scheduled_at` |
| CSS classes | kebab-case | `reminder-card` |
| Environment vars | UPPER_SNAKE_CASE | `DATABASE_URL` |
| Epic branches | kebab-case with prefix | `feat/ROOT-041-reminder-ui` |

---

## 3. Commit Message Format

```
type(EPIC-REF): short description (imperative mood, max 72 chars)

Optional body: explain WHY, not WHAT.
```

### Commit Types
| Type | When |
|---|---|
| `feat` | New feature or user-facing functionality |
| `fix` | Bug fix (prod bug, test failure, edge case) |
| `patch` | Security patch from Sonar/CVE finding |
| `refactor` | Code restructure with no behavior change |
| `test` | Adding or fixing tests only |
| `docs` | Documentation, spec updates |
| `chore` | Dependency updates, config changes, build tweaks |
| `rollover` | Picking up uncommitted work from previous sprint |

### Examples
```
feat(ROOT-041): add reminder scheduling endpoint with Zod validation
fix(ROOT-045): resolve iOS crash on reminder save — null pointer guard
patch(ROOT-044): upgrade lodash to 4.17.22 — CVE-2026-1234
```

---

## 4. Branch Naming

| Type | Pattern | Example |
|---|---|---|
| Feature | `feat/ROOT-NNN-short-description` | `feat/ROOT-041-reminder-ui` |
| Bug fix | `fix/ROOT-NNN-short-description` | `fix/ROOT-045-ios-crash` |
| Hotfix | `hotfix/ROOT-NNN-short-description` | `hotfix/ROOT-044-lodash-cve` |
| Rollover | `rollover/ROOT-NNN-from-S-NN` | `rollover/ROOT-042-from-S-03` |
| Repo split | `chore/repo-split-domain-name` | `chore/repo-split-notifications` |

---

## 5. PR Requirements

Every PR must pass ALL of the following before merge:

1. **Epic ref present** — PR body contains `ROOT-NNN`
2. **Acceptance criteria linked** — `Satisfies: AC-001, AC-002`
3. **Spec changelog updated** — or reason provided why not
4. **Coding standards checklist** — all boxes checked
5. **No console.log / debug statements** in diff
6. **CI tests passing** — unit tests, TypeScript, lint
7. **No secrets in diff** — automated scanning via git-secrets

---

## 6. Testing Standards

| Test type | Tool | When required |
|---|---|---|
| Unit tests | Jest | Every function with business logic |
| API integration | Supertest | Every new or modified endpoint |
| Component tests | React Testing Library | Every new component |
| E2E (mobile) | Detox | Critical user flows only (auth, reminders, push) |
| Type checking | `tsc --noEmit` | Every PR (CI enforced) |
| Linting | ESLint + Prettier | Every PR (CI enforced) |

### Test file naming
- Unit: `*.test.ts` (co-located with source file)
- Integration: `*.integration.test.ts`
- E2E: `*.e2e.ts` (in `e2e/` directory)

---

## 7. File Organization

```
src/
├── api/                # Express route handlers
│   ├── reminders.ts
│   └── auth.ts
├── db/
│   ├── schema.ts       # Drizzle schema definitions
│   └── migrations/     # Drizzle migration files
├── services/           # Business logic (no HTTP concerns)
│   └── reminderService.ts
├── utils/              # Pure utility functions
│   └── formatDate.ts
├── types/              # Shared TypeScript types
│   └── reminder.ts
└── middleware/          # Express middleware
    └── auth.ts

mobile/
├── screens/            # React Native screens
├── components/         # Shared mobile components
├── navigation/         # React Navigation config
└── services/           # API client layer
```

---

## 8. Security Rules

- **No secrets in code** — all credentials in `.env` only
- **No `eval()` or `Function()` constructors** — ever
- **Zod validation on all external input** — API requests, URL params, form data
- **Parameterized queries only** — Drizzle ORM handles this, but verify
- **CORS configured explicitly** — no wildcard `*` in production
- **Rate limiting on all public endpoints** — Express rate-limit middleware
- **Dependencies audited weekly** — PO tech-scan cron job

---

## 9. Epic Traceability Rules (PLAT-005)

> **Every change in the system must be traceable to an epic. No exceptions.**

### 9.1 Commit Messages — MUST contain epic ref
```
type(EPIC-REF): description

Valid epic refs: ROOT-NNN, PLAT-NNN, INFRA-NNN
```
- Enforced by: `commit-msg` git hook (blocks commit locally)
- Enforced by: `pr-validation.yml` (blocks PR in CI)
- Merge commits are exempt

### 9.2 Branch Names — MUST contain epic ref
```
feat/ROOT-041-reminder-scheduling     ← valid
fix/PLAT-001-token-alert-fix          ← valid
feature/login-fix                     ← BLOCKED by CI
```

### 9.3 PRs — MUST reference epic + acceptance criteria
```
Epic ref: ROOT-041
Satisfies: AC-001, AC-002, AC-003
```

### 9.4 Spec Updates — REQUIRED when code changes
- If you change code → you MUST update the spec's `[CHANGE LOG]` section in the same PR
- The spec file must appear in the PR diff alongside the code changes
- Escape hatch: add `[skip-spec] <reason>` to PR body (dependency bumps, typo fixes)
- `[skip-spec]` is monitored — PO flags if used >3 times per sprint

### 9.5 What to update in specs

| Code change | Spec update required |
|---|---|
| New file added | Add to `[TECH SPEC]` → files touched + `[CHANGE LOG]` entry |
| API endpoint changed | Update `[TECH SPEC]` → endpoint details + `[CHANGE LOG]` entry |
| DB schema changed | Update `[TECH SPEC]` → table definition + `[CHANGE LOG]` entry |
| Bug fix | `[CHANGE LOG]` entry: "Fixed: [description]" |
| Test added | `[CHANGE LOG]` entry only |
| Dependency bump | `[skip-spec]` allowed with reason |
| Config change | `[CHANGE LOG]` entry |
| Refactor (same behavior) | `[skip-spec]` allowed with reason |

### 9.6 Tracing commands
```bash
# All commits for one epic
git log --grep="ROOT-041" --oneline

# All files ever touched by an epic
git log --grep="ROOT-041" --name-only --pretty=format:"" | sort -u

# Which epics touched a file
git log --oneline -- src/api/reminders.ts

# Epic activity in a sprint (date range)
git log --since="2026-04-14" --until="2026-04-18" --oneline \
  | grep -oE '(ROOT|PLAT|INFRA)-[0-9]+' | sort -u

# Commits per epic (velocity)
git log --oneline | grep -oE '(ROOT|PLAT|INFRA)-[0-9]+' | sort | uniq -c | sort -rn
```

---

## 10. Story Points & Epic Sizing Rules (PLAT-006)

### 10.1 Point Scale
| Points | AI Agent | Human Agent | Complexity |
|---|---|---|---|
| 1 | ~1 hour | ~2-3 hours | Trivial — config change, small bug |
| 2 | ~2 hours | ~half day | Small — single endpoint, simple component |
| 3 | ~3 hours | ~1 day | Medium — feature with tests, multi-file |
| 5 | ~5 hours (1 full day) | ~2 days | Large — full feature end-to-end |

### 10.2 Hard Rules
- **Maximum 5 points per epic — no exceptions**
- If estimated >5 → PO MUST split into independently deliverable sub-epics
- Points include the FULL lifecycle: groom → tech spec → code → test → PR → review → deploy → demo → acceptance → done
- Velocity = sum of COMPLETED points per sprint (rolled-over epics don't count)
- PO uses trailing 3-sprint average velocity to load next sprint

### 10.3 Definition of Ready (before coding starts)
- [ ] Business spec written by PO (Saturday planning)
- [ ] Technical spec written by assigned agent (Sunday kickoff)
- [ ] Tech spec approved by Lead Dev
- [ ] Business alignment approved by PO
- [ ] Story points assigned (1, 2, 3, or 5)
- [ ] Acceptance criteria defined (Given/When/Then)
- [ ] No file collision with other in-progress epics

### 10.4 Definition of Done
- [ ] Code complete and follows coding standards
- [ ] All tests passing (unit + integration)
- [ ] PR raised with epic ref + AC links
- [ ] PR reviewed and approved by Lead Dev
- [ ] Spec [CHANGE LOG] updated
- [ ] Merged to main, deployed to staging
- [ ] PO demo script passes
- [ ] {{ADVISOR}} QA green flag issued
- [ ] Spec moved to `finished/` in INDEX.md
