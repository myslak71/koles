"""CLI module for koles."""
import argparse
import os
import sys
from enum import IntEnum

from koles.checker import KolesChecker
from koles.config import KolesConfig
from koles.utils import non_negative_int_validator


class ReturnCode(IntEnum):
    """Class containing error codes."""

    no_errors = 0
    errors_found = 1


class AccessibleDir(argparse.Action):
    """An action class for the path argument validation."""

    def __call__(self, parser, namespace, value, option_string=None) -> None:
        """Raise an error if given path is not valid or cannot be accessed."""
        if not os.path.isdir(value) and not os.path.isfile(value):
            raise argparse.ArgumentTypeError(
                f'Argument path: {value} is not a valid path'
            )

        # check if access to the file is granted
        if os.access(value, os.R_OK):
            setattr(namespace, self.dest, value)
        else:
            raise argparse.ArgumentTypeError(
                f'Argument path: {value} is not a readable path'
            )


def run_koles(cli_args: str, run_dir: str) -> int:
    """Run check for the given path."""
    # leaving this part without error handling just for development stage
    config = KolesConfig(cli_args=cli_args, run_dir=run_dir)
    koles_checker = KolesChecker(config)
    sys.stdout.write(koles_checker.check())  # type: ignore
    return ReturnCode.no_errors.value


def main() -> None:
    """Run koles as a script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('path', action=AccessibleDir)
    parser.add_argument("--ignore-shorties", type=non_negative_int_validator)
    parser.add_argument("--exit-code", action='store_true')
    args = parser.parse_args()

    run_dir = os.getcwd()
    sys.stdout.write(f'Running Koles from: {run_dir}')

    try:
        sys.exit(run_koles(args, run_dir=run_dir))
    except KeyboardInterrupt:
        pass
