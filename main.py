import requests

from config import (
    MARZBAN_URL,
    MARZBAN_USERNAME,
    MARZBAN_PASSWORD
)


class Marzban:

    def __init__(self):
        self.url = MARZBAN_URL.rstrip("/")
        self.username = MARZBAN_USERNAME
        self.password = MARZBAN_PASSWORD
        self.token = None


    def login(self):
        url = f"{self.url}/api/admin/token"

        data = {
            "username": self.username,
            "password": self.password
        }

        response = requests.post(
            url,
            data=data,
            timeout=20
        )

        if response.status_code == 200:
            self.token = response.json()["access_token"]
            return True

        print("Login Error:")
        print(response.text)

        return False


    def headers(self):
        return {
            "Authorization": f"Bearer {self.token}"
        }


    def test(self):

        if self.login():
            print("Marzban Connected ✅")
            return True

        print("Marzban Failed ❌")
        return False
