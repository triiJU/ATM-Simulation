import re
from datetime import datetime

from .exceptions import DoesNotExist


PATTERN1 = re.compile(r"(\d{1,2})[\s\/\\]+(\d{1,2})[\s\/\\]+(\d{4})")
PATTERN2 = re.compile(
    r"(\d{1,2})(?:st|nd|rd|th)\s*(Jan(?:uary)?|Feb(?:uary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember?)|Dec(?:ember)?)\s*(\d{4})",
    re.IGNORECASE,
)

MONTHS = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
]


def convert_to_datetime(val: str):
    if valid := PATTERN1.search(val):
        valid_groups = valid.groups()
        return datetime.strptime(
            f"{valid_groups[0]}/{valid_groups[1]}/{valid_groups[2]}", "%d/%m/%Y"
        )
    elif valid := PATTERN2.search(val):
        valid_groups = valid.groups()
        month = valid_groups[1].lower()
        return datetime.strptime(
            f"{valid_groups[0]}/{MONTHS.index(month[:3]) + 1}/{valid_groups[2]}",
            "%d/%m/%Y",
        )
    else:
        raise DoesNotExist(val, message="Invalid datetime string provided: {0}")
