"""TODO"""
import os
import re

import pkg_resources


class KolesChecker:
    """A koles checker class."""

    def __init__(self, path: str):
        """TODO"""
        self._path = path
        self._bad_words = self._get_bad_words()
        self.pattern = '|'.join(self._bad_words)

    def _get_files_to_check(self):
        """TODO"""
        if os.path.isdir(self._path):
            for root, dirs, filenames in os.walk(self._path):
                for file in filenames:
                    yield os.path.join(root, file)

    def _get_bad_words(self):
        """TODO"""
        data = pkg_resources.resource_string(__name__, 'data/english.dat')
        return set(data.decode().strip().split('\n'))

    def _check_line(self, line: str):
        """TODO"""
        nasty_positions = [
            m.start() for m in re.finditer(f'(?=({self.pattern}))', line)
        ]
        return nasty_positions

    def _check_file(self, path):
        """TODO"""
        errors = []

        with open(path, encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                error_positions = self._check_line(line)
                if error_positions:
                    errors.append((line_number, error_positions))

        return errors

    def check(self):
        """TODO"""
        errors = []
        files_to_check = self._get_files_to_check()
        for file in files_to_check:
            result = self._check_file(file)
            errors += [
                f'{file}:{line_number}: Inappropriate vocabulary found at positions: {positions}'
                for line_number, positions in result
            ]
        return '\n'.join(errors)
