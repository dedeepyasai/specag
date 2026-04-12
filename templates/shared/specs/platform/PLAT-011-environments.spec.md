# PLAT-011: Environment Strategy & Deployment Pipeline

## [SUMMARY]
- App: SpecAg
- Epic owner: Lead Dev (implementation), Datta (QA gate between envs)
- Status: BACKLOG
- Sprint: PC-01 Sprint 0
- Related specs: INFRA-001 (VPS), PLAT-009 (testing), PLAT-012 (rollback)
- Priority: S1 — must be configured before any feature code deploys

## [STORY]
As the team, we need separate Development and Production environments with a 1-sprint
delay between them — code deploys to Dev in Sprint N, Datta QA's in Sprint N+1, and
only after approval does it promote to Production. This ensures no untested code
reaches real users.

## [TECH SPEC]

### 1. Environment Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    SPRINT N                                │
│                                                            │
│  Agents code → PR → CI passes → Merge to main             │
│       │                                                    │
│       ▼                                                    │
│  ┌──────────────────┐                                      │
│  │   DEVELOPMENT     │  ← auto-deploy on merge to main    │
│  │   ENVIRONMENT     │                                      │
│  │                    │  Web: dev.rootine.app               │
│  │                    │  API: api-dev.rootine.app           │
│  │                    │  Mobile: Expo Dev build              │
│  │                    │  DB: PostgreSQL (dev)                │
│  └────────┬─────────┘                                      │
│           │                                                 │
│           │  PO runs demo script against Dev env            │
│           │  PO accepts epic (DEMO_PASSED)                  │
│           ▼                                                 │
│  Epic status: DEMO_PASSED — waiting for Datta QA           │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                    SPRINT N+1                               │
│                                                            │
│  Datta QA's Sprint N's work on Dev environment             │
│       │                                                    │
│       ├── Green flag → Epic ACCEPTED                       │
│       │                                                    │
│       └── Bug found → Datta creates Prod Issue epic        │
│           (assigned to agent in current sprint)             │
│                                                            │
│  End of Sprint N+1 (Saturday):                              │
│       │                                                    │
│       ▼                                                    │
│  ┌──────────────────┐                                      │
│  │   PRODUCTION      │  ← manual promotion (Datta approves)│
│  │   ENVIRONMENT     │                                      │
│  │                    │  Web: rootine.app                    │
│  │                    │  API: api.rootine.app                │
│  │                    │  Mobile: App Store / Play Store      │
│  │                    │  DB: PostgreSQL (prod)               │
│  └──────────────────┘                                      │
└──────────────────────────────────────────────────────────┘
```

### 2. Environment Details

| Field | Development | Production |
|---|---|---|
| **Purpose** | Agent testing, PO demos, Datta QA | Real users |
| **Web URL** | `dev.rootine.app` | `rootine.app` |
| **API URL** | `api-dev.rootine.app` | `api.rootine.app` |
| **Mobile** | Expo Dev build (internal) | App Store + Play Store |
| **Database** | PostgreSQL (dev instance) | PostgreSQL (prod instance, separate) |
| **Deploy trigger** | Auto on merge to `main` | Manual — Datta approves promotion |
| **Who tests** | PO (demo script), agents (integration tests) | End users |
| **Data** | Seed data + test data | Real user data |
| **Hosting** | Vercel (preview) + Expo EAS (dev) | Vercel (production) + App Store/Play |
| **Git branch** | `main` | `release/vN.N.N` (tagged from main) |

### 3. Deployment Flow — Sprint by Sprint

```
SPRINT 0 (Setup):
  Configure both environments
  No feature code — infra only

SPRINT 1 (first feature sprint):
  Agents build features → merge to main → auto-deploy to DEV
  PO demos on DEV → accepts epics
  NO production deploy yet (nothing to promote)

SPRINT 2:
  Agents build Sprint 2 features → deploy to DEV
  Datta QA's Sprint 1 features on DEV environment
    ├── Green flag: Epic marked ACCEPTED
    └── Bug found: Datta creates bug epic (fixed in Sprint 2)
  End of Sprint 2: Sprint 1 features (all accepted) → promoted to PRODUCTION
  Release tag: v1.0.0

SPRINT 3:
  Agents build Sprint 3 features → deploy to DEV
  Datta QA's Sprint 2 features on DEV
  End of Sprint 3: Sprint 2 features → promoted to PRODUCTION
  Release tag: v1.1.0

...and so on (1-sprint delay always maintained)
```

### 4. The 1-Sprint QA Delay

| Sprint | What deploys to DEV | What Datta QA's | What goes to PROD |
|---|---|---|---|
| S-01 | S-01 features | Nothing (first sprint) | Nothing |
| S-02 | S-02 features | S-01 features | S-01 features (end of S-02) |
| S-03 | S-03 features | S-02 features | S-02 features (end of S-03) |
| S-04 | S-04 features | S-03 features | S-03 features (end of S-04) |
| S-05 | S-05 features | S-04 features | S-04 features (end of S-05) |
| S-01 (next PC) | New features | S-05 features | S-05 features |

### 5. Datta's QA Process (Sprint N+1)

```
Sunday–Saturday of Sprint N+1:
  Datta receives list of Sprint N epics to QA (posted by PO on Saturday)
  For each epic:
    1. Open Dev environment (dev.rootine.app)
    2. Test against acceptance criteria (AC-001, AC-002, etc.)
    3. Test on web browser
    4. Test on iOS (Expo Dev build or TestFlight)
    5. Test on Android (Expo Dev build or internal track)
    6. Decision:
       ├── PASS: Type "green flag ROOT-NNN" in Slack
       │         → PO marks ACCEPTED
       │         → Queued for production promotion
       └── FAIL: Type "bug ROOT-NNN: [description]" in Slack
                 → PO creates Prod Issue epic
                 → Assigned to developer in CURRENT sprint
                 → Must be fixed before end of sprint
                 → Datta re-tests after fix deployed to DEV

