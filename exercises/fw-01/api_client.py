from wsgiref import headers

import requests
from config import BASE_URL

class ApiClient:
    def __init__(self):
        self.session = requests.Session()

    def register_user(self,first_name,last_name,email,password):
        return self.session.post(f"{BASE_URL}/api/public/users",
        json = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": password,
        },)

    def login(self, email, password):
        return self.session.post(
            f"{BASE_URL}/api/public/users/login",
            json={"email": email, "password": password},
        )

    def get_me(self, token):
        return self.session.get(
            f"{BASE_URL}/api/public/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )

    def create_contact(self, first_name,last_name,email,phone,city,token):
       return self.session.post(f"{BASE_URL}/api/public/contacts",
        json = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "city": city,
        },
        headers={"Authorization": f"Bearer {token}"},
        )

    def list_contacts(self, token):
        return self.session.get(f"{BASE_URL}/api/public/contacts",
        headers={"Authorization": f"Bearer {token}"},
        )

    def get_contact_by_id(self,token,id):
        return self.session.get(f"{BASE_URL}/api/public/contacts/{id}",
                                headers={"Authorization": f"Bearer {token}"},
        )

    def put_contact(self,first_name,last_name,email,token,contact_id):
        return self.session.put(f"{BASE_URL}/api/public/contacts/{contact_id}",
            json={"firstName": first_name,
                  "lastName": last_name,
                  "email": email },
            headers={"Authorization": f"Bearer {token}"},)

    def patch_contact(self,phone,token,contact_id):
        return self.session.patch(f"{BASE_URL}/api/public/contacts/{contact_id}",
            json={"phone": phone},
            headers={"Authorization": f"Bearer {token}"},)

    def delete_contact(self, token,id):
       return self.session.delete(f"{BASE_URL}/api/public/contacts/{id}",
                                  headers={"Authorization": f"Bearer {token}"},)


    def delete_me(self, token):
        return self.session.delete(f"{BASE_URL}/api/public/users/me",
        headers = {"Authorization": f"Bearer {token}"},
        )

#list_contacts, create_contact, get_contact, update_contact (PUT), patch_contact, delete_contact

