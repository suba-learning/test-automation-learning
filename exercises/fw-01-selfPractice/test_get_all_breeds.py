import requests
from config import BASE_URL
from api_client import ApiClient

def test_get_all_breeds():
    client = ApiClient()
    response = client.get_all_breeds()
    print(response.text)
    assert response.status_code == 200