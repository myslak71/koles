"""Koles config module."""
import configparser


class KolesConfig:
    """Koles config class."""

    ALLOW_CONFIG_FILENAMES = ('setup.cfg',)

    def __init__(self, path, run_dir: str) -> None:
        """Set path and config."""
        self.path = path
        self.run_dir = run_dir

    def get_config(self):
        """Set config."""
        config = configparser.ConfigParser()

        try:
            config.read(f'{self.run_dir}/{self.ALLOW_CONFIG_FILENAMES[0]}')
            config.sections()
        except Exception as e:
            print(e)
