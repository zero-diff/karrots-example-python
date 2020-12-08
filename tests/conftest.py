import pytest

from src.server import service as flask_app


@pytest.fixture
def service():
    yield flask_app


@pytest.fixture
def client(service):
    return service.test_client()
