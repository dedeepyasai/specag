# PLAT-012: Rollback Mechanism

## [SUMMARY]
- App: Rootine
- Epic owner: Lead Dev (implementation), Datta (approval gate)
- Status: BACKLOG
- Sprint: PC-01 Sprint 0
- Related specs: PLAT-011 (environments), INFRA-001 (VPS)
- Priority: S1 — safety net for every production deployment

## [STORY]
As the team, we need a reliable rollback mechanism so that if a production deployment
introduces critical bugs, we can revert to the previous working version within minutes.
The rollback must cover all layers — web app, API, mobile builds, and database — and
be triggerable via a simple Slack command by Datta.

## [TECH SPEC]

### 1. Rollback Philosophy

```
Every production promotion creates a "restore point."
Rollback = revert to the previous restore point.
The system ALWAYS has exactly one rollback target: the previous release tag.

Current Production: v1.2.0 (Sprint 3 features)
Rollback Target:    v1.1.0 (Sprint 2 features)

After rollback:
Current Production: v1.1.0
Rollback Target:    v1.0.0
```

### 2. Rollback Triggers

| Trigger | Who | When |
|---|---|---|
| **Slack command** | Datta types `rollback production` | Any time after a bad deploy |
| **Failed health check** | Automated (GitHub Actions) | Within 5 min of deploy |
| **Critical bug in prod** | Datta decides after user report | During business hours |

**Rollback does NOT happen automatically** — Datta always approves, even if health
check fails. The system alerts Datta, and he decides.

### 3. Rollback Scope — What Gets Reverted

| Layer | Rollback Method | Time to Revert |
|---|---|---|
| **Web (Vercel)** | Vercel instant rollback to previous deployment | < 1 minute |
| **API (Vercel/VPS)** | Redeploy previous release tag | < 3 minutes |
| **Mobile (Expo)** | OTA update to previous JS bundle (Expo Updates) | < 5 minutes |
| **Mobile (native)** | Cannot rollback App Store/Play Store — use OTA | N/A |
| **Database** | Reverse migration OR restore from pre-deploy backup | 5–15 minutes |

### 4. Web & API Rollback (Vercel)

```bash
# Option A: Vercel instant rollback (preferred)
# Vercel keeps every deployment — rollback is just promoting the previous one
vercel rollback --token=${{ secrets.VERCEL_TOKEN }}

# Option B: Redeploy previous tag
git checkout v1.1.0
vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}
```

Vercel maintains deployment history. Every deploy gets a unique URL. "Rollback" simply
re-points the production domain to the previous deployment — zero downtime.

### 5. Mobile Rollback (Expo OTA Updates)

```bash
# Expo EAS Update allows OTA (Over-The-Air) JS bundle updates
# No App Store/Play Store review needed for JS-only changes

# Roll back by publishing the previous update bundle
eas update --branch production --message "Rollback to v1.1.0"

# If the bad release included NATIVE changes (new native modules):
# Cannot OTA rollback — must submit new App Store/Play Store build
# This is rare — most changes are JS-only with Expo
```

**OTA Rollback Flow:**
```
v1.2.0 deployed to App Store (native + JS)
  → Bug found in JS layer
  → Publish OTA update pointing to v1.1.0 JS bundle
  → Users get v1.1.0 JS on next app open (within minutes)
  → No App Store review needed

v1.2.0 deployed with NEW native module
  → Bug in native layer
  → Cannot OTA — must build v1.2.1 hotfix
  → Submit to App Store (1-2 day review)
  → Use PLAT-011 hotfix path
```

### 6. Database Rollback

Database rollback is the most complex layer. Two strategies:

#### Strategy A: Reverse Migration (preferred for schema changes)

```typescript
// Every migration file has an UP and DOWN
// Example: migrations/0005_add_push_tokens.ts

export async function up(db: PostgresJsDatabase) {
  await db.execute(sql`
    ALTER TABLE users ADD COLUMN push_token TEXT;
    CREATE INDEX idx_users_push_token ON users(push_token);
  `);
}

export async function down(db: PostgresJsDatabase) {
  await db.execute(sql`
    DROP INDEX IF EXISTS idx_users_push_token;
    ALTER TABLE users DROP COLUMN IF EXISTS push_token;
  `);
}
```

```bash
# Run reverse migration
npx drizzle-kit down

# Verify schema matches previous version
npx drizzle-kit check
```

#### Strategy B: Backup Restore (for data corruption or failed migration)

```bash
# Pre-deploy backup is ALWAYS taken (PLAT-011 requirement)
# Backup file: /opt/rootine/backups/pre-deploy-v1.2.0-20260425.sql

# Step 1: Stop API to prevent new writes
systemctl stop rootine-api

# Step 2: Restore from backup
pg_restore -h localhost -p 5433 -U rootine_prod -d rootine_prod \
  --clean --if-exists \
  /opt/rootine/backups/pre-deploy-v1.2.0-20260425.sql

# Step 3: Restart API (now pointing to rolled-back data)
systemctl start rootine-api
```

