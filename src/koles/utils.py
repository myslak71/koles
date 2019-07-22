"""Utils module."""
from typing import Any


def validate_non_negative_int(value: Any) -> bool:
    """Check if the value can be converted to non-negative int."""
    try:
        number = int(value)
    except TypeError:
        return False

    return number >= 1