Saturday of Sprint N+1:
  All Sprint N epics either ACCEPTED or bug-fixed and re-tested
  PO prepares promotion list
  Datta approves production deployment
  PO/Lead Dev runs promotion script
```

### 6. Production Promotion Process

```bash
# Only runs on Saturday after Datta approval
# Creates a release branch + tag from current main

# Step 1: Create release tag
git tag -a v1.1.0 -m "Release v1.1.0 — Sprint S-02 features"
git push origin v1.1.0

# Step 2: Vercel auto-deploys tagged releases to production
# (configured in Vercel: production branch = release tags)

# Step 3: Expo EAS builds production mobile app
eas build --platform all --profile production

# Step 4: Submit to App Store / Play Store
eas submit --platform ios
eas submit --platform android

# Step 5: PO confirms in Slack
# "v1.1.0 deployed to production. Sprint S-02 features live."
```

### 7. Versioning (Semantic Versioning)

```
Format: vMAJOR.MINOR.PATCH

MAJOR: Increments at each PC boundary (v1.x.x = PC-01, v2.x.x = PC-02)
MINOR: Increments at each sprint promotion (v1.1.0 = Sprint 1, v1.2.0 = Sprint 2)
PATCH: Increments for hotfixes between sprints (v1.1.1 = hotfix on Sprint 1 release)

Examples:
  v1.0.0 — PC-01 Sprint 1 features (first production release)
  v1.1.0 — PC-01 Sprint 2 features
  v1.1.1 — Hotfix for S1 prod bug during Sprint 3
  v1.2.0 — PC-01 Sprint 3 features
  v2.0.0 — PC-02 Sprint 1 features (new PC = major version bump)
```

### 8. Hotfix Path (bypasses 1-sprint delay)

For S1 Prod Issues that need immediate production fix:

```
S1 bug reported in PRODUCTION
  → Lead Dev fixes on hotfix/ROOT-NNN branch
  → Fast-track PR review (Lead Dev self-reviews if alone)
  → Merge to main → auto-deploy to DEV
  → Quick Datta QA on DEV (within hours, not next sprint)
  → If green: cherry-pick to release branch
  → Deploy to PRODUCTION immediately
  → Tag: v1.1.1 (patch version)
  → Normal retro covers the incident
```

### 9. Database Strategy Per Environment

| Aspect | Development DB | Production DB |
|---|---|---|
| Host | Same VPS (Docker, port 5432) | Same VPS (Docker, port 5433) OR separate managed DB |
| Data | Seed data + test data, can be wiped | Real user data, never wiped |
| Migrations | Run automatically on deploy | Run manually after Datta approval |
| Backups | Weekly (VPS snapshot) | Daily automated + before every promotion |
| Access | All agents + Datta | Read: PO (reports). Write: deploy script only |

### 10. GitHub Actions — Environment Deploy Config

```yaml
# .github/workflows/deploy-dev.yml
name: Deploy to Development
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: development
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Vercel (preview)
        run: vercel deploy --token=${{ secrets.VERCEL_TOKEN }}
      - name: Notify Slack
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text": "Deployed to DEV: dev.rootine.app — commit: ${{ github.sha }}"}'

# .github/workflows/deploy-prod.yml
name: Deploy to Production
on:
  push:
    tags: ['v*.*.*']
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Vercel (production)
        run: vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}
      - name: Notify Slack
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text": "🚀 PRODUCTION DEPLOY: rootine.app — ${{ github.ref_name }}"}'
```

### Files Touched
- `.github/workflows/deploy-dev.yml` — auto-deploy to Dev on merge
- `.github/workflows/deploy-prod.yml` — deploy to Prod on release tag
- `docker-compose.yml` — separate dev and prod DB containers
- `.sdd/project.config.yaml` — environment URLs
- `CHANGELOG.md` — release notes per version

## [STANDARDS]
- Dev deploys are automatic (merge to main). Prod deploys are manual (Datta approves).
- 1-sprint QA delay is ALWAYS maintained — no shortcuts except S1 hotfix path
- Every production promotion gets a semantic version tag
- Database migrations to prod require Datta approval
- Production database backups run before every promotion
- Hotfixes bypass the delay but still require Datta QA (within hours, not next sprint)

## [ACCEPTANCE CRITERIA]
```
AC-001: Given an agent merges a PR to main, then code auto-deploys to Dev
        environment within 5 minutes and Slack is notified.

AC-002: Given Datta QA's Sprint 1 features during Sprint 2, when all epics
        get green flags, then PO prepares promotion list for end of Sprint 2.

AC-003: Given Datta approves production promotion, when Lead Dev tags v1.1.0
        and pushes, then production deploys automatically and Slack is notified.

AC-004: Given Datta finds a bug during QA, when he types "bug ROOT-NNN: description"
        in Slack, then PO creates a Prod Issue epic assigned in the current sprint.

AC-005: Given an S1 production bug, when Lead Dev fixes and Datta QA's on Dev,
        then the fix is cherry-picked to release branch and deployed to prod
        within hours (bypasses 1-sprint delay).

AC-006: Given a production promotion is about to happen, then a database backup
        runs before the deployment begins.

AC-007: Given Sprint 3 features are on Dev and Sprint 2 features are on Prod,
        then Dev and Prod are running different code versions simultaneously.
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created — Dev/Prod split, 1-sprint delay, semver, hotfix path
