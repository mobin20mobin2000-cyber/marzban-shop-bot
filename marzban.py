# ==========================================================
# Zeus Shop VPN PRO
# marzban.py
# Part 1/4
# ==========================================================

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



    # ======================================================
    # ورود به پنل Marzban
    # ======================================================

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




        except Exception as error:


            print(
                "❌ Marzban Login Error:",
                error
            )


            return False





    # ======================================================
    # ساخت Header
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
    # تبدیل گیگابایت به بایت
    # ======================================================

    def gb_to_bytes(
        self,
        gb
    ):

        return int(gb) * 1024 * 1024 * 1024





    # ======================================================
    # ساخت نام کاربری تصادفی
    # ======================================================

    def random_username(self):


        chars = (

            string.ascii_lowercase

            +

            string.digits

        )


        random_text = "".join(

            random.choice(chars)

            for _ in range(8)

        )


        return (
            "zeus_"
            +
            random_text
        )
        # ==========================================================
# ساخت و مدیریت کاربر Marzban
# Part 2/4
# ==========================================================


    # ======================================================
    # ساخت کاربر جدید
    # ======================================================

    def create_user(
        self,
        username=None,
        data_limit=0,
        expire=0
    ):


        headers = self.headers()


        if headers is None:

            return None




        if username is None:

            username = self.random_username()




        payload = {


            "username":

            username,



            "proxies":

            {

                "vless": {}

            },



            "inbounds":

            {

                "vless": []

            },



            "expire":

            expire,



            "data_limit":

            data_limit,



            "data_limit_reset_strategy":

            "no_reset"

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




            if response.status_code in (

                200,

                201

            ):


                return response.json()




            return None




        except Exception as error:


            print(

                "CREATE USER ERROR:",

                error

            )


            return None






    # ======================================================
    # دریافت اطلاعات کاربر
    # ======================================================

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




        except Exception as error:


            print(

                "GET USER ERROR:",

                error

            )


            return None






    # ======================================================
    # دریافت لینک اشتراک
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
        # ==========================================================
# عملیات کاربر Marzban
# Part 3/4
# ==========================================================


    # ======================================================
    # حذف کاربر
    # ======================================================

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




            if response.status_code in (

                200,

                204

            ):

                return True




            print(

                "DELETE USER ERROR:",

                response.text

            )


            return False




        except Exception as error:


            print(

                "DELETE ERROR:",

                error

            )


            return False






    # ======================================================
    # بروزرسانی کاربر
    # ======================================================

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

                "UPDATE USER ERROR:",

                response.text

            )


            return False




        except Exception as error:


            print(

                "UPDATE ERROR:",

                error

            )


            return False






    # ======================================================
    # بررسی وجود کاربر
    # ======================================================

    def user_exists(
        self,
        username
    ):


        user = self.get_user(
            username
        )


        if user:

            return True



        return False






    # ======================================================
    # دریافت لیست کاربران
    # ======================================================

    def get_users(
        self
    ):


        headers = self.headers()


        if headers is None:

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
# ابزارهای تکمیلی Marzban
# Part 4/4
# ==========================================================


    # ======================================================
    # وضعیت اتصال پنل
    # ======================================================

    def test_connection(self):


        if self.login():

            return True


        return False





    # ======================================================
    # اطلاعات پنل
    # ======================================================

    def panel_info(self):


        return {


            "url":

            self.url,


            "username":

            self.username,


            "status":

            "connected"

            if self.token

            else

            "offline"

        }






    # ======================================================
    # ساخت سرویس کامل
    # ======================================================

    def create_service(
        self,
        volume,
        days
    ):


        data_limit = self.gb_to_bytes(
            volume
        )



        expire = (

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



            "subscription":

            subscription,



            "volume":

            volume,



            "days":

            days

        }





    # ======================================================
    # پایان
    # ======================================================
