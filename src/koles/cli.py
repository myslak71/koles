"""CLI module for koles."""
import argparse
import os
import sys
from enum import Enum

from koles.checker import KolesChecker


class ReturnCode(Enum):
    """Class containing error codes."""

    no_errors = 0
    errors_found = 1


class accessible_dir(argparse.Action):
    """An action class for the path argument validation."""

    def __call__(self, parser, namespace, value, option_string=None):
        """Raise an error if given path is not valid or cannot be accessed."""
        if not os.path.isdir(value) and not os.path.isfile(value):
            raise argparse.ArgumentTypeError(f'Argument path: {value} is not a valid path')

        # check if access to the file is granted
        if os.access(value, os.R_OK):
            setattr(namespace, self.dest, value)
        else:
            raise argparse.ArgumentTypeError(f'Argument path: {value} is not a readable path')


def run_koles(path: str):
    """Run check on the given path."""
    # leaving this part without error handling just for development stage
    koles_checker = KolesChecker(path=path)
    sys.stdout.write(koles_checker.check())  # type: ignore
    return ReturnCode.no_errors.value


def main():
    """Run koles as a script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('path', action=accessible_dir)
    args = parser.parse_args()

    try:
        sys.exit(run_koles(args.path))
    except KeyboardInterrupt:
        pass
