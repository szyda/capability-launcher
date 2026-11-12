from datetime import datetime

try:
    import zoneinfo
except ImportError:  # pragma: no cover
    from backports import zoneinfo


def run(inputs: dict) -> dict:
    timestamp = inputs.get('timestamp', '')
    from_tz_name = inputs.get('from_tz', 'UTC')
    to_tz_name = inputs.get('to_tz', 'UTC')

    naive = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    from_tz = zoneinfo.ZoneInfo(from_tz_name)
    to_tz = zoneinfo.ZoneInfo(to_tz_name)

    aware = naive.astimezone(from_tz)
    converted = aware.astimezone(to_tz)

    return {
        'utc_time': aware.astimezone(zoneinfo.ZoneInfo('UTC')).isoformat(),
        'converted_time': converted.isoformat(),
        'from_tz': from_tz_name,
        'to_tz': to_tz_name,
    }