#### Which strategy to use:

| Situation | Strategy |
|---|---|
| Schema change only (add column, index) | A — Reverse migration |
| Data migration (transform existing data) | B — Backup restore |
| Migration failed mid-way (partial state) | B — Backup restore |
| No DB changes in this release | Skip — no DB rollback needed |

### 7. Rollback Script (Full Orchestration)

```bash
#!/bin/bash
# scripts/rollback-production.sh
# Called by Lead Dev after Datta approves rollback
# Usage: ./rollback-production.sh v1.1.0

set -euo pipefail

ROLLBACK_TAG=$1
CURRENT_TAG=$(git describe --tags --abbrev=0)

echo "=== PRODUCTION ROLLBACK ==="
echo "Rolling back from: $CURRENT_TAG"
echo "Rolling back to:   $ROLLBACK_TAG"
echo ""

# Step 1: Verify rollback tag exists
if ! git rev-parse "$ROLLBACK_TAG" >/dev/null 2>&1; then
  echo "ERROR: Tag $ROLLBACK_TAG does not exist"
  exit 1
fi

# Step 2: Pre-rollback database backup (safety net for the rollback itself)
echo "[1/6] Taking pre-rollback database backup..."
BACKUP_FILE="/opt/rootine/backups/pre-rollback-$(date +%Y%m%d-%H%M%S).sql"
pg_dump -h localhost -p 5433 -U rootine_prod rootine_prod > "$BACKUP_FILE"
echo "  Backup saved: $BACKUP_FILE"

# Step 3: Rollback web/API (Vercel)
echo "[2/6] Rolling back Vercel deployment..."
vercel rollback --token="$VERCEL_TOKEN"
echo "  Vercel rolled back"

# Step 4: Rollback database (if needed)
echo "[3/6] Checking if database rollback needed..."
MIGRATION_DIFF=$(git diff "$ROLLBACK_TAG".."$CURRENT_TAG" -- "src/db/migrations/")
if [ -n "$MIGRATION_DIFF" ]; then
  echo "  Database changes detected — running reverse migration"
  git checkout "$ROLLBACK_TAG" -- src/db/migrations/
  npx drizzle-kit down
  echo "  Database rolled back"
else
  echo "  No database changes — skipping DB rollback"
fi

# Step 5: Rollback mobile (OTA)
echo "[4/6] Publishing OTA rollback for mobile..."
git checkout "$ROLLBACK_TAG"
eas update --branch production --message "Rollback to $ROLLBACK_TAG"
echo "  OTA update published"

# Step 6: Tag the rollback
echo "[5/6] Creating rollback tag..."
PATCH_VERSION=$(echo "$CURRENT_TAG" | sed 's/.*\.\([0-9]*\)$/\1/')
NEW_PATCH=$((PATCH_VERSION + 1))
ROLLBACK_VERSION=$(echo "$CURRENT_TAG" | sed "s/\.[0-9]*$/.$NEW_PATCH/")
git tag -a "$ROLLBACK_VERSION" -m "Rollback from $CURRENT_TAG to $ROLLBACK_TAG"
git push origin "$ROLLBACK_VERSION"
echo "  Tagged as $ROLLBACK_VERSION"

# Step 7: Notify Slack
echo "[6/6] Notifying Slack..."
curl -X POST "$SLACK_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"⚠️ PRODUCTION ROLLBACK: $CURRENT_TAG → $ROLLBACK_TAG (tagged $ROLLBACK_VERSION). Reason: Datta-approved rollback.\"}"

echo ""
echo "=== ROLLBACK COMPLETE ==="
echo "Production is now running: $ROLLBACK_TAG"
echo "Rollback tagged as: $ROLLBACK_VERSION"
```

### 8. Slack Commands for Rollback

```
Datta types: "rollback production"
  → Bot responds:
    ┌──────────────────────────────────────┐
    │  ⚠️ ROLLBACK CONFIRMATION            │
    │                                       │
    │  Current: v1.2.0 (Sprint 3 features) │
    │  Target:  v1.1.0 (Sprint 2 features) │
    │                                       │
    │  This will:                           │
    │  • Revert web app to v1.1.0           │
    │  • Revert API to v1.1.0              │
    │  • Push OTA update to mobile          │
    │  • Reverse DB migrations (if any)     │
    │                                       │
    │  Type "confirm rollback" to proceed   │
    │  Type "cancel" to abort               │
    └──────────────────────────────────────┘

Datta types: "confirm rollback"
  → Bot runs rollback script
  → Bot posts results to Slack

Datta types: "rollback status"
  → Bot responds with current production version + rollback target
```

