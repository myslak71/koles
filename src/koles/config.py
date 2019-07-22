"""Koles config module."""
import configparser
from collections import UserDict

from koles.errors import OptionValidationError

DEFAULT_CONFIG = {
    "ignore-shorties": None,
}

OPTION_VALIDATION_MAP = {
    "ignore-shorties": None,
}


class KolesConfig(UserDict):
    """Koles config class."""

    ALLOW_CONFIG_FILENAMES = ('setup.cfg',)
    DEFAULT_CONFIG = DEFAULT_CONFIG

    def __init__(self, path, run_dir: str) -> None:
        """Set path and config."""
        self.path = path
        self._run_dir = run_dir
        super().__init__(self._get_file_config())

    def _discover_config_file_path(self) -> str:
        """Discover config file and return its path."""
        #  config filename is hard-coded for now
        return f'{self._run_dir}/{self.ALLOW_CONFIG_FILENAMES[0]}'

    def _get_file_config(self) -> dict:
        """Set config."""
        path = self._discover_config_file_path()
        config = configparser.ConfigParser()
        config.read(path)

        result_dict = {}

        try:
            options = config['koles'].items()
        except KeyError:
            return result_dict

        for key, value in options:
            try:
                self._validate_option(key, value)
                result_dict.update({key: value})
            except OptionValidationError:
                pass

        return result_dict

    @staticmethod
    def _validate_option(key: str, value: str) -> bool:
        """Validate config option."""
        return key in DEFAULT_CONFIG
