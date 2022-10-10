import pytest

from music import create_app
from music.adapters import memory_repository
from music.adapters.memory_repository import MemoryRepository

from utils import get_project_root

# the csv files in the test folder are different from the csv files in the music/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_DATA_PATH = get_project_root() / "tests" / "data"


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'TEST_DATA_PATH': TEST_DATA_PATH})
    return app.test_client()
