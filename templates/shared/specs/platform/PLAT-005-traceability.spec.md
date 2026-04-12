# PLAT-005: Epic Traceability & Spec-Code Sync Enforcement

## [SUMMARY]
- App: Rootine
- Epic owner: Lead Dev Agent
- Status: BACKLOG
- Sprint: PC-01 Sprint 1
- Related specs: All specs — this is a cross-cutting concern
- Priority: S2 — must be active before any feature development begins

## [STORY]
As Datta (Advisor), when I see a commit, PR, branch, or workflow change, I need to
instantly know WHICH epic caused it. And when code changes, the corresponding spec
must be updated — so the spec always reflects reality, not just the original plan.

## [TECH SPEC]

### Traceability Rule: Every Change Has an Epic

```
RULE 1: Every commit message MUST contain an epic reference (ROOT-NNN or PLAT-NNN or INFRA-NNN)
RULE 2: Every branch MUST be named with an epic reference
RULE 3: Every PR body MUST reference the epic AND list which ACs it satisfies
RULE 4: Every code change MUST trigger a spec [CHANGE LOG] update in the same PR
RULE 5: Every spec change MUST be reviewable in the PR diff
```

### How traceability flows

```
Epic ROOT-041
  ↓
Branch: feat/ROOT-041-reminder-scheduling
  ↓
Commits:
  feat(ROOT-041): add reminder POST endpoint
  feat(ROOT-041): add Zod validation for reminder payload
  test(ROOT-041): add unit tests for reminder service
  docs(ROOT-041): update spec changelog with API changes
  ↓
PR #34:
  Title: "feat(ROOT-041): reminder scheduling API"
  Body: "Epic ref: ROOT-041 | Satisfies: AC-001, AC-002"
  Files changed: src/api/reminders.ts, specs/in-progress/ROOT-041.spec.md
  ↓
Merged → git log shows:
  Every commit traceable to ROOT-041
  Spec updated in same PR
  ↓
git log --grep="ROOT-041" → shows ALL changes for this epic
git log --grep="ROOT-042" → shows ALL changes for that epic
```

### Enforcement Layer 1: Git Commit Hook (local)

Pre-commit hook runs on every commit. Rejects commits without epic reference.

**File:** `.git/hooks/commit-msg`

```bash
#!/bin/bash
# Enforce epic reference in every commit message
# Format: type(EPIC-REF): description
# Valid refs: ROOT-NNN, PLAT-NNN, INFRA-NNN

COMMIT_MSG=$(cat "$1")

# Allow merge commits
if echo "$COMMIT_MSG" | grep -qE '^Merge '; then
  exit 0
fi

# Check for epic reference
if ! echo "$COMMIT_MSG" | grep -qE '\((ROOT|PLAT|INFRA)-[0-9]+\)'; then
  echo ""
  echo "ERROR: Commit message must contain an epic reference."
  echo ""
  echo "Format: type(EPIC-REF): description"
  echo ""
  echo "Examples:"
  echo "  feat(ROOT-041): add reminder scheduling endpoint"
  echo "  fix(PLAT-001): correct token alert threshold"
  echo "  chore(INFRA-001): update Docker compose memory limits"
  echo ""
  echo "Your message: $COMMIT_MSG"
  echo ""
  exit 1
fi

# Check commit type prefix
if ! echo "$COMMIT_MSG" | grep -qE '^(feat|fix|patch|refactor|test|docs|chore|rollover)\('; then
  echo ""
  echo "ERROR: Commit must start with a valid type."
  echo "Valid types: feat, fix, patch, refactor, test, docs, chore, rollover"
  echo ""
  echo "Your message: $COMMIT_MSG"
  echo ""
  exit 1
fi

exit 0
```

### Enforcement Layer 2: GitHub Actions CI (remote)

