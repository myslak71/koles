"""Utils module."""
import argparse
from typing import Any


def non_negative_int_validator(value: Any) -> int:
    """Check if the value can be converted to non-negative int."""
    error = argparse.ArgumentTypeError(f'{value} has to be an integer larger than 0.')

    try:
        number = int(value)
    except (TypeError, ValueError):
        raise error

    if number <= 1:
        raise error

    return number
