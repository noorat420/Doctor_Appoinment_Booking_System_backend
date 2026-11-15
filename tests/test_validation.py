from datetime import date, time

import pytest

from utils.validation import (
    ValidationError, get_json_body, parse_date, parse_int, parse_time, require,
)


def test_require_reports_each_missing_field():
    with pytest.raises(ValidationError) as exc:
        require({"a": "x", "b": "  ", "c": None}, "a", "b", "c", "d")
    assert set(exc.value.fields) == {"b", "c", "d"}


@pytest.mark.parametrize("value", ["2026-11-16", " 2026-11-16 "])
def test_parse_date_ok(value):
    assert parse_date(value) == date(2026, 11, 16)


@pytest.mark.parametrize("value", ["16-11-2026", "2026-02-30", "2026/11/16", "", None, 20261116])
def test_parse_date_rejects(value):
    with pytest.raises(ValidationError) as exc:
        parse_date(value, "start_date")
    assert "start_date" in exc.value.fields


def test_parse_time_ok():
    assert parse_time("09:30") == time(9, 30)
    assert parse_time("23:59") == time(23, 59)


@pytest.mark.parametrize("value", ["24:00", "9.30", "09:30:00", "9am", None])
def test_parse_time_rejects(value):
    with pytest.raises(ValidationError):
        parse_time(value, "start_time")


def test_parse_int():
    assert parse_int(5, "n") == 5
    assert parse_int("42", "n") == 42
    for bad in (True, 1.5, "abc", None):
        with pytest.raises(ValidationError):
            parse_int(bad, "n")
    with pytest.raises(ValidationError, match="Invalid number"):
        parse_int(0, "slot_id", min_value=1)
    with pytest.raises(ValidationError):
        parse_int(121, "interval", max_value=120)


@pytest.mark.parametrize("kwargs", [{"data": "not json", "content_type": "text/plain"},
                                    {"json": [1, 2]}, {}])
def test_get_json_body_rejects_non_objects(app, kwargs):
    with app.test_request_context("/", method="POST", **kwargs):
        with pytest.raises(ValidationError):
            get_json_body()


def test_handler_returns_400_json(app, client):
    @app.route("/_test/validate", methods=["POST"])
    def _validate():
        data = get_json_body()
        require(data, "name")
        return {"ok": True}

    res = client.post("/_test/validate", json={})
    assert res.status_code == 400
    assert res.get_json() == {"error": "Missing required fields",
                              "fields": {"name": "This field is required"}}

    res = client.post("/_test/validate", data="x", content_type="text/plain")
    assert res.status_code == 400
    assert res.get_json() == {"error": "Request body must be a JSON object"}
