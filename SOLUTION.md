# LeaderFactor — Solution Spec

_Source of truth for what we're building and why. Decisions below are locked; see "Scope cuts" for what's deliberately out._

## Bird's eye view

**Who it's for:** learning **managers** — not the L&D admin buyer. Customer interviews found manager involvement is the biggest lever on whether a learner keeps engaging with their action plan after training. So we build for the manager.

**The bet:** give managers (1) visibility into their team's engagement, framed competitively against the company average, and (2) a one-click way to act on it that fits their existing workflow. Visibility + light social pressure + a frictionless nudge → more manager involvement → more learner engagement → (the real goal) behavior change at re-assessment.

**What it does:**
1. A manager **dashboard** that makes team engagement visible at a glance.
2. A weekly **Monday email** that pulls the manager back in with their headline number + a link.
3. A **Schedule 1:1** action, in both places, that turns "my team is behind" into a booked conversation in one click.

## The metric: check-in completion

The whole dashboard hangs on one number.

- **Expected check-ins** for a learner = `2 × (weeks since their plan was created)` — tied to the existing twice-weekly reminder cadence. Computed as a float (`2 × days_active / 7`), floored defensively to avoid divide-by-zero on a brand-new plan.
- **Actual** = count of that learner's check-ins.
- **Completion %** (per learner, for the table) = `actual / expected`, capped at 100%.
- **Completed plans count as 100%** — a finished action plan is fulfilled by definition, so check-in cadence only judges learners still mid-plan (active/abandoned). This flows into the aggregate too, so the table column and headline stay consistent.
- **Team completion** = aggregate `Σ effective / Σ expected` across the manager's learners (weights by tenure; robust to one outlier), capped at 100%.
- **Company completion** = same aggregate across all learners (the single seeded company).

Against the seed this yields a real spread — **Tim Cook 43%, company 30%, Indra 26%, Sheryl 17%**. Tim's team carries the one learner who completed their plan (counted 100%), which lifts the company line to 30% and leaves Indra's all-active team just below it — so the green/red comparison is meaningful, not cosmetic. (Numbers drift slightly as days pass; reseed near demo time.)

## Dashboard — three KPIs

1. **Completion vs company** — big number (Spectral-italic numeral) = team completion, with a green ▲ / red ▼ delta vs the company average. This is the competitive hook. Other teams' specifics are never shown — only the aggregated company rate.
2. **Engagement bar chart** (ApexCharts) — one bar per learner, height = check-in count, colored by plan status (active / completed / abandoned). At-a-glance "who's engaging."
3. **Commitments table** — sortable: Name · Commitment · Status · Check-ins · **Schedule 1:1**. The per-learner detail + action surface.

## Schedule 1:1

A Google **Calendar template** link (`calendar.google.com/calendar/render?action=TEMPLATE`): learner pre-added as guest, tomorrow at noon (local/floating time, no timezone guessing), 30 min, description seeded with their commitment text. No auth, opens in one click, Meet added inside the event. Present on every table row and in the email.

## Weekly email

`email.html` rendered at `/manager/<id>/email` — inline-styled HTML showing the completion-vs-company number, a compact learner table with a Schedule 1:1 button each, and a "View dashboard" button. Rendered (demoable), not sent — see scope cuts.

## Architecture

- **Flask + Jinja**, server-rendered. **ApexCharts** via CDN. Vanilla JS for table sorting. No build step.
- `metrics.py` — pure completion math (unit-tested in `test_metrics.py`, stdlib asserts, no new deps).
- `links.py` — calendar URL + synthesized learner emails (`first.last@northstar.example`), shared by dashboard + email.
- `app.py` — routes + `resolve_current_manager()`: reads `session` first, falls back to `?manager_id=` / default. The manager switcher writes to session, so it already behaves as a stand-in for login; a real login screen later is a localized drop-in.
- Data flow: request → resolve manager → compute → embed numbers as JSON in the template → JS renders. One request, no separate API.

## Styling

LeaderFactor tokens (see STYLING.md): cream `#FFFEF8` bg, ink `#101322`, **one accent = PS blue `#2A77EA`**, pill buttons, flat 16px cards no shadow, system-ui sans (Fustat fallback) + **Spectral italic** for the headline numerals/accent word, `0.18s ease`.

## Scope cuts (deliberate)

- **Email is rendered, not sent** — no SMTP/cron. The weekly cadence is described, not wired.
- **No auth** — manager switcher + session seam instead; login left for a later update.
- **No live data entry** — reads the seed; no check-in creation UI (the learner side is out of scope for a manager tool).
- **Learner emails synthesized**, not stored — avoids a schema change.

## Deploy

Render (Flask + gunicorn + Neon pooled `DATABASE_URL`). Start command `gunicorn app:app`.
