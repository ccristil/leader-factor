# LeaderFactor — Product Engineer Take-Home

## What this is

Take-home build exercise for the Product Engineer role at LeaderFactor. Deliver in less thana week.

## Time box

Max 3 hours of build time. Scope discipline is explicitly part of the grade — cutting visibly and explaining the cut in the README matters more than feature count.

## The problem (as given)

LeaderFactor is a behavior-change company, not just a training company. Flow: assessment → training → commitment ("action plan") → practice period → re-assessment.

**Problem:** fewer than 5% of learners keep engaging with their action plan after training ends.

Context from the brief:

- Buyers are L&D admins who purchase the training and care about outcomes + admin-visible metrics (sellability matters).
- Managers often don't know the specifics of what a learner committed to, but do care whether the skill improves. Customer interviews found manager involvement is a major lever for better outcomes.
- Learners pick commitments either from curated behavioral guides or from AI suggestions tied to their assessment results.
- Learners already get twice-weekly reminder emails — that alone isn't moving the number.
- Real success = behavior change, measured via re-assessment. Engagement is a leading indicator and the mechanism through which change happens, not the definition of success itself.

## Deliverables

- Working deployed prototype (deploy link)
- Repo link

## Stack decisions (locked in)

- Backend: Python / Flask
- DB: Neon (serverless Postgres)
- Hosting: TBD

## Known technical gotchas to handle

- Use Neon's **pooled** connection string (`-pooler` in the hostname) in SQLAlchemy, with `pool_pre_ping=True` and a `pool_recycle` value set — avoids random dropped-connection errors serverless Postgres can throw.
- Seed realistic fake data (a few weeks of history, varied engagement patterns) rather than relying on live data entry during a demo — one empty account won't show anything interesting. Went with a single company/admin for this demo rather than multiple — simpler seed story, buyer-facing dashboard doesn't need cross-company data to be convincing.

## Current state

- Neon project: `leader_factor` (id `solitary-king-59049854`), pooled connection string in `.env` as `DATABASE_URL` (gitignored).
- Schema (5 tables, see [models.py](models.py) for SQLAlchemy source of truth): `admin` → `manager` (many) → `learner` (many) → `plan` (many) → `check_in` (many). One learner has exactly one manager; one manager has exactly one admin.
  - `plan.status`: `active` / `completed` / `abandoned`.
  - `plan.source`: `curated` / `ai_suggested` — tracks which of the two commitment pathways from the brief the learner used.
- Seed data ([seed.py](seed.py), re-running wipes and reseeds all 5 tables): 1 admin, 3 managers, 15 learners (5 each), named after famous executives. Check-in histories are deliberately uneven across learners — one sustained-engagement outlier, several who checked in once or twice then went quiet, a few with zero check-ins — to make the engagement drop-off problem visible in any dashboard/metric built on top, rather than seeding uniform data that hides it.
- No Flask app/routes yet — schema and seed data only so far.

## Not decided yet

The actual solution/feature design is intentionally left out of this file. That part is mine to work out — this file is just the shared factual context and technical setup so Claude Code has the brief straight without re-explaining it every session.
