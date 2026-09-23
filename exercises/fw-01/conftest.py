import pytest
from api_client import ApiClient
import uuid

@pytest.fixture
def api_client():
    return ApiClient()

@pytest.fixture
def auth_token(api_client):
    #unique_email = f"grace{uuid.uuid4().hex[:8]}@example.com"
    api_client.register_user("Grace", "Hopper", "grace@example.com", "Secret123!")
    response = api_client.login("grace@example.com", "Secret123!")
    return response.json()["token"]

@pytest.fixture
def authenticated_client(api_client):
    unique_email = f"grace{uuid.uuid4().hex[:8]}@example.com"
    api_client.register_user("Grace", "Hopper", unique_email, "Secret123!")
    response = api_client.login("grace@example.com", "Secret123!")
    token= response.json()["token"]
    return api_client, token

@pytest.fixture
def existing_contact(authenticated_client):
    client, token = authenticated_client
    resp = client.create_contact("Ada", "Lovelace", "adatt@test.com","555-0100","London",token)
    contact_id = resp.json()["id"]
    yield contact_id
    client.delete_contact(token, contact_id)