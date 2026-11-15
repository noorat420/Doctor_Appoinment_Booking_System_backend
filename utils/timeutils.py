"""Time helpers.

Rules (see CLAUDE.md §6):
- Slot date + start_time are clinic-local wall time in CLINIC_TIMEZONE.
- Audit timestamps are UTC.
- Never use datetime.utcnow() (deprecated, returns naive values).
"""
from datetime import date, datetime, time, timezone
from zoneinfo import ZoneInfo

from flask import current_app


def utcnow() -> datetime:
    """Timezone-aware current UTC time."""
    return datetime.now(timezone.utc)


def utcnow_naive() -> datetime:
    """Current UTC time without tzinfo, for the existing naive DateTime columns.
    Switch model defaults to utcnow() once columns are migrated to TIMESTAMPTZ (task 2.x)."""
    return utcnow().replace(tzinfo=None)


def clinic_tz() -> ZoneInfo:
    return ZoneInfo(current_app.config["CLINIC_TIMEZONE"])


def clinic_now(now: datetime | None = None) -> datetime:
    """Current time in the clinic timezone. `now` (aware) can be injected for tests."""
    return (now or utcnow()).astimezone(clinic_tz())


def clinic_today(now: datetime | None = None) -> date:
    return clinic_now(now).date()


def clinic_datetime(slot_date: date, slot_time: time) -> datetime:
    """Combine a clinic-local date and time into an aware datetime."""
    return datetime.combine(slot_date, slot_time, tzinfo=clinic_tz())


def slot_start_dt(slot) -> datetime:
    return clinic_datetime(slot.date, slot.start_time)


def is_future(slot_date: date, slot_time: time, now: datetime | None = None) -> bool:
    """True iff the clinic-local moment is strictly after now."""
    return clinic_datetime(slot_date, slot_time) > clinic_now(now)


def is_slot_in_future(slot, now: datetime | None = None) -> bool:
    return is_future(slot.date, slot.start_time, now)
