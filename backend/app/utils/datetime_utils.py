from datetime import datetime, date, timezone
from zoneinfo import ZoneInfo
from flask.json.provider import DefaultJSONProvider
from flask_restx import fields

PERU_TIMEZONE = ZoneInfo('America/Lima')


def to_peru_datetime(value: datetime) -> datetime:
    """Convert a UTC datetime or naive UTC timestamp to America/Lima timezone."""
    if value is None:
        return None

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    return value.astimezone(PERU_TIMEZONE)


def to_peru_isoformat(value: datetime) -> str:
    """Return an ISO 8601 string localized to America/Lima."""
    return to_peru_datetime(value).isoformat()


class PeruDateTime(fields.DateTime):
    """DateTime field that serializes datetimes in America/Lima timezone."""

    def format_iso8601(self, dt):
        return to_peru_isoformat(dt)

    def format_rfc822(self, dt):
        dt = to_peru_datetime(dt)
        return super().format_rfc822(dt)


class PeruJSONProvider(DefaultJSONProvider):
    """JSON provider that serializes datetime objects to America/Lima ISO 8601."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return to_peru_isoformat(obj)
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)