Runs on every PR. Checks:
1. Commit messages have epic refs
2. PR body has epic ref + AC references
3. If code files changed → spec file MUST also be changed in the same PR
4. Spec [CHANGE LOG] section has a new entry dated today

**File:** `.github/workflows/pr-validation.yml` (updated steps)

```yaml
- name: Validate all commit messages have epic refs
  run: |
    COMMITS=$(git log origin/main..HEAD --pretty=format:"%s")
    while IFS= read -r msg; do
      # Skip merge commits
      if echo "$msg" | grep -qE '^Merge '; then continue; fi
      if ! echo "$msg" | grep -qE '\((ROOT|PLAT|INFRA)-[0-9]+\)'; then
        echo "::error::Commit missing epic ref: $msg"
        echo "Format: type(EPIC-REF): description"
        exit 1
      fi
    done <<< "$COMMITS"

- name: Validate spec updated when code changes
  run: |
    # Get changed files
    CODE_CHANGED=$(git diff --name-only origin/main...HEAD | grep -E '\.(ts|tsx|js|jsx|py|sql)$' || true)
    SPEC_CHANGED=$(git diff --name-only origin/main...HEAD | grep -E '\.spec\.md$' || true)

    if [ -n "$CODE_CHANGED" ] && [ -z "$SPEC_CHANGED" ]; then
      echo "::error::Code files changed but no spec file updated!"
      echo ""
      echo "Code files changed:"
      echo "$CODE_CHANGED"
      echo ""
      echo "RULE: Every code change must update the related spec's [CHANGE LOG] section."
      echo "Add a line like: - 2026-04-10: Updated API endpoint to support PATCH method"
      echo ""
      echo "If no spec change is truly needed, add '[skip-spec]' to your PR description with a reason."
      exit 1
    fi

- name: Validate spec changelog has today's entry
  run: |
    SPEC_FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.spec\.md$' || true)
    TODAY=$(date +%Y-%m-%d)

    for spec in $SPEC_FILES; do
      if ! git diff origin/main...HEAD -- "$spec" | grep -qE "^\+.*$TODAY"; then
        echo "::warning::Spec $spec was modified but no changelog entry for today ($TODAY)."
        echo "Add to [CHANGE LOG]: - $TODAY: <what changed>"
      fi
    done

- name: Extract epic ID for workflow tracking
  run: |
    # Extract epic ID from branch name for tagging
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    EPIC_ID=$(echo "$BRANCH" | grep -oE '(ROOT|PLAT|INFRA)-[0-9]+' || echo "UNKNOWN")
    echo "EPIC_ID=$EPIC_ID" >> $GITHUB_ENV
    echo "Epic detected: $EPIC_ID"
    
    # Tag the PR with the epic label
    if [ "$EPIC_ID" != "UNKNOWN" ]; then
      echo "All commits in this PR are traced to $EPIC_ID"
    else
      echo "::error::Branch name must contain an epic reference (e.g., feat/ROOT-041-description)"
      exit 1
    fi
```

### Enforcement Layer 3: PO Agent Audit (daily)

PO Agent runs a daily audit at 08:00 to catch any drift between code and specs.

```
PO Daily Audit:
1. Read specs/INDEX.md — get all in-progress epics
2. For each in-progress epic:
   a. Read the spec's [TECH SPEC] → files touched list
   b. Run: git log --since="yesterday" --grep="ROOT-NNN" --name-only
   c. Compare: did any file change that's NOT in the spec's files-touched list?
   d. If yes → flag in Slack: "ROOT-NNN: file src/new-file.ts was modified but not listed in spec"
3. Check: any commits since yesterday WITHOUT an epic ref? (shouldn't exist with hook, but safety net)
4. Report findings in morning Slack message
```

### [skip-spec] Escape Hatch

Sometimes a code change genuinely doesn't need a spec update (e.g., fixing a typo, updating a dependency version). For these cases:

