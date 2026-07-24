# =========================
# marzban.py
# Zeus Shop VPN
# =========================

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



    # =====================
    # ورود به پنل
    # =====================

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

            self.token = response.json().get(
                "access_token"
            )

            return True



        print(
            "Marzban Login Error:",
            response.text
        )


        return False




    # =====================
    # هدر درخواست
    # =====================

    def headers(self):


        if not self.token:

            if not self.login():

                return None



        return {

            "Authorization":
            f"Bearer {self.token}",

            "Content-Type":
            "application/json"

        }





    # =====================
    # ساخت یوزر
    # =====================

    def create_user(
        self,
        username=None,
        data_limit=0
    ):


        headers = self.headers()


        if headers is None:

            return None



        if username is None:

            username = self.random_username()



        url = f"{self.url}/api/user"



        payload = {


            "username": username,


            "proxies": {

                "vless": {}

            },


            "inbounds": {

                "vless": [

                    "VLESS-WS"

                ]

            },


            "expire": 0,


            "data_limit": data_limit,


            "data_limit_reset_strategy":
            "no_reset"

        }



        response = requests.post(

            url,

            json=payload,

            headers=headers,

            timeout=20

        )



        print(
            response.text
        )



        if response.status_code in [200,201]:

            return response.json()



        return None





    # =====================
    # نام تصادفی
    # =====================

    def random_username(self):


        chars = (
            string.ascii_lowercase
            +
            string.digits
        )


        return (
            "user_"
            +
            "".join(

                random.choice(chars)

                for _ in range(8)

            )
        )





    # =====================
    # گرفتن کاربر
    # =====================

    def get_user(self, username):


        headers = self.headers()


        if headers is None:

            return None



        response = requests.get(

            f"{self.url}/api/user/{username}",

            headers=headers,

            timeout=20

        )



        if response.status_code == 200:

            return response.json()



        return None





    # =====================
    # لینک اشتراک
    # =====================

    def subscription(self, username):


        user = self.get_user(username)



        if not user:

            return None



        sub = user.get(
            "subscription_url"
        )



        if not sub:

            return None



        if sub.startswith("http"):

            return sub



        return self.url + sub