### 9. Health Check After Deploy (Auto-Alert)

```yaml
# .github/workflows/deploy-prod.yml (addition to PLAT-011 workflow)
# After production deploy, run health checks

  post-deploy-health:
    needs: deploy
    runs-on: ubuntu-latest
    steps:
      - name: Wait for deployment to propagate
        run: sleep 30

      - name: Health check — web
        run: |
          HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://rootine.app)
          if [ "$HTTP_STATUS" != "200" ]; then
            echo "WEB HEALTH CHECK FAILED: HTTP $HTTP_STATUS"
            curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
              -d '{"text": "🚨 PRODUCTION HEALTH CHECK FAILED — web returned HTTP '$HTTP_STATUS'. @Datta: type `rollback production` to revert."}'
            exit 1
          fi

      - name: Health check — API
        run: |
          HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.rootine.app/health)
          if [ "$HTTP_STATUS" != "200" ]; then
            echo "API HEALTH CHECK FAILED: HTTP $HTTP_STATUS"
            curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
              -d '{"text": "🚨 PRODUCTION HEALTH CHECK FAILED — API returned HTTP '$HTTP_STATUS'. @Datta: type `rollback production` to revert."}'
            exit 1
          fi

      - name: Health check passed
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text": "✅ Production health check passed — ${{ github.ref_name }} is live and healthy."}'
```

### 10. Rollback Decision Matrix

| Situation | Severity | Action |
|---|---|---|
| Web returns 5xx after deploy | S1 | Alert Datta → rollback if confirmed |
| API health check fails | S1 | Alert Datta → rollback if confirmed |
| Critical user-facing bug | S1 | Datta decides: rollback OR hotfix |
| Minor UI bug | S3 | Do NOT rollback — fix in next sprint |
| Performance degradation (>2x latency) | S2 | Alert Datta → investigate → maybe rollback |
| Database migration failed | S1 | Restore from pre-deploy backup |
| Mobile app crash on launch | S1 | Push OTA rollback immediately |

### 11. Rollback Log

Every rollback is logged in `CHANGELOG.md` and `sprints/S-NN/rollback-log.md`:

```markdown
# Rollback Log — Sprint S-03

## Rollback #1
- **Date:** 2026-05-23 14:30 CST
- **Rolled back from:** v1.2.0
- **Rolled back to:** v1.1.0
- **Tagged as:** v1.2.1
- **Reason:** API health check failed — /api/tasks returning 500
- **Root cause:** Migration 0005 had a typo in column name
- **Time to rollback:** 4 minutes
- **Approved by:** Datta
- **Executed by:** Lead Dev
- **Post-mortem:** Fix migration, re-test, re-promote in Sprint S-04
```

### Files Touched
- `scripts/rollback-production.sh` — orchestrated rollback script
- `.github/workflows/deploy-prod.yml` — health check addition (post-deploy)
- `sprints/S-NN/rollback-log.md` — per-sprint rollback log (if rollback occurs)
- `CHANGELOG.md` — rollback events recorded
- `/app/agents/slack_commands.py` — rollback Slack commands

## [STANDARDS]
- Rollback ALWAYS requires Datta's approval (no automatic rollbacks)
- Pre-deploy database backup is mandatory before every promotion (PLAT-011)
- Pre-rollback database backup is taken before executing rollback (safety net)
- Every migration MUST have a `down()` function for reverse migration
- Rollback is tagged with a PATCH version increment (v1.2.0 → v1.2.1)
- Rollback events are logged in CHANGELOG.md and sprint rollback log
- Health check runs automatically after every production deploy
- Health check failure alerts Datta but does NOT auto-rollback

## [ACCEPTANCE CRITERIA]
```
AC-001: Given a production deploy just completed, when health checks run within
        5 minutes, then web and API endpoints are verified and Slack is notified
        of pass/fail.

AC-002: Given a health check fails, when Datta is alerted in Slack, then he can
        type "rollback production" and the bot shows confirmation with current
        version and rollback target.

AC-003: Given Datta confirms rollback, when the rollback script runs, then web,
        API, and mobile are reverted to the previous release tag within 5 minutes.

AC-004: Given a rollback involves database changes, when reverse migration runs,
        then the database schema matches the previous release version.

AC-005: Given a rollback involves data corruption, when backup restore is chosen,
        then the pre-deploy backup is restored and API is restarted.

AC-006: Given a rollback completes, then a PATCH version tag is created, Slack
        is notified, and the rollback is logged in CHANGELOG.md.

AC-007: Given the mobile app has a JS-only bug in production, when OTA rollback
        is published, then users receive the previous JS bundle on next app open.

AC-008: Given every migration file, then it MUST include both up() and down()
        functions — PR validation enforces this.
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created — full-stack rollback, Slack commands, health checks, decision matrix
