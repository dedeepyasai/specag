# PLAT-009: Testing Standards & SonarQube Quality Gate

## [SUMMARY]
- App: SpecAg
- Epic owner: Lead Dev (standards), PO (enforcement via CI)
- Status: BACKLOG
- Sprint: PC-01 Sprint 1
- Related specs: PLAT-005 (traceability), INFRA-001 (VPS — hosts SonarQube)
- Priority: S2 — no code merges without passing quality gate

## [STORY]
As the team, we need comprehensive test coverage for both UI and backend, enforced by
a SonarQube quality gate that blocks merges when coverage drops or code smells are
introduced — ensuring every PR maintains or improves code quality.

## [TECH SPEC]

### 1. Test Pyramid

```
           ┌──────────┐
           │   E2E    │  Few — critical user flows only
           │  (Detox) │  Runs: Expo EAS / cloud device farm
           ├──────────┤
           │Integration│  Moderate — API endpoints + DB
           │(Supertest)│  Runs: CI (GitHub Actions)
           ├──────────┤
           │   Unit    │  Many — business logic, utils, services
           │  (Jest)   │  Runs: CI + locally before every commit
           └──────────┘
```

### 2. Backend Testing Standards

#### Unit Tests (Jest)
| Rule | Detail |
|---|---|
| **Coverage target** | **80% line coverage minimum** (quality gate blocks below this) |
| **What to test** | Every service function, utility function, validation schema |
| **What NOT to test** | Express route wiring (covered by integration), ORM config |
| **File naming** | `*.test.ts` co-located with source: `reminderService.test.ts` next to `reminderService.ts` |
| **Test structure** | Arrange → Act → Assert pattern |
| **Mocking** | Mock external services (Slack, push providers). Never mock the DB in integration tests. |

```typescript
// Example: src/services/reminderService.test.ts
describe('ReminderService', () => {
  describe('createReminder', () => {
    it('should create a reminder with valid data', async () => {
      // Arrange
      const input = { title: 'Test', scheduledAt: futureDate, userId: 'user-1' };
      // Act
      const result = await reminderService.create(input);
      // Assert
      expect(result.id).toBeDefined();
      expect(result.title).toBe('Test');
      expect(result.status).toBe('scheduled');
    });

    it('should reject past dates', async () => {
      const input = { title: 'Test', scheduledAt: pastDate, userId: 'user-1' };
      await expect(reminderService.create(input)).rejects.toThrow('Date must be in the future');
    });
  });
});
```

#### Integration Tests (Supertest + Jest)
| Rule | Detail |
|---|---|
| **Coverage target** | Every API endpoint has at least one happy path + one error path test |
| **What to test** | Full request → response cycle including DB |
| **Database** | Use real PostgreSQL (Docker test container). **Never mock the DB.** |
| **File naming** | `*.integration.test.ts` |
| **Setup/teardown** | Fresh DB state per test suite (transactions or truncate) |

```typescript
// Example: src/api/reminders.integration.test.ts
describe('POST /api/reminders', () => {
  it('should create a reminder and return 201', async () => {
    const res = await request(app)
      .post('/api/reminders')
      .set('Authorization', `Bearer ${testToken}`)
      .send({ title: 'Test', scheduledAt: futureDate });
    
    expect(res.status).toBe(201);
    expect(res.body.data.id).toBeDefined();
  });

  it('should return 400 for missing title', async () => {
    const res = await request(app)
      .post('/api/reminders')
      .set('Authorization', `Bearer ${testToken}`)
      .send({ scheduledAt: futureDate });
    
    expect(res.status).toBe(400);
    expect(res.body.error).toContain('title');
  });

  it('should return 401 without auth token', async () => {
    const res = await request(app)
      .post('/api/reminders')
      .send({ title: 'Test', scheduledAt: futureDate });
    
    expect(res.status).toBe(401);
  });
});
```

#### Required test cases per endpoint
| HTTP Method | Required Tests |
|---|---|
| POST | Happy path (201), validation error (400), auth failure (401), duplicate handling (409 if applicable) |
| GET | Happy path (200), not found (404), auth failure (401), pagination if applicable |
| PATCH | Happy path (200), not found (404), validation error (400), auth failure (401) |
| DELETE | Happy path (200/204), not found (404), auth failure (401) |

### 3. UI Testing Standards

#### Component Tests (React Testing Library)
| Rule | Detail |
|---|---|
| **Coverage target** | Every component with user interaction or conditional rendering |
| **What to test** | Render output, user interactions, state changes, error states |
| **What NOT to test** | Styling, layout (visual regression is separate), static text |
| **File naming** | `*.test.tsx` co-located with component |

