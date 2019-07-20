"""CLI module for koles."""
import argparse
import os
import sys

from koles.checker import KolesChecker


class readable_dir(argparse.Action):
    """An action class for path argument validation."""

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
    koles_checker = KolesChecker(path=path)
    return koles_checker.check()


def main():
    """Run koles as a script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('path', action=readable_dir)
    args = parser.parse_args()

    try:
        sys.exit(run_koles(args.path))
    except KeyboardInterrupt:
        pass
