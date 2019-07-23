"""Koles config module."""
import configparser
from collections import UserDict

from koles.errors import OptionValidationError

DEFAULT_CONFIG = {
    'ignore-shorties': 0,
    'exit-code': False
}

OPTION_VALIDATION_MAP = {
    'ignore-shorties': None,
    'exit-code': False
}


class KolesConfig(UserDict):
    """Koles config class."""

    ALLOWED_CONFIG_FILENAMES = ('setup.cfg',)
    DEFAULT_CONFIG = DEFAULT_CONFIG

    def __init__(self, cli_args, run_dir: str) -> None:
        """Set path and config."""
        self.path = cli_args.path
        self._cli_args = {
            key: value for key, value in vars(cli_args).items()
            if key != 'path' and value is not None
        }
        self._run_dir = run_dir

        super().__init__(self._get_file_config())

    def _discover_config_file_path(self) -> str:
        """Discover config file and return its path."""
        #  config filename is hard-coded for now
        return None

    def _get_file_config(self) -> dict:
        """Set config."""
        path = self._discover_config_file_path()

        if not path:
            data = DEFAULT_CONFIG.copy()
            data.update(self._cli_args)
            return data

        config = configparser.ConfigParser()
        config.read(path)

        result_dict = {}

        try:
            options = config['koles'].items()
        except KeyError:
            return self.DEFAULT_CONFIG

        for key, value in options:
            try:
                self._validate_option(key, value)
                result_dict.update({key: int(value)})
            except OptionValidationError:
                pass

        return result_dict

    @staticmethod
    def _validate_option(key: str, value: str) -> bool:
        """Validate config option."""
        return key in DEFAULT_CONFIG
