import requests
from config import BASE_URL
from api_client import ApiClient
import uuid

def test_register_user():
    client = ApiClient()
    response = client.register_user("Ada", "Lovelace", f"ada{uuid.uuid4().hex[:8]}@example.com", "Secret123!")
    assert response.status_code == 201

def test_get_me(authenticated_client):
    client, token = authenticated_client
    resp = client.get_me(token)
    assert resp.status_code == 200
    assert resp.json()["email"].startswith("grace")

def test_create_contact(authenticated_client):
    api_client, auth_token = authenticated_client
    resp = api_client.create_contact("Ada", "Lovelace", "adatt@test.com","555-0100","London",auth_token)
    assert resp.status_code == 201
    assert resp.json()["firstName"].startswith("Ada")

def test_get_contacts(authenticated_client):
    api_client, auth_token = authenticated_client
    resp = api_client.list_contacts(auth_token)
    assert resp.status_code == 200
    #assert resp.json()["count"] > 0

def test_get_contact_by_id(authenticated_client,existing_contact):
    api_client, auth_token = authenticated_client
    contact_id = existing_contact
    # create_resp = api_client.create_contact("Suba", "Lovelace", "adatt@test.com", "555-0100", "London", auth_token)
    #contact_id = create_resp.json()["id"]
    resp = api_client.get_contact_by_id(auth_token, contact_id)
    assert resp.status_code == 200
    assert resp.json()["firstName"].startswith("Ada")


def test_update_contact(authenticated_client,existing_contact):
    api_client, auth_token = authenticated_client
    contact_id = existing_contact
    #resp = api_client.get_me(auth_token)
    # create_resp = api_client.create_contact("Narayanan", "Lovelace", "adatt@test.com", "555-0100", "London", auth_token)
    # contact_id = create_resp.json()["id"]
    resp = api_client.put_contact("Narayanan", "Lovelace", "adatt@test.com",auth_token, contact_id)
    assert resp.status_code == 200
    assert resp.json()["firstName"].startswith("Narayanan")

def test_patch_contact(authenticated_client,existing_contact):
    api_client, auth_token = authenticated_client
    contact_id = existing_contact
    resp = api_client.patch_contact("555-1100",auth_token, contact_id)
    assert resp.status_code == 200

def test_delete_contact(authenticated_client,existing_contact):
    api_client, auth_token = authenticated_client
    contact_id = existing_contact
    resp = api_client.delete_contact(auth_token, contact_id)
    assert resp.status_code == 204
