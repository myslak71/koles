"""Koles config parser module."""
import configparser


class KolesConfigParser:
    """Koles config parser."""

    CONFIG_FILENAME = 'setup.cfg'

    def __init__(self, path: str) -> None:
        """Set path and config."""
        self.path = path
        self._get_config()

    def _get_config(self):
        """Set config."""
        try:
            config = configparser.ConfigParser()
            config.read(f'{self.path}/{self.CONFIG_FILENAME}')
            config.sections()
        except Exception as e:
            print(e)
