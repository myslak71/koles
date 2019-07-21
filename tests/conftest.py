"""pytest configuration file."""
import pytest
from koles.checker import KolesChecker
from koles.config import KolesConfig


@pytest.fixture
def config_fixture():
    """Return simple KolesConfig."""
    koles_config = KolesConfig(path='test_path', run_dir='run_dir')
    yield koles_config


@pytest.fixture
def koles_checker_fixture(config_fixture):
    """Return clean KolesChecker instance."""
    koles_checker = KolesChecker(config_fixture)
    yield koles_checker
