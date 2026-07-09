"""Unit tests for links.py (email synthesis + Google Calendar template URL).

The clock is injected (`today=`) so the tomorrow-noon math is deterministic.
Full "does it actually open a prefilled event" correctness is verified in a
browser; here we pin the pure string/date logic.
"""

from datetime import date
from urllib.parse import parse_qs, urlparse

from links import learner_email, schedule_1on1_url

FIXED = date(2026, 7, 9)  # a Thursday; tomorrow = 2026-07-10


def _params(url):
    return parse_qs(urlparse(url).query)


def test_learner_email_slug():
    assert learner_email("Steve Jobs") == "steve.jobs@northstar.example"
    assert learner_email("Ginni Rometty") == "ginni.rometty@northstar.example"


def test_schedule_url_host_and_action():
    url = schedule_1on1_url("Steve Jobs", "Do the thing", today=FIXED)
    assert url.startswith("https://calendar.google.com/calendar/render?")
    assert _params(url)["action"] == ["TEMPLATE"]


def test_schedule_url_prefills_guest():
    url = schedule_1on1_url("Steve Jobs", "Do the thing", today=FIXED)
    assert _params(url)["add"] == ["steve.jobs@northstar.example"]


def test_schedule_url_is_tomorrow_noon_floating_30min():
    url = schedule_1on1_url("Steve Jobs", "Do the thing", today=FIXED)
    # Floating local time (no trailing Z), noon start, 30-minute end.
    assert _params(url)["dates"] == ["20260710T120000/20260710T123000"]


def test_schedule_url_carries_name_and_commitment():
    url = schedule_1on1_url("Steve Jobs", "Ask one clarifying question", today=FIXED)
    q = _params(url)
    assert "Steve Jobs" in q["text"][0]
    assert "Ask one clarifying question" in q["details"][0]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"FAIL {t.__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    raise SystemExit(1 if failures else 0)
