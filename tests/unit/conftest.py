""" configure pytest """
import pytest

# pylint: disable=import-error
from server import server as flask_app


@pytest.fixture
def service():
    """ setup service """
    yield flask_app


@pytest.fixture
# pylint: disable=redefined-outer-name
def client(service):
    """ setup client """
    return service.test_client()
