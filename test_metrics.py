"""Unit tests for the completion math in metrics.py.

Pure functions, deterministic (no DB, no clock). Runnable two ways:
    python test_metrics.py     # zero dependencies, prints a summary
    pytest test_metrics.py     # if pytest happens to be installed
"""

from metrics import aggregate_completion, completion_ratio, expected_check_ins

TOL = 1e-9


def approx(a, b):
    return abs(a - b) < TOL


# --- expected_check_ins: twice-weekly cadence ---------------------------------

def test_expected_is_two_per_week():
    assert approx(expected_check_ins(7), 2.0)
    assert approx(expected_check_ins(14), 4.0)
    assert approx(expected_check_ins(35), 10.0)


def test_expected_floors_days_to_avoid_zero():
    # A plan created today must not yield a zero denominator downstream.
    assert expected_check_ins(0) > 0
    assert approx(expected_check_ins(0), expected_check_ins(1))


# --- completion_ratio: per-learner, capped at 100% ----------------------------

def test_completion_ratio_basic():
    assert approx(completion_ratio(5, 10.0), 0.5)


def test_completion_ratio_caps_at_one():
    assert approx(completion_ratio(10, 10.0), 1.0)
    assert approx(completion_ratio(12, 10.0), 1.0)  # over-achiever capped


def test_completion_ratio_guards_zero_expected():
    assert approx(completion_ratio(0, 0.0), 0.0)  # no ZeroDivisionError


# --- aggregate_completion: team / company roll-up -----------------------------

def test_aggregate_sums_then_divides():
    # Tim Cook's team in the seed: one PROFILE_A + four PROFILE_B.
    pairs = [(5, 10.0)] + [(2, 8.0)] * 4  # Sum actual=13, Sum expected=42
    assert approx(aggregate_completion(pairs), 13 / 42)


def test_aggregate_caps_at_one():
    assert approx(aggregate_completion([(20, 10.0)]), 1.0)


def test_aggregate_empty_is_zero():
    assert approx(aggregate_completion([]), 0.0)


def test_aggregate_all_zero_expected_is_zero():
    assert approx(aggregate_completion([(0, 0.0), (0, 0.0)]), 0.0)


def test_company_aggregate_matches_seed():
    # The full seed: A + 4B + 5C + 3D + 2E.
    pairs = (
        [(5, expected_check_ins(35))]
        + [(2, expected_check_ins(28))] * 4
        + [(1, expected_check_ins(21))] * 5
        + [(0, expected_check_ins(14))] * 3
        + [(3, expected_check_ins(20))] * 2
    )
    # Sum actual = 24, Sum expected = 95.428..., company completion ~= 0.2515.
    assert approx(aggregate_completion(pairs), 24 / (95 + 3 / 7))


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
        except Exception as e:  # noqa: BLE001 - surface import/other errors clearly
            failures += 1
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    raise SystemExit(1 if failures else 0)
