import pytest
from api_client import ApiClient
import uuid

@pytest.fixture
def api_client():
    return ApiClient()