```typescript
// Example: src/components/ReminderForm.test.tsx
describe('ReminderForm', () => {
  it('should render form fields', () => {
    render(<ReminderForm />);
    expect(screen.getByLabelText('Title')).toBeInTheDocument();
    expect(screen.getByLabelText('Date')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Save' })).toBeInTheDocument();
  });

  it('should show validation error for empty title', async () => {
    render(<ReminderForm />);
    fireEvent.click(screen.getByRole('button', { name: 'Save' }));
    expect(await screen.findByText('Title is required')).toBeInTheDocument();
  });

  it('should call onSubmit with form data', async () => {
    const onSubmit = jest.fn();
    render(<ReminderForm onSubmit={onSubmit} />);
    
    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Test' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save' }));
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith(expect.objectContaining({ title: 'Test' }));
    });
  });

  it('should show loading state during submission', async () => {
    render(<ReminderForm />);
    fireEvent.click(screen.getByRole('button', { name: 'Save' }));
    expect(screen.getByText('Saving...')).toBeInTheDocument();
  });

  it('should display server error message', async () => {
    // Mock API failure
    render(<ReminderForm />);
    // ... trigger error
    expect(await screen.findByRole('alert')).toHaveTextContent('Failed to save');
  });
});
```

#### Required UI test cases per component type
| Component Type | Required Tests |
|---|---|
| Form | Render, validation errors, successful submit, loading state, server error |
| List | Render items, empty state, loading state, pagination/infinite scroll |
| Modal/Dialog | Open, close, confirm action, cancel action |
| Navigation | Route renders correct screen, back navigation, deep link |
| Auth-gated | Authenticated view, unauthenticated redirect |

#### E2E Tests (Detox — mobile only)
| Rule | Detail |
|---|---|
| **When to write** | Critical user flows only (auth, core CRUD, push notifications) |
| **Where to run** | Expo EAS / BrowserStack (not on VPS — no simulator) |
| **File naming** | `e2e/*.e2e.ts` |
| **Frequency** | Run on every release build, not every PR |

Required E2E flows:
```
1. Signup → Login → Create reminder → See in list → Logout
2. Login → Edit reminder → Verify updated
3. Login → Delete reminder → Verify removed
4. Login → Receive push notification (when time arrives)
5. Offline → Create reminder → Come online → Verify synced
```

### 4. SonarQube Quality Gate

#### Setup on VPS
```yaml
# docker-compose.yml addition
services:
  sonarqube:
    image: sonarqube:community
    restart: unless-stopped
    ports:
      - "9000:9000"
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://postgres:5432/sonar
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: ${SONAR_DB_PASSWORD}
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_logs:/opt/sonarqube/logs
    deploy:
      resources:
        limits:
          memory: 3G
    depends_on:
      - postgres

volumes:
  sonarqube_data:
  sonarqube_logs:
```

#### Quality Gate Rules (enforced on every PR)

| Metric | Threshold | Action if fails |
|---|---|---|
| **Line coverage** | ≥ 80% on new code | PR blocked |
| **Branch coverage** | ≥ 70% on new code | PR blocked |
| **Duplicated lines** | ≤ 3% on new code | PR blocked |
| **Code smells** | 0 new (A rating) | PR blocked |
| **Bugs** | 0 new | PR blocked |
| **Vulnerabilities** | 0 new | PR blocked |
| **Security hotspots** | All reviewed | PR warning (manual review) |
| **Technical debt ratio** | ≤ 5% on new code | PR warning |

#### SonarQube Scanner in CI

