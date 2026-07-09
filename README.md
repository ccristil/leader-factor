# LeaderFactor — Manager Engagement Dashboard

A prototype that tackles the take-home's core problem — **fewer than 5% of learners
keep engaging with their action plan after training** — by building for the one lever
customer interviews flagged as highest-impact: **the learning manager**.

The bet: give managers (1) visibility into their team's engagement, framed
competitively against the company average, and (2) a one-click way to act that fits
their existing workflow. Visibility + light social pressure + a frictionless nudge →
more manager involvement → more learner engagement → (the real goal) behavior change
at re-assessment.

> Full product reasoning and locked decisions live in [SOLUTION.md](SOLUTION.md).
> The design tokens this UI is built on are in [STYLING.md](STYLING.md).

---

## What's in it

**1. A manager dashboard** (`/dashboard`) with three KPIs:
- **Team check-in completion vs. company average** — the headline number, green/red
  against the company aggregate. The competitive hook. A manager only ever sees their
  own team vs. the company — never another team's details.
- **Engagement-by-learner bar chart** (ApexCharts) — check-ins per learner, colored by
  plan status (active / completed / abandoned).
- **Commitments & progress table** — sortable, with a **Schedule 1:1** button on every row.

**2. A weekly Monday email** (`/manager/<id>/email`) — an inline-styled HTML email with
the headline number, a per-learner list of Schedule 1:1 buttons, and a link back to the
dashboard.

**3. Schedule 1:1** — every button opens a pre-filled Google Calendar event (learner added
as guest, tomorrow at noon, 30 min, their commitment in the notes). One click from
"my team is behind" to a booked conversation.

## The one metric everything hangs on

`completion = actual check-ins / expected check-ins`, where **expected = 2 per week**
since the plan started (the brief's twice-weekly cadence), capped at 100%. A **completed**
plan counts as 100% (fulfilled by definition), and that flows into the team/company
aggregate too. Team and company figures are aggregates (tenure-weighted, robust to a single
outlier). The math is the heart of the product, so it's pure and unit-tested
([metrics.py](metrics.py) / [test_metrics.py](test_metrics.py)).

## Run it locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# .env with the Neon POOLED connection string (the -pooler host):
#   DATABASE_URL=postgresql://...-pooler.../neondb?sslmode=require
#   SECRET_KEY=some-random-string          # optional locally

python seed.py            # wipes + reseeds: 1 admin, 3 managers, 15 learners, 24 check-ins
python app.py             # http://127.0.0.1:5001   (or: gunicorn app:app)
```

Run the tests:

```bash
python test_metrics.py && python test_links.py     # 15 assertions, no extra deps
```

## Architecture

Server-rendered Flask + Jinja, ApexCharts via CDN, a little vanilla JS for table sorting.
No build step, no frontend framework.

| File | Responsibility |
|------|----------------|
| [app.py](app.py) | Routes + `resolve_current_manager()` — the auth seam (see below) |
| [metrics.py](metrics.py) | Completion math (pure, tested) + DB roll-up into dashboard data |
| [links.py](links.py) | Google Calendar URL + synthesized learner emails (pure, tested) |
| [models.py](models.py) | SQLAlchemy schema (Neon pooled engine, `pool_pre_ping`, `pool_recycle`) |
| [seed.py](seed.py) | Deterministic fake data with deliberately uneven engagement |
| `templates/`, `static/` | LF-styled shell, dashboard, email; chart + sort JS |

**The login seam:** there's no auth yet, but `resolve_current_manager()` reads
`session` first and falls back to the query-param switcher. A real login later just sets
`session["manager_id"]` — nothing downstream changes.

## Deploy (Render)

The app connects to the same Neon database that's already seeded, so deploy is just:

1. New **Web Service** from this repo.
2. Build: `pip install -r requirements.txt` · Start: `gunicorn app:app` (also in the `Procfile`).
3. Env vars: `DATABASE_URL` (Neon **pooled** string) and `SECRET_KEY`.

`runtime.txt` pins Python 3.12.

## Scope cuts (deliberate — the 3-hour box)

- **Email is rendered, not sent.** No SMTP/cron. The weekly cadence is described and the
  email is fully demoable at its route — wiring a real mailer added no product insight.
- **No auth.** A manager switcher + session seam stands in, so the competitive angle is
  still demoable across teams. Login is scaffolded-for, not built.
- **No learner-side / data entry.** This is a manager tool; it reads the seeded history.
- **Learner emails are synthesized** (`first.last@northstar.example`) rather than stored —
  avoided a schema change and reseed for a cosmetic field.
- **Light mode only.** It's the LeaderFactor brand default; a dark theme was scope, not value.
