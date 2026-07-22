import requests
import random
import string

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


    # ورود به پنل و گرفتن توکن
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


    # هدر احراز هویت
    def headers(self):

        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }


    # تست اتصال
    def test(self):

        if self.login():
            print("Marzban Connected ✅")
            return True

        print("Marzban Failed ❌")
        return False



    # ساخت نام کاربری تصادفی
    def random_username(self):

        chars = string.ascii_lowercase

        return "user_" + "".join(
            random.choice(chars)
            for _ in range(8)
        )



    # ساخت کاربر جدید
    def create_user(
        self,
        username=None,
        days=30,
        data_limit=0
    ):

        if not self.token:
            self.login()


        if username is None:
            username = self.random_username()


        url = f"{self.url}/api/user"


        payload = {

            "username": username,

            "proxies": {
                "vless": {}
            },


            "inbounds": {

                "vless": []

            },


            "expire": days * 86400,

            "data_limit": data_limit

        }


        response = requests.post(

            url,

            json=payload,

            headers=self.headers(),

            timeout=20

        )


        print(response.text)


        if response.status_code in [200,201]:

            return response.json()


        return None



    # گرفتن اطلاعات کاربر
    def get_user(self, username):

        if not self.token:
            self.login()


        url = f"{self.url}/api/user/{username}"


        response = requests.get(

            url,

            headers=self.headers(),

            timeout=20

        )


        if response.status_code == 200:

            return response.json()


        return None



    # حذف کاربر
    def delete_user(self, username):

        if not self.token:
            self.login()


        url = f"{self.url}/api/user/{username}"


        response = requests.delete(

            url,

            headers=self.headers(),

            timeout=20

        )


        return response.status_code == 200



    # لیست کاربران
    def users(self):

        if not self.token:
            self.login()


        url = f"{self.url}/api/users"


        response = requests.get(

            url,

            headers=self.headers(),

            timeout=20

        )


        if response.status_code == 200:

            return response.json()


        return None
