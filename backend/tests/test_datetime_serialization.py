from datetime import datetime, date
from app import create_app
from app.utils.datetime_utils import PeruDateTime


def test_peru_datetime_helper_formats_utc_as_lima():
    dt = datetime(2024, 1, 1, 12, 0, 0)
    formatted = PeruDateTime().format(dt)

    assert formatted.endswith('-05:00')
    assert '2024-01-01T07:00:00' in formatted


def test_app_json_provider_serializes_datetimes_to_lima_timezone():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    payload = {'timestamp': datetime(2024, 1, 1, 12, 0, 0), 'today': date(2024, 1, 1)}
    json_text = app.json.dumps(payload)

    assert '2024-01-01T07:00:00-05:00' in json_text
    assert '2024-01-01' in json_text
