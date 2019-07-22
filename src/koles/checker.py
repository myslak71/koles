"""Koles checker module."""
import os
import re
from typing import Set, Generator, List, Optional, Tuple

import pkg_resources
from koles.config import KolesConfig


class KolesChecker:
    """A koles checker class."""

    swear_list_file = 'data/swear_list/english.dat'

    def __init__(self, config: KolesConfig) -> None:
        """Initialize path and word matching pattern."""
        self._config = config
        self._pattern = '|'.join(self._get_bad_words())

    def _get_files_to_check(self) -> Generator:
        """
        Get files to check basing on the initialized path.

        Inaccessible files are omitted.
        """
        for root, _, filenames in os.walk(self._config.path):
            for file in filenames:
                full_file = os.path.join(root, file)
                if os.access(full_file, os.R_OK):
                    yield full_file

    def _get_bad_words(self) -> Set[str]:
        """Get a set of bad words."""
        data = pkg_resources.resource_string(__name__, self.swear_list_file)
        return set(data.decode().strip().split('\n'))

    def _check_row(self, string: str) -> List[Tuple[int, str]]:
        """Return a List containing a bad word and its position."""
        if self._pattern == '':
            return []

        regex = re.compile(f'(?=({self._pattern}))', flags=re.IGNORECASE)

        return [
            (match.start(), match.group(1))
            for match in regex.finditer(string)
        ]

    @staticmethod
    def _format_matches(matches):
        """Format matches and censor swears."""
        result = ''
        for index, swear in matches:
            result += f'{index}: {swear[0] + "*" * (len(swear) - 1)}, '
        return result[:-2]  # remove last comma and space

    def _check_file_content(self, path: str) -> List[str]:
        """Check the file and return formatted errors."""
        errors = []

        with open(path, encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                raw_matches = self._check_row(line)
                if raw_matches:
                    matches = self._format_matches(raw_matches)
                    errors.append(
                        f'{path}:{line_number}: '
                        f'Inappropriate vocabulary found: {matches}'
                    )

        return errors

    def _check_file(self, path: str) -> List[str]:
        """Check the file for inappropriate language and return errors."""
        errors = []
        filename = self._check_row(path)

        if filename:
            matches = self._format_matches(filename)
            errors.append(
                f'{path}: Filename contains bad language: {matches}'
            )

        try:
            file_errors = self._check_file_content(path)
            if file_errors:
                errors += file_errors
        except UnicodeDecodeError as e:
            errors.append(f'{path}: File couldn\'t have been opened: {e}')

        return errors

    def check(self) -> Optional[str]:
        """Check the given path and return formatted errors."""
        if not self._pattern:
            return ''

        errors: List[str] = []
        files_to_check = self._get_files_to_check()

        for file in files_to_check:
            result = self._check_file(file)
            errors += result

        return '\n'.join(errors)
