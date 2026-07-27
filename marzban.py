# ==========================================================
# Zeus Shop VPN PRO
# marzban.py
# Part 1/4
# ==========================================================


import requests
import random
import string
import time



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





    # ======================================================
    # Login
    # ======================================================


    def login(self):


        try:


            response = requests.post(

                f"{self.url}/api/admin/token",

                data={

                    "username": self.username,

                    "password": self.password

                },

                timeout=20

            )



            if response.status_code == 200:


                self.token = response.json().get(

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





        except Exception as error:


            print(

                "❌ Marzban Error:",

                error

            )


            return False






    # ======================================================
    # Headers
    # ======================================================


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






    # ======================================================
    # GB To Byte
    # ======================================================


    def gb_to_bytes(

        self,

        gb

    ):


        return int(gb) * 1024 * 1024 * 1024





    # ======================================================
    # Random Username
    # ======================================================


    def random_username(self):


        chars = (

            string.ascii_lowercase

            +

            string.digits

        )



        name = "".join(

            random.choice(chars)

            for _ in range(8)

        )



        return "zeus_" + name
        # ==========================================================
# Create & Get User
# Part 2/4
# ==========================================================



    # ======================================================
    # Create User
    # ======================================================


    def create_user(

        self,

        username=None,

        data_limit=0,

        expire=None

    ):



        headers = self.headers()



        if not headers:

            return None





        if username is None:


            username = self.random_username()





        if expire is None:


            expire = int(time.time()) + (

                30 *

                24 *

                60 *

                60

            )






        payload = {


            "username": username,


            "proxies": {


                "vless": {}

            },


            "expire": expire,


            "data_limit": data_limit,


            "data_limit_reset_strategy": "no_reset"


        }






        try:



            response = requests.post(

                f"{self.url}/api/user",

                json=payload,

                headers=headers,

                timeout=20

            )




            print(

                "CREATE USER:",

                response.text

            )





            if response.status_code in [200,201]:


                return response.json()





            return None





        except Exception as error:


            print(

                "CREATE USER ERROR:",

                error

            )


            return None






    # ======================================================
    # Get User
    # ======================================================


    def get_user(

        self,

        username

    ):


        headers = self.headers()



        if not headers:

            return None






        try:



            response = requests.get(

                f"{self.url}/api/user/{username}",

                headers=headers,

                timeout=20

            )






            if response.status_code == 200:


                return response.json()





            return None






        except Exception as error:



            print(

                "GET USER ERROR:",

                error

            )


            return None






    # ======================================================
    # Subscription Link
    # ======================================================


    def subscription(

        self,

        username

    ):



        user = self.get_user(

            username

        )



        if not user:


            return None





        link = (

            user.get("subscription_url")

            or

            user.get("subscription")

        )





        if not link:


            return None





        if link.startswith("http"):


            return link





        return self.url + link
        # ==========================================================
# User Management
# Part 3/4
# ==========================================================



    # ======================================================
    # Delete User
    # ======================================================


    def delete_user(

        self,

        username

    ):


        headers = self.headers()



        if not headers:

            return False





        try:


            response = requests.delete(

                f"{self.url}/api/user/{username}",

                headers=headers,

                timeout=20

            )





            if response.status_code in [

                200,

                204

            ]:


                return True





            print(

                "DELETE ERROR:",

                response.text

            )



            return False






        except Exception as error:



            print(

                "DELETE USER ERROR:",

                error

            )


            return False







    # ======================================================
    # Update User
    # ======================================================


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



            response = requests.put(

                f"{self.url}/api/user/{username}",

                json=payload,

                headers=headers,

                timeout=20

            )






            if response.status_code == 200:


                return True






            print(

                "UPDATE ERROR:",

                response.text

            )



            return False






        except Exception as error:



            print(

                "UPDATE USER ERROR:",

                error

            )


            return False







    # ======================================================
    # Check User Exists
    # ======================================================


    def user_exists(

        self,

        username

    ):


        user = self.get_user(

            username

        )



        return True if user else False







    # ======================================================
    # Get All Users
    # ======================================================


    def get_users(self):


        headers = self.headers()



        if not headers:

            return []







        try:



            response = requests.get(

                f"{self.url}/api/users",

                headers=headers,

                timeout=20

            )






            if response.status_code == 200:


                data = response.json()


                return data.get(

                    "users",

                    []

                )






            return []






        except Exception as error:



            print(

                "GET USERS ERROR:",

                error

            )


            return []
            # ==========================================================
# Service Builder
# Part 4/4
# ==========================================================



    # ======================================================
    # Test Connection
    # ======================================================


    def test_connection(self):


        return self.login()





    # ======================================================
    # Panel Info
    # ======================================================


    def panel_info(self):


        return {


            "url":

            self.url,


            "username":

            self.username,


            "status":

            "online"

            if self.token

            else

            "offline"


        }






    # ======================================================
    # Create Complete Service
    # ======================================================


    def create_service(

        self,

        volume,

        days

    ):



        # تبدیل حجم

        data_limit = self.gb_to_bytes(

            volume

        )





        # تاریخ انقضا

        expire = int(time.time()) + (

            int(days)

            *

            24

            *

            60

            *

            60

        )






        user = self.create_user(

            data_limit=data_limit,

            expire=expire

        )





        if not user:


            return None






        username = user.get(

            "username"

        )





        if not username:


            return None






        subscription = self.subscription(

            username

        )






        return {


            "username":

            username,



            "subscription_url":

            subscription,



            "volume":

            volume,



            "days":

            days,



            "expire":

            expire


        }







# ==========================================================
# Test
# ==========================================================


if __name__ == "__main__":


    marzban = Marzban()



    if marzban.test_connection():


        print(

            "✅ Panel OK"

        )


    else:


        print(

            "❌ Panel Error"

        )