```yaml
# Added to .github/workflows/pr-validation.yml
- name: SonarQube Scan
  uses: SonarSource/sonarqube-scan-action@v3
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

- name: SonarQube Quality Gate
  uses: SonarSource/sonarqube-quality-gate-action@v1
  timeout-minutes: 5
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

#### sonar-project.properties
```properties
sonar.projectKey=rootine
sonar.projectName=SpecAg
sonar.sources=src
sonar.tests=src
sonar.test.inclusions=**/*.test.ts,**/*.test.tsx,**/*.integration.test.ts
sonar.typescript.lcov.reportPaths=coverage/lcov.info
sonar.coverage.exclusions=**/*.test.ts,**/*.test.tsx,**/*.e2e.ts,**/types/**,**/migrations/**
sonar.cpd.exclusions=**/migrations/**
```

#### Weekly Full Scan (beyond PR-level)
```bash
# Cron: every Friday 5 PM (after tech-upgrades scan)
0 17 * * 5  /app/venv/bin/python /app/agents/sonar_full_scan.py
```

Full scan checks:
- Overall project coverage (not just new code)
- All existing code smells, bugs, vulnerabilities
- CVSS scoring on vulnerabilities → feeds into PO severity triage
- Results posted to `#rootine-dev` by PO:

```
*SonarQube Weekly Report — Friday, Apr 18*

*Quality Gate: PASSED*

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Coverage | 84.2% | ≥80% | ✅ |
| Duplications | 1.8% | ≤3% | ✅ |
| Code Smells | 12 total (0 new this week) | 0 new | ✅ |
| Bugs | 0 | 0 | ✅ |
| Vulnerabilities | 1 (CVSS 3.2, S4) | 0 new | ⚠️ existing |
| Tech Debt | 2.1 days | ≤5% ratio | ✅ |

*Action items:*
- 1 existing vulnerability (CVSS 3.2) — S4, deferred to PC-11
- 12 code smells — 8 are in legacy auth module (TechMain candidate)
```

### 5. Test Coverage Requirements Per Epic Type

| Epic Type | Unit Tests | Integration Tests | UI Tests | E2E Tests | SonarQube |
|---|---|---|---|---|---|
| **Task** | Required (80%+) | Required (all endpoints) | Required (all components) | If critical flow | Quality gate must pass |
| **Story** | N/A (no code) | N/A | N/A | N/A | N/A |
| **Prod Issue** | Required (cover the bug) | Required (regression test) | If UI-related | If critical flow | Quality gate must pass |
| **TechMain** | Update existing tests | Update if endpoints change | Update if UI changes | N/A | Quality gate must pass |
| **Feature** (child epics) | Per child epic rules | Per child epic rules | Per child epic rules | At least 1 E2E for feature | Quality gate per PR |

### 6. Test Scripts (package.json)

```json
{
  "scripts": {
    "test": "jest --coverage",
    "test:watch": "jest --watch",
    "test:unit": "jest --testPathPattern='test\\.ts$' --coverage",
    "test:integration": "jest --testPathPattern='integration\\.test\\.ts$' --coverage",
    "test:e2e": "detox test --configuration ios.sim.release",
    "test:ci": "jest --ci --coverage --reporters=default --reporters=jest-junit",
    "lint": "eslint src/ --ext .ts,.tsx",
    "type-check": "tsc --noEmit",
    "quality": "npm run lint && npm run type-check && npm run test:ci"
  }
}
```

### Files Touched
- `.github/workflows/pr-validation.yml` — add SonarQube scan + quality gate steps
- `sonar-project.properties` — SonarQube project configuration
- `docker-compose.yml` — add SonarQube service
- `package.json` — test scripts
- `.sdd/coding-standards.md` — test coverage requirements section
- `jest.config.ts` — Jest configuration with coverage thresholds

## [STANDARDS]
- **80% line coverage minimum** on new code — quality gate blocks merges below this
- **Every endpoint** must have happy path + error path integration tests
- **Every interactive component** must have render + interaction + error state tests
- **Never mock the database** in integration tests — use real PostgreSQL
- **SonarQube quality gate** must pass on every PR — no exceptions, no bypasses
- **Zero new bugs, vulnerabilities, or code smells** per PR
- **E2E tests** run on release builds, not every PR (too slow + needs simulator)
- **Weekly full scan** catches drift in overall project quality

## [ACCEPTANCE CRITERIA]
```
AC-001: Given a PR is raised, when CI runs, then Jest runs with coverage and
        SonarQube quality gate checks pass before merge is allowed.

AC-002: Given a new API endpoint is added, when the PR is reviewed, then it
        includes at minimum: happy path test, validation error test, auth test.

AC-003: Given a new UI component with a form, when the PR is reviewed, then it
        includes: render test, validation error test, submit test, loading state test.

AC-004: Given an integration test, when it runs, then it uses a real PostgreSQL
        container — not a mocked database.

AC-005: Given new code has 75% line coverage (below 80%), when SonarQube quality
        gate runs, then the PR is BLOCKED with a coverage failure message.

AC-006: Given a PR introduces 1 new code smell, when SonarQube scans it, then
        the PR is BLOCKED until the code smell is resolved.

AC-007: Given it is Friday 5 PM, when the weekly full scan runs, then PO posts
        the SonarQube report to #rootine-dev with metrics and action items.

AC-008: Given a Prod Issue hotfix PR, then it must include a regression test
        that specifically covers the bug being fixed.
```

## [CHANGE LOG]
- 2026-04-10: Initial spec created — test pyramid, coverage rules, SonarQube quality gate
