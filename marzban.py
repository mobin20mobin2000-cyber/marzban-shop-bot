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
    # ورود به مرزبان
    # =====================

    def login(self):

        try:

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


                if self.token:

                    print(
                        "✅ Marzban Login Success"
                    )

                    return True



            print(
                "❌ Marzban Login Failed:",
                response.text
            )


            return False



        except Exception as e:


            print(
                "❌ Login Error:",
                e
            )


            return False





    # =====================
    # هدر
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
    # تبدیل گیگ به بایت
    # =====================

    def gb_to_bytes(self, gb):

        return int(gb) * 1024 * 1024 * 1024





    # =====================
    # ساخت کاربر مرزبان
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

                "vless": []

            },


            "expire": 0,


            "data_limit": data_limit,


            "data_limit_reset_strategy":

                "no_reset"


        }




        try:


            response = requests.post(

                url,

                json=payload,

                headers=headers,

                timeout=20

            )



            print(
                "CREATE USER:",
                response.text
            )



            if response.status_code in (

                200,

                201

            ):


                return response.json()



            return None




        except Exception as e:


            print(

                "CREATE USER ERROR:",

                e

            )


            return None






    # =====================
    # ساخت نام کاربری
    # =====================


    def random_username(self):


        chars = (

            string.ascii_lowercase

            +

            string.digits

        )


        return (

            "zeus_"

            +

            "".join(

                random.choice(chars)

                for _ in range(8)

            )

        )
            # =====================
    # دریافت اطلاعات کاربر
    # =====================

    def get_user(
        self,
        username
    ):


        headers = self.headers()


        if headers is None:

            return None



        try:


            response = requests.get(

                f"{self.url}/api/user/{username}",

                headers=headers,

                timeout=20

            )


            if response.status_code == 200:

                return response.json()



            print(
                "GET USER ERROR:",
                response.text
            )


            return None



        except Exception as e:


            print(
                "GET USER EXCEPTION:",
                e
            )


            return None






    # =====================
    # لینک اشتراک
    # =====================

    def subscription(
        self,
        username
    ):


        user = self.get_user(
            username
        )



        if not user:

            return None



        subscription = user.get(
            "subscription_url"
        )



        if not subscription:

            return None



        if subscription.startswith(
            "http"
        ):

            return subscription



        return (

            self.url

            +

            subscription

        )






    # =====================
    # حذف کاربر
    # =====================

    def delete_user(
        self,
        username
    ):


        headers = self.headers()


        if headers is None:

            return False



        try:


            response = requests.delete(

                f"{self.url}/api/user/{username}",

                headers=headers,

                timeout=20

            )



            return response.status_code == 200



        except Exception as e:


            print(
                "DELETE ERROR:",
                e
            )


            return False





    # =====================
    # تمدید حجم و زمان
    # =====================

    def update_user(
        self,
        username,
        data_limit=None,
        expire=None
    ):


        headers = self.headers()


        if headers is None:

            return False



        payload = {}



        if data_limit:

            payload["data_limit"] = data_limit



        if expire:

            payload["expire"] = expire





        try:


            response = requests.put(

                f"{self.url}/api/user/{username}",

                json=payload,

                headers=headers,

                timeout=20

            )



            return response.status_code == 200



        except Exception as e:


            print(
                "UPDATE ERROR:",
                e
            )


            return False
        # =====================
    # دریافت اطلاعات کاربر
    # =====================

    def get_user(
        self,
        username
    ):


        headers = self.headers()


        if headers is None:

            return None



        try:


            response = requests.get(

                f"{self.url}/api/user/{username}",

                headers=headers,

                timeout=20

            )


            if response.status_code == 200:

                return response.json()



            print(
                "GET USER ERROR:",
                response.text
            )


            return None



        except Exception as e:


            print(
                "GET USER EXCEPTION:",
                e
            )


            return None






    # =====================
    # لینک اشتراک
    # =====================

    def subscription(
        self,
        username
    ):


        user = self.get_user(
            username
        )



        if not user:

            return None



        subscription = user.get(
            "subscription_url"
        )



        if not subscription:

            return None



        if subscription.startswith(
            "http"
        ):

            return subscription



        return (

            self.url

            +

            subscription

        )






    # =====================
    # حذف کاربر
    # =====================

    def delete_user(
        self,
        username
    ):


        headers = self.headers()


        if headers is None:

            return False



        try:


            response = requests.delete(

                f"{self.url}/api/user/{username}",

                headers=headers,

                timeout=20

            )



            return response.status_code == 200



        except Exception as e:


            print(
                "DELETE ERROR:",
                e
            )


            return False





    # =====================
    # تمدید حجم و زمان
    # =====================

    def update_user(
        self,
        username,
        data_limit=None,
        expire=None
    ):


        headers = self.headers()


        if headers is None:

            return False



        payload = {}



        if data_limit:

            payload["data_limit"] = data_limit



        if expire:

            payload["expire"] = expire





        try:


            response = requests.put(

                f"{self.url}/api/user/{username}",

                json=payload,

                headers=headers,

                timeout=20

            )



            return response.status_code == 200



        except Exception as e:


            print(
                "UPDATE ERROR:",
                e
            )


            return False
