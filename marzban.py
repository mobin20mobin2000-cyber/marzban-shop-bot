# =========================
# marzban.py
# Zeus Shop VPN PRO
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


        self.session = requests.Session()



    # =========================
    # Login
    # =========================

    def login(self):

        try:

            url = f"{self.url}/api/admin/token"


            data = {

                "username": self.username,

                "password": self.password

            }


            response = self.session.post(

                url,

                data=data,

                timeout=20

            )


            if response.status_code == 200:

                result = response.json()


                self.token = result.get(
                    "access_token"
                )


                if self.token:

                    print(
                        "✅ Marzban Connected"
                    )

                    return True



            print(
                "❌ Marzban Login Failed",
                response.text
            )


            return False



        except Exception as e:


            print(
                "❌ Marzban Login Error:",
                e
            )


            return False




    # =========================
    # Headers
    # =========================

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




    # =========================
    # GB To Byte
    # =========================

    def gb_to_bytes(
        self,
        gb
    ):

        return int(gb) * 1024 * 1024 * 1024



    # =========================
    # Random Username
    # =========================

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
            # =========================
    # Create User
    # =========================

    def create_user(
        self,
        username=None,
        data_limit=0,
        expire=0
    ):

        headers = self.headers()


        if not headers:

            return None



        if username is None:

            username = self.random_username()



        payload = {

            "username": username,


            "proxies": {

                "vless": {}

            },


            "inbounds": {

                "vless": []

            },


            "expire": expire,


            "data_limit": data_limit,


            "data_limit_reset_strategy":

            "no_reset"

        }



        try:

            response = self.session.post(

                f"{self.url}/api/user",

                json=payload,

                headers=headers,

                timeout=20

            )


            print(
                "CREATE USER:",
                response.text
            )



            if response.status_code in [200, 201]:

                return response.json()



            return None



        except Exception as e:


            print(
                "CREATE USER ERROR:",
                e
            )


            return None




    # =========================
    # Get User
    # =========================

    def get_user(
        self,
        username
    ):

        headers = self.headers()


        if not headers:

            return None



        try:

            response = self.session.get(

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




    # =========================
    # Subscription Link
    # =========================

    def subscription(
        self,
        username
    ):


        user = self.get_user(
            username
        )



        if not user:

            return None



        link = user.get(
            "subscription_url"
        )



        if not link:

            return None



        if link.startswith(
            "http"
        ):

            return link



        return (
            self.url
            +
            link
    )
            # =========================
    # Delete User
    # =========================

    def delete_user(
        self,
        username
    ):

        headers = self.headers()


        if not headers:

            return False



        try:

            response = self.session.delete(

                f"{self.url}/api/user/{username}",

                headers=headers,

                timeout=20

            )


            if response.status_code == 200:

                return True



            print(
                "DELETE USER ERROR:",
                response.text
            )


            return False



        except Exception as e:


            print(
                "DELETE USER EXCEPTION:",
                e
            )


            return False




    # =========================
    # Update User
    # تمدید حجم و زمان
    # =========================

    def update_user(
        self,
        username,
        data_limit=None,
        expire=None
    ):


        headers = self.headers()


        if not headers:

            return False



        payload = {}



        if data_limit is not None:

            payload["data_limit"] = data_limit



        if expire is not None:

            payload["expire"] = expire



        if not payload:

            return False



        try:

            response = self.session.put(

                f"{self.url}/api/user/{username}",

                json=payload,

                headers=headers,

                timeout=20

            )



            if response.status_code == 200:

                return True



            print(
                "UPDATE USER ERROR:",
                response.text
            )


            return False



        except Exception as e:


            print(
                "UPDATE USER EXCEPTION:",
                e
            )


            return False




    # =========================
    # Test Connection
    # =========================

    def test_connection(self):


        if self.login():

            return True


        return False
