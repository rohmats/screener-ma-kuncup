"""Timezone helpers for consistent timestamp handling."""

from datetime import datetime
from zoneinfo import ZoneInfo


JAKARTA_TZ = ZoneInfo("Asia/Jakarta")


def now_jakarta() -> datetime:
    """Return timezone-aware current datetime in Asia/Jakarta (GMT+7)."""
    return datetime.now(JAKARTA_TZ)
