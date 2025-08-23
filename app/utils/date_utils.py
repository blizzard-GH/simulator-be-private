from datetime import datetime, date, timedelta, timezone
from typing import Optional

# transform to 2025-12-31
def parse_date(raw_date: str) -> Optional[str]:
    """
    Convert different date string formats into 'YYYY-MM-DD'.
    Handles:
      - 2024-12-31
      - 2024-12-31T00:00:00+07:00
      - 2025-07-31T17:00:00.000Z
      - Wed, 13 Aug 2025 00:00:00 GMT
      - 2025-08-13 00:00:00
    """
    if not raw_date:
        return None

    local_tz = timezone(timedelta(hours=7))

    # ISO format with timezone or Z
    try:
        dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
        dt_local = dt.astimezone(local_tz)
        return dt_local.strftime("%Y-%m-%d")
    except ValueError:
        pass

    # RFC1123 format: "Wed, 13 Aug 2025 00:00:00 GMT"
    try:
        dt = datetime.strptime(raw_date, "%a, %d %b %Y %H:%M:%S GMT")
        dt_local = dt.replace(tzinfo=timezone.utc).astimezone(local_tz)
        return dt_local.strftime("%Y-%m-%d")
    except ValueError:
        pass

    # YYYY-MM-DD
    try:
        dt = datetime.strptime(raw_date, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass

    # YYYY-MM-DD HH:MM:SS
    try:
        dt = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass

    return None

from datetime import datetime, date

# transform to 2024-12-31T00:00:00+07:00
def parse_payload_date(payload_date: str) -> Optional[str]:
    """
    Parse a date string from payload into a timezone-aware ISO datetime string.
    Converts payload into Asia/Bangkok (GMT+7).
    
    Examples:
        - "2024-12-31" -> "2024-12-31T00:00:00+07:00"
        - "2025-07-31T17:00:00.000Z" -> "2025-08-01T00:00:00+07:00"
    """
    if not payload_date:
        return None

    local_tz = timezone(timedelta(hours=7))

    try:
        # Case: full ISO datetime with Z or offset
        dt = datetime.fromisoformat(payload_date.replace("Z", "+00:00"))
        local_dt = dt.astimezone(local_tz)
        return local_dt.isoformat()
    except ValueError:
        pass

    try:
        # Case: just a date string (YYYY-MM-DD)
        dt = datetime.strptime(payload_date, "%Y-%m-%d")
        # Localize at midnight GMT+7
        local_dt = dt.replace(tzinfo=local_tz)
        return local_dt.isoformat()
    except ValueError:
        pass

    try:
        # Case: RFC1123 format
        dt = datetime.strptime(payload_date, "%a, %d %b %Y %H:%M:%S GMT")
        local_dt = dt.replace(tzinfo=timezone.utc).astimezone(local_tz)
        return local_dt.isoformat()
    except ValueError:
        pass

    raise ValueError(f"Invalid date format: {payload_date}")