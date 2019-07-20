"""Koles checker module."""
import os
import re
from typing import Set, Generator, List, Tuple

import pkg_resources


class KolesChecker:
    """A koles checker class."""

    def __init__(self, path: str) -> None:
        """
        Initialize path and word matching pattern.

        :param path: path to check
        """
        self._path = path
        self._pattern = '|'.join(self._get_bad_words())

    def _get_files_to_check(self) -> Generator:
        """Get files to check basing on initialized path."""
        for root, dirs, filenames in os.walk(self._path):
            for file in filenames:
                yield os.path.join(root, file)

    def _get_bad_words(self) -> Set[str]:
        """Get a set of bad words."""
        data = pkg_resources.resource_string(__name__, 'data/english.dat')
        return set(data.decode().strip().split('\n'))

    def _check_line(self, line: str) -> List[int]:
        """Return a list of bad words starting positions."""
        nasty_positions = [
            m.start() for m in re.finditer(f'(?=({self._pattern}))', line)
        ]
        return nasty_positions

    def _check_file(self, path: str) -> List[Tuple[int, List[int]]]:
        """Check the file for inappropriate language and return existing errors."""
        errors = []

        with open(path, encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                error_positions = self._check_line(line)
                if error_positions:
                    errors.append((line_number, error_positions))

        return errors

    def check(self):
        """Check the given path and return formatted errors."""
        errors = []
        files_to_check = self._get_files_to_check()
        for file in files_to_check:
            result = self._check_file(file)
            errors += [
                f'{file}:{line_number}: Inappropriate vocabulary found at positions: {positions}'
                for line_number, positions in result
            ]
        return '\n'.join(errors)
