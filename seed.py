"""Seed the leader_factor DB with fake but realistic demo data.

Structure: 1 admin -> 3 managers -> 5 learners each (15 total).
Each learner gets one action plan with a check-in history. The three teams are
deliberately shaped as distinct archetypes so the dashboard's manager-switcher
tells a story and the "vs company average" delta means something in every
direction:
    Tim Cook        — STRONG team, most learners sustaining check-ins (~87%)
    Sheryl Sandberg — STRUGGLING team, the disengagement problem in full (~14%)
    Indra Nooyi     — MIXED team, thriving + middling + stalled together (~59%)
Company average lands ~57%. Within a team, completion still varies learner to
learner so the color-coded, worst-first table has real disparity to triage.

Re-running this script wipes and reseeds all five tables.
"""

from datetime import date, timedelta

from dotenv import load_dotenv

from models import Admin, Base, CheckIn, Learner, Manager, Plan, get_engine, get_session

load_dotenv()

TODAY = date.today()

ADMIN = {"name": "Satya Nadella", "company": "Northstar Leadership Group"}

MANAGERS = ["Tim Cook", "Sheryl Sandberg", "Indra Nooyi"]

LEARNERS_BY_MANAGER = {
    "Tim Cook": ["Steve Jobs", "Jony Ive", "Angela Ahrendts", "Eddy Cue", "Lisa Jackson"],
    "Sheryl Sandberg": ["Mark Zuckerberg", "Marissa Mayer", "Susan Wojcicki", "Sundar Pichai", "Ginni Rometty"],
    "Indra Nooyi": ["Warren Buffett", "Jamie Dimon", "Mary Barra", "Bob Iger", "Jack Welch"],
}

PLAN_TEXTS = [
    "Ask one clarifying question before responding in every 1:1 this week",
    "Delegate one recurring decision to a direct report",
    "Give specific, timely feedback within 24 hours of an event",
    "Hold a weekly retro with the team to surface blockers",
    "Practice active listening by summarizing before replying in meetings",
    "Set aside 15 minutes weekly for direct reports to raise concerns",
    "Publicly recognize a team member's contribution each week",
    "Block 30 minutes daily for focused strategic thinking",
    "Ask for feedback on my leadership style from two peers",
    "Run a pre-mortem before the next major decision",
    "Reduce meeting load by cancelling one recurring meeting",
    "Check in 1:1 with each direct report about career goals",
    "Practice saying no to non-critical requests this month",
    "Share the context/rationale behind decisions with the team",
    "Set clear, measurable goals with each direct report",
]

COMMENTS = [
    "Still getting used to this, but noticing small wins.",
    "Team responded well when I tried this in our stand-up.",
    "Harder than expected -- reverted to old habits a couple times this week.",
    "Feeling more confident applying this consistently now.",
    "A direct report mentioned they appreciated the change.",
    "Skipped a few days but picked it back up.",
    "This is becoming more natural each week.",
    "Struggled to find the time, but got one rep in.",
]


def comment(i):
    return COMMENTS[i % len(COMMENTS)]


# Each learner's plan + check-in history, keyed by manager so the three team
# archetypes are legible at a glance:
#   Tim Cook        — STRONG:      nearly everyone sustaining check-ins   (~87% team)
#   Sheryl Sandberg — STRUGGLING:  the disengagement problem in full       (~14% team)
#   Indra Nooyi     — MIXED:       two thriving, one middling, two stalled (~59% team)
#
# Profile = (status, source, days_active, check_in_day_offsets, scores).
# Per-learner completion ≈ len(offsets) / (2 * days_active / 7), capped at 1.0;
# a "completed" plan always counts as 100%. Offsets are spread across the active
# window and scores jitter 2–5 so histories read as organic, not uniform.
PROFILES_BY_MANAGER = {
    "Tim Cook": [  # STRONG team
        ("completed",  "curated",      42, [2, 5, 9, 12, 16, 19, 23, 27, 31, 35, 39], [3, 4, 4, 4, 5, 4, 5, 5, 4, 5, 5]),
        ("active",     "curated",      28, [2, 6, 9, 13, 17, 21, 25],                 [3, 4, 4, 5, 4, 5, 5]),
        ("active",     "ai_suggested", 24, [2, 6, 10, 14, 18, 22],                    [4, 4, 5, 4, 5, 5]),
        ("active",     "curated",      21, [3, 7, 11, 15, 19],                        [3, 4, 4, 5, 4]),
        ("active",     "ai_suggested", 30, [3, 8, 13, 18, 23, 28],                    [3, 3, 4, 4, 5, 4]),
    ],
    "Sheryl Sandberg": [  # STRUGGLING team
        ("active",     "ai_suggested", 16, [],        []),
        ("abandoned",  "curated",      24, [2],       [3]),
        ("active",     "curated",      20, [4],       [2]),
        ("abandoned",  "ai_suggested", 30, [2, 8],    [3, 2]),
        ("active",     "ai_suggested", 12, [],        []),
    ],
    "Indra Nooyi": [  # MIXED team (the default dashboard view)
        ("completed",  "curated",      38, [2, 6, 9, 13, 17, 20, 24, 28, 31, 35], [3, 4, 3, 4, 5, 4, 5, 4, 5, 5]),
        ("active",     "ai_suggested", 26, [2, 6, 10, 14, 19, 23],               [2, 3, 4, 4, 4, 5]),
        ("active",     "curated",      20, [3, 9, 15],                           [3, 4, 3]),
        ("abandoned",  "ai_suggested", 22, [3],                                  [2]),
        ("active",     "curated",      18, [],                                    []),
    ],
}


def seed():
    engine = get_engine()
    Base.metadata.create_all(engine)  # no-op: tables already exist in Neon

    session = get_session()
    session.bind = engine

    session.execute(
        __import__("sqlalchemy").text(
            "TRUNCATE check_in, plan, learner, manager, admin RESTART IDENTITY CASCADE"
        )
    )

    admin = Admin(**ADMIN)
    session.add(admin)
    session.flush()

    plan_idx = 0
    checkin_idx = 0
    learner_count = 0

    for manager_name in MANAGERS:
        manager = Manager(admin_id=admin.id, name=manager_name)
        session.add(manager)
        session.flush()

        learners = LEARNERS_BY_MANAGER[manager_name]
        profiles = PROFILES_BY_MANAGER[manager_name]
        for learner_name, profile in zip(learners, profiles):
            learner = Learner(manager_id=manager.id, name=learner_name)
            session.add(learner)
            session.flush()
            learner_count += 1

            status, source, days_ago, offsets, scores = profile
            plan_text = PLAN_TEXTS[plan_idx % len(PLAN_TEXTS)]
            plan_idx += 1

            created = TODAY - timedelta(days=days_ago)
            plan = Plan(
                learner_id=learner.id,
                text=plan_text,
                date_created=created,
                status=status,
                source=source,
            )
            session.add(plan)
            session.flush()

            for offset, score in zip(offsets, scores):
                session.add(
                    CheckIn(
                        learner_id=learner.id,
                        plan_id=plan.id,
                        date=created + timedelta(days=offset),
                        score=score,
                        comment=comment(checkin_idx),
                    )
                )
                checkin_idx += 1

    session.commit()
    session.close()

    print(f"Seeded 1 admin, {len(MANAGERS)} managers, {learner_count} learners, "
          f"{plan_idx} plans, {checkin_idx} check-ins.")


if __name__ == "__main__":
    seed()
