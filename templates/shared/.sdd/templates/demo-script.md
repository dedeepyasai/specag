# Demo Script Template — Sprint S-NN

> **Purpose:** A 5-minute structured demo so the team and Datta can SEE working
> software at the end of every epic, not just read about it. Working software is
> the primary measure of progress (Bible §1.1).
>
> **Owner:** Whoever delivered the epic (Lead Dev or Associate).
> **Audience:** Datta (acceptance), PO (verification), other agents (awareness).
> **When:** Before the epic moves to ACCEPTED. Posted to `#rootine-dev`.
> **Format:** Slack post + linked staging/screenshots/cURL transcript.
> **Length cap:** 5 minutes to read or watch. If it takes longer, you're showing too much.

---

## 1. Header (15 seconds)

```
*Demo — <EPIC-ID> — <Epic Title>*

Sprint:        S-NN
Owner:         Lead Dev | Associate
Story points:  N
Spec:          [link to spec file]
PR:            [link to merged PR]
Staging:       [link to where it's running] OR [N/A — backend only]
```

## 2. What Shipped (30 seconds)

One paragraph, plain language. No jargon. What does this epic actually let
someone DO that they couldn't do before?

> Example: "Users can now receive a push notification when their reminder
> fires. Previously, the reminder only appeared inside the app. The notification
> works on iOS and Android, respects the user's quiet-hours setting, and falls
> back to a silent in-app banner if the device has notifications disabled."

## 3. Live Demo (2-3 minutes)

Pick the form that fits the epic. Don't do all of them — pick ONE.

### Option A — UI epic (web or mobile)
- Link to staging URL or TestFlight build number.
- 3-5 screenshots OR a 60-second screen recording.
- Walk through the GOLDEN PATH (the most common user flow).
- Show ONE edge case (error state, empty state, or boundary).

### Option B — API / backend epic
- Paste a working `curl` transcript showing the request and response.
- Show the success response.
- Show ONE error response (4xx or 5xx) with the right status code.
- If a DB row was created/updated, paste the relevant row(s).

### Option C — Infrastructure / platform epic
- Paste the command(s) that prove the thing works (e.g., `docker ps`, cron output, log tail, dashboard screenshot).
- Show the BEFORE state and the AFTER state if relevant.
- For monitoring/alerting epics, show a sample alert firing in the test channel.

### Option D — Process / methodology epic (PLAT-* docs)
- Link to the new/changed Bible section or spec.
- Show the workflow running in practice (e.g., a real ceremony post, a real retro entry).
- Skip a code demo — the artifact IS the demo.

## 4. Acceptance Proof (1 minute)

Walk down the spec's [ACCEPTANCE CRITERIA] block. For each AC, paste a
one-line confirmation.

```
AC-001: Push notification fires within 30 seconds of reminder time.
        ✅ Verified — staging log shows fire at 14:00:03 for 14:00:00 reminder.

AC-002: Notification respects quiet-hours.
        ✅ Verified — set quiet-hours 22:00–08:00, fired reminder at 23:30,
           in-app banner appeared, no push sent.

AC-003: Falls back to in-app banner if device notifications disabled.
        ✅ Verified — disabled notifications in iOS settings, fired reminder,
           banner appeared in-app.
```

If any AC is NOT verified, the epic is NOT done. Move it back to IN PROGRESS,
do NOT post the demo as if it passed.

## 5. Next Steps (15 seconds)

Pick ONE:
- **Ready for acceptance** — `@datta please QA + green flag.`
- **Known follow-ups** — list any TechMain epics this surfaced, link to them.
- **Blocked on** — if the demo reveals a downstream gap, name it and tag the owner.

---

## What this template is NOT

- NOT a status report. Status goes in the daily report (PLAT-006 §3.4).
- NOT a sales pitch. No marketing language, no superlatives.
- NOT a place to explain WHY you built it that way. That's the spec.
- NOT a place to hide problems. Problems get raised in §5 explicitly.

## Rules

- Every epic MUST have a demo before it can move to ACCEPTED. No exceptions for "trivial" epics — even a 1-pt config change gets a 30-second demo.
- The demo MUST show the system actually working. Screenshots of code are NOT a demo. Test output that says "PASS" is NOT a demo. The demo shows the thing DOING the thing.
- If the epic cannot be demoed (e.g., a hidden internal refactor), the spec MUST explicitly mark it `demoable: false` in frontmatter and link to the proxy verification (test suite, before/after benchmark, log diff).
- Demos older than 7 days MUST be re-run on current main before acceptance. Stale demos lie.
