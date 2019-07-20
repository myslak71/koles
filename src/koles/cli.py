"""CLI module for koles"""
import argparse
import os
import sys

from koles.checker import KolesChecker


class readable_dir(argparse.Action):
    """TODO"""

    def __call__(self, parser, namespace, values, option_string=None):
        """TODO"""
        if not os.path.isdir(values):
            raise argparse.ArgumentTypeError(f'Argument path: {values[0]} is not a valid path')

        # check if access to the file is granted
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError(f'Argument path: {values[0]} is not a readable path')


def run_koles(path: str):
    """TODO"""
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
