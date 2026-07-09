"""Seed the leader_factor DB with fake but realistic demo data.

Structure: 1 admin -> 3 managers -> 5 learners each (15 total).
Each learner gets one action plan with a check-in history shaped to
illustrate the take-home's core problem: most learners disengage from
their plan quickly after training, and only a small minority keep
checking in over time.

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


# Engagement profiles: (status, source, days_since_created, check_in_day_offsets, scores)
PROFILE_A = ("completed", "curated", 35, [3, 10, 17, 24, 31], [3, 3, 4, 4, 5])
PROFILE_B = ("abandoned", "curated", 28, [2, 9], [3, 3])
PROFILE_C = ("abandoned", "ai_suggested", 21, [2], [2])
PROFILE_D = ("active", "ai_suggested", 14, [], [])
PROFILE_E = ("active", "ai_suggested", 20, [3, 11, 18], [3, 4, 4])

PROFILE_ORDER = [PROFILE_A] + [PROFILE_B] * 4 + [PROFILE_C] * 5 + [PROFILE_D] * 3 + [PROFILE_E] * 2


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

    learner_queue = []
    for manager_name in MANAGERS:
        manager = Manager(admin_id=admin.id, name=manager_name)
        session.add(manager)
        session.flush()
        for learner_name in LEARNERS_BY_MANAGER[manager_name]:
            learner = Learner(manager_id=manager.id, name=learner_name)
            session.add(learner)
            session.flush()
            learner_queue.append(learner)

    for learner, profile in zip(learner_queue, PROFILE_ORDER):
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

    print(f"Seeded 1 admin, {len(MANAGERS)} managers, {len(learner_queue)} learners, "
          f"{plan_idx} plans, {checkin_idx} check-ins.")


if __name__ == "__main__":
    seed()
