# ==========================================================
# Zeus Shop VPN PRO
# marzban.py
# Part 1/6
# ==========================================================

import time
import requests
import random
import string

from config import (
    MARZBAN_URL,
    MARZBAN_USERNAME,
    MARZBAN_PASSWORD,
)


class Marzban:

    def __init__(self):

        self.base_url = MARZBAN_URL.rstrip("/")

        self.token = None

        self.login()
            # ==========================================================
    # Login
    # ==========================================================

    def login(self):

        url = f"{self.base_url}/api/admin/token"

        response = requests.post(

            url,

            data={

                "username": MARZBAN_USERNAME,

                "password": MARZBAN_PASSWORD,

            },

            timeout=30

        )

        response.raise_for_status()

        self.token = response.json()["access_token"]

        return self.token


    # ==========================================================
    # Headers
    # ==========================================================

    def headers(self):

        return {

            "Authorization": f"Bearer {self.token}",

            "Content-Type": "application/json",

            "Accept": "application/json"

        }


    # ==========================================================
    # Generate Username
    # ==========================================================

    def generate_username(self, user_id):

        rand = "".join(

            random.choice(

                string.ascii_lowercase + string.digits

            )

            for _ in range(6)

        )

        return f"z{user_id}_{rand}"
            # ==========================================================
    # Create Service
    # ==========================================================

    def create_service(

        self,

        user_id,

        volume,

        days

    ):

        username = self.generate_username(user_id)

        payload = {

            "username": username,

            "status": "active",

            "note": "Zeus Shop VPN",

            "expire": int(time.time()) + (days * 86400),

            "data_limit": (
                volume * 1024 * 1024 * 1024
                if volume > 0
                else 0
            ),

            "data_limit_reset_strategy": "no_reset",

            "proxies": {

                "vmess": {},

                "vless": {},

                "trojan": {},

                "shadowsocks": {}

            }

        }

        response = requests.post(

            f"{self.base_url}/api/user",

            headers=self.headers(),

            json=payload,

            timeout=30

        )

        response.raise_for_status()

        user = response.json()

        return {

            "username": user["username"],

            "subscription_url": user.get(

                "subscription_url",

                ""

            )

        }
        # ==========================================================
# Part 5
# Helpers
# ==========================================================

    def refresh_token(self):
        """Refresh expired token"""
        global TOKEN
        TOKEN = None
        self.token = self.login()
        return self.token

    def ping(self):
        """Test panel connection"""
        try:
            response = requests.get(
                f"{self.base_url}/api/system",
                headers=self.headers(),
                timeout=10,
            )
            return response.status_code == 200
        except Exception:
            return False

    def user_exists(self, username):
        try:
            self.get_user(username)
            return True
        except Exception:
            return False

    def get_subscription(self, username):
        user = self.get_user(username)
        return user.get("subscription_url")

    def get_usage(self, username):
        user = self.get_user(username)

        return {
            "used": user.get("used_traffic", 0),
            "limit": user.get("data_limit", 0),
            "expire": user.get("expire", 0),
            "status": user.get("status"),
        }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    panel = Marzban()

    if panel.ping():
        print("✅ Connected to Marzban")
    else:
        print("❌ Connection failed")
            # ==========================================================
    # Update Service
    # ==========================================================

    def update_service(

        self,

        username,

        volume,

        days

    ):

        payload = {

            "status": "active",

            "expire": int(time.time()) + (days * 86400),

            "data_limit": (
                volume * 1024 * 1024 * 1024
                if volume > 0
                else 0
            )

        }

        response = requests.put(

            f"{self.base_url}/api/user/{username}",

            headers=self.headers(),

            json=payload,

            timeout=30

        )

        response.raise_for_status()

        return response.json()


    # ==========================================================
    # Delete Service
    # ==========================================================

    def delete_service(

        self,

        username

    ):

        response = requests.delete(

            f"{self.base_url}/api/user/{username}",

            headers=self.headers(),

            timeout=30

        )

        response.raise_for_status()

        return True


    # ==========================================================
    # Enable Service
    # ==========================================================

    def enable_service(self, username):

        payload = {

            "status": "active"

        }

        response = requests.put(

            f"{self.base_url}/api/user/{username}",

            headers=self.headers(),

            json=payload,

            timeout=30

        )

        response.raise_for_status()

        return response.json()


    # ==========================================================
    # Disable Service
    # ==========================================================

    def disable_service(self, username):

        payload = {

            "status": "disabled"

        }

        response = requests.put(

            f"{self.base_url}/api/user/{username}",

            headers=self.headers(),

            json=payload,

            timeout=30

        )

        response.raise_for_status()

        return response.json()
        # ==========================================================
# Part 6
# System / Helpers
# ==========================================================

    def get_user(self, username):

        response = requests.get(

            f"{self.base_url}/api/user/{username}",

            headers=self.headers(),

            timeout=30

        )

        response.raise_for_status()

        return response.json()


    # ==========================================================
    # Get All Users
    # ==========================================================

    def get_users(self):

        response = requests.get(

            f"{self.base_url}/api/users",

            headers=self.headers(),

            timeout=30

        )

        response.raise_for_status()

        return response.json()


    # ==========================================================
    # Get System Info
    # ==========================================================

    def get_system_stats(self):

        response = requests.get(

            f"{self.base_url}/api/system",

            headers=self.headers(),

            timeout=30

        )

        response.raise_for_status()

        return response.json()


    # ==========================================================
    # Refresh Token
    # ==========================================================

    def refresh_token(self):

        self.token = None

        return self.login()


    # ==========================================================
    # Ping
    # ==========================================================

    def ping(self):

        try:

            response = requests.get(

                f"{self.base_url}/api/system",

                headers=self.headers(),

                timeout=10

            )

            return response.status_code == 200

        except Exception:

            return False


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    panel = Marzban()

    if panel.ping():

        print("✅ Marzban Connected")

    else:

        print("❌ Marzban Connection Failed")
