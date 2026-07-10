"""Check-in completion math for the manager dashboard.

The pure functions here are the heart of the product and are unit-tested in
test_metrics.py. `expected` is the number of check-ins a learner *should* have
by now, derived from the twice-weekly reminder cadence in the brief.

The DB-composition helpers at the bottom (`dashboard_data`, `list_managers`)
are thin glue over the pure functions; they're exercised end-to-end in the
browser rather than unit-tested, since they hit Neon.
"""

from datetime import date

from models import Manager

CADENCE_PER_WEEK = 2


def expected_check_ins(days_active):
    """Check-ins expected so far, at twice per week since the plan started.

    A float (we don't round until display). Days are floored at 1 so a plan
    created today can't produce a zero denominator downstream.
    """
    return CADENCE_PER_WEEK * max(days_active, 1) / 7


def completion_ratio(actual, expected):
    """Per-learner completion in [0, 1], capped so over-achievers read as 100%."""
    if expected <= 0:
        return 0.0
    return min(1.0, actual / expected)


def aggregate_completion(pairs):
    """Team/company completion in [0, 1] from (actual, expected) pairs.

    Aggregate (sum actual / sum expected), not a mean of per-learner ratios:
    it weights by tenure and is robust to a single outlier. Guards an empty
    team / all-zero expected against divide-by-zero.
    """
    total_expected = sum(expected for _, expected in pairs)
    if total_expected <= 0:
        return 0.0
    total_actual = sum(actual for actual, _ in pairs)
    return min(1.0, total_actual / total_expected)


# --- DB composition (not unit-tested; verified end-to-end) --------------------

def _current_plan(learner):
    """A learner's active commitment = their most recent plan (one, in the seed)."""
    if not learner.plans:
        return None
    return max(learner.plans, key=lambda p: p.date_created)


def learner_row(learner, today):
    """Flatten one learner into a primitive dict (detached-safe for templates)."""
    plan = _current_plan(learner)
    if plan is None:
        return None
    days_active = (today - plan.date_created).days
    expected = expected_check_ins(days_active)
    actual = sum(1 for c in learner.check_ins if c.plan_id == plan.id)
    # A completed plan is fulfilled by definition, so it counts as 100%. Check-in
    # cadence only judges learners still mid-plan (active/abandoned).
    completion = 1.0 if plan.status == "completed" else completion_ratio(actual, expected)
    return {
        "id": learner.id,
        "name": learner.name,
        "commitment": plan.text,
        "source": plan.source,
        "check_ins": actual,
        "days_active": days_active,
        "completion": completion,
        "_expected": expected,                # for the aggregate roll-up
        "_effective": completion * expected,  # completion re-expressed as check-ins, so the
                                              # team number pools consistently with the table
    }


def dashboard_data(session, manager_id, today=None):
    """Everything the dashboard/email need for one manager. Primitives only."""
    today = today or date.today()
    manager = session.get(Manager, manager_id)
    if manager is None:
        return None
    admin = manager.admin

    team = [r for r in (learner_row(l, today) for l in manager.learners) if r]
    team_completion = aggregate_completion([(r["_effective"], r["_expected"]) for r in team])

    company_pairs = [
        (r["_effective"], r["_expected"])
        for m in admin.managers
        for l in m.learners
        if (r := learner_row(l, today))
    ]
    company_completion = aggregate_completion(company_pairs)

    return {
        "manager_id": manager.id,
        "manager_name": manager.name,
        "company": admin.company,
        "team": team,
        "team_completion": team_completion,
        "company_completion": company_completion,
        "delta": team_completion - company_completion,
    }


def list_managers(session):
    """[{'id', 'name'}] for the switcher, ordered by name."""
    managers = session.query(Manager).order_by(Manager.name).all()
    return [{"id": m.id, "name": m.name} for m in managers]