- Developer adds `[skip-spec]` to the PR description
- Must include a reason: `[skip-spec] Dependency version bump only, no behavior change`
- CI accepts the PR without spec change
- PO Agent logs the skip in `status.log` for audit trail
- If `[skip-spec]` is used more than 3 times in one sprint, PO flags it in the daily report

### Git Commands for Epic Tracing

These commands let Datta or any agent trace changes back to epics:

```bash
# See ALL commits for a specific epic
git log --grep="ROOT-041" --oneline

# See ALL files ever touched by an epic
git log --grep="ROOT-041" --name-only --pretty=format:"" | sort -u

# See which epics touched a specific file
git log --oneline -- src/api/reminders.ts

# See all epics active in a date range
git log --since="2026-04-14" --until="2026-04-18" --oneline | grep -oE '(ROOT|PLAT|INFRA)-[0-9]+' | sort -u

# See how many commits per epic (velocity metric)
git log --oneline | grep -oE '(ROOT|PLAT|INFRA)-[0-9]+' | sort | uniq -c | sort -rn

# Blame a file to see which epic introduced each line
git blame src/api/reminders.ts
# Output: abc1234 (Lead Dev 2026-04-15) feat(ROOT-041): ...
```

### Spec Update Requirements Per Change Type

| Change type | What to update in spec | Required? |
|---|---|---|
| New file added | Add to [TECH SPEC] → files touched | YES |
| API endpoint changed | Update [TECH SPEC] → endpoint details | YES |
| DB schema changed | Update [TECH SPEC] → DB table definition | YES |
| Bug fix (no spec change) | Add [CHANGE LOG] entry: "Fixed: [description]" | YES |
| Test added | Add [CHANGE LOG] entry only | YES |
| Dependency bump | [skip-spec] allowed with reason | NO |
| Config/env change | Add [CHANGE LOG] entry | YES |
| Refactor (same behavior) | [skip-spec] allowed with reason | NO |

### Files Touched
- `.git/hooks/commit-msg` — local git hook (auto-installed on VPS setup)
- `.github/workflows/pr-validation.yml` — CI enforcement
- `/app/agents/po_daily_audit.py` — PO's daily drift check
- `.sdd/coding-standards.md` — traceability rules section

## [STANDARDS]
- ZERO tolerance for commits without epic references (hook blocks it)
- ZERO tolerance for PRs without spec updates (CI blocks it, unless [skip-spec] with reason)
- [skip-spec] is an escape hatch, not a habit — PO monitors usage
- Spec [CHANGE LOG] is append-only — never delete previous entries
- Branch names MUST contain epic ID — CI validates this

## [ACCEPTANCE CRITERIA]
```
AC-001: Given a developer tries to commit "fix login bug" (no epic ref), when
        the commit-msg hook runs, then the commit is REJECTED with a helpful
        error message showing the correct format.

AC-002: Given a developer commits "feat(ROOT-041): add reminder endpoint", when
        the hook runs, then the commit is ACCEPTED.

AC-003: Given a PR changes src/api/reminders.ts but no spec file is modified,
        when CI runs, then the PR is BLOCKED with an error requiring spec update.

AC-004: Given a PR changes src/api/reminders.ts and includes [skip-spec] with
        a reason in the PR body, when CI runs, then the PR is ACCEPTED.

AC-005: Given Datta runs "git log --grep=ROOT-041 --oneline", then ALL commits
        related to ROOT-041 are shown — complete traceability.

AC-006: Given PO runs the daily audit, when a file was changed that's not in
        the spec's files-touched list, then PO flags it in Slack.

AC-007: Given [skip-spec] is used 4 times in Sprint S-03, when PO generates the
        daily report, then it includes a warning about excessive spec skips.

AC-008: Given a branch is named "feature/login-fix" (no epic ID), when CI runs,
        then the PR is BLOCKED with an error requiring epic ID in branch name.
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created — commit hook, CI checks, PO audit, skip-spec escape hatch
