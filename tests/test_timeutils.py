from datetime import date, datetime, time, timezone
from types import SimpleNamespace

from utils.timeutils import (
    clinic_datetime, clinic_now, clinic_today, is_future, is_slot_in_future, utcnow, utcnow_naive,
)

# 2026-11-15 19:00 UTC == 2026-11-16 00:30 IST (UTC+5:30): clinic is already "tomorrow".
NOW_UTC = datetime(2026, 11, 15, 19, 0, tzinfo=timezone.utc)


def test_utcnow_is_aware_and_naive_variant_matches():
    aware, naive = utcnow(), utcnow_naive()
    assert aware.tzinfo is not None
    assert naive.tzinfo is None
    assert abs((aware.replace(tzinfo=None) - naive).total_seconds()) < 1


def test_clinic_now_converts_to_clinic_zone(app):
    now = clinic_now(NOW_UTC)
    assert (now.date(), now.hour, now.minute) == (date(2026, 11, 16), 0, 30)
    assert now.utcoffset().total_seconds() == 5.5 * 3600


def test_clinic_today_crosses_midnight_before_utc(app):
    assert NOW_UTC.date() == date(2026, 11, 15)
    assert clinic_today(NOW_UTC) == date(2026, 11, 16)


def test_is_future_around_clinic_midnight(app):
    assert not is_future(date(2026, 11, 16), time(0, 15), NOW_UTC)   # 15 min ago (clinic time)
    assert not is_future(date(2026, 11, 16), time(0, 30), NOW_UTC)   # exactly now -> not strictly future
    assert is_future(date(2026, 11, 16), time(0, 45), NOW_UTC)
    assert not is_future(date(2026, 11, 15), time(23, 59), NOW_UTC)  # "yesterday" in clinic time
    # A naive UTC comparison would wrongly call this future (19:00 UTC < 20:00):
    assert not is_future(date(2026, 11, 15), time(20, 0), NOW_UTC)


def test_is_slot_in_future_uses_slot_fields(app):
    slot = SimpleNamespace(date=date(2026, 11, 16), start_time=time(9, 0))
    assert is_slot_in_future(slot, NOW_UTC)


def test_clinic_timezone_is_configurable(app):
    app.config["CLINIC_TIMEZONE"] = "UTC"
    assert clinic_today(NOW_UTC) == date(2026, 11, 15)
    assert is_future(date(2026, 11, 15), time(20, 0), NOW_UTC)
    assert clinic_datetime(date(2026, 1, 1), time(9, 0)).utcoffset().total_seconds() == 0
