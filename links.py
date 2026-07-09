"""Shared link/identity helpers for the dashboard and the weekly email.

`schedule_1on1_url` builds a Google Calendar *template* URL: one click opens a
pre-filled event with the learner added as a guest, tomorrow at noon, 30 min.
We use floating local time (no trailing 'Z') so "noon" is noon in whoever's
timezone opens it — no server-side timezone guessing. A real Google Meet link
has no plain-URL equivalent; the manager clicks "Add Google Meet" in the event.
"""

import re
from datetime import date, datetime, time, timedelta
from urllib.parse import urlencode

EMAIL_DOMAIN = "northstar.example"
CAL_ENDPOINT = "https://calendar.google.com/calendar/render"
MEETING_MINUTES = 30


def learner_email(name):
    """Synthesize a stable address from a name: 'Steve Jobs' -> steve.jobs@..."""
    parts = [re.sub(r"[^a-z0-9]", "", p.lower()) for p in name.split()]
    slug = ".".join(p for p in parts if p)
    return f"{slug}@{EMAIL_DOMAIN}"


def _tomorrow_noon(today):
    return datetime.combine((today or date.today()) + timedelta(days=1), time(12, 0))


def schedule_1on1_url(learner_name, commitment, today=None):
    """Google Calendar template link for a 1:1, tomorrow noon local time."""
    start = _tomorrow_noon(today)
    end = start + timedelta(minutes=MEETING_MINUTES)
    fmt = "%Y%m%dT%H%M%S"  # no 'Z' => floating/local time in the viewer's tz
    params = {
        "action": "TEMPLATE",
        "text": f"1:1 with {learner_name} — action plan check-in",
        "add": learner_email(learner_name),
        "dates": f"{start.strftime(fmt)}/{end.strftime(fmt)}",
        "details": (
            "Quick check-in on your leadership action plan:\n\n"
            f"“{commitment}”\n\n"
            "How's it going? What's getting in the way?"
        ),
    }
    return f"{CAL_ENDPOINT}?{urlencode(params)}"
