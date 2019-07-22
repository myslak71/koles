"""Errors module."""
from dataclasses import dataclass


@dataclass
class OptionValidationError(Exception):
    """Raise if the option cannot be validated."""

    error_code: str
    detail: str

    def __str__(self):
        """Return error message."""
        return f'{self.error_code}: {self.detail}'
