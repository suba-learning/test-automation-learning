import requests
from config import BASE_URL


class ApiClient:
    def __init__(self):
        self.session = requests.Session()

    def get_all_breeds(self):
        return self.session.get(f"{BASE_URL}/api/breeds.json")