# ==========================================================
# Zeus Shop VPN PRO
# marzban.py
# Part 1/5
# ==========================================================

import requests

from config import (
    MARZBAN_URL,
    MARZBAN_USERNAME,
    MARZBAN_PASSWORD,
)

TOKEN = None


class Marzban:

    def __init__(self):

        self.base_url = MARZBAN_URL.rstrip("/")

        self.token = self.login()

    # ======================================================
    # Login
    # ======================================================

    def login(self):

        global TOKEN

        if TOKEN:
            return TOKEN

        url = f"{self.base_url}/api/admin/token"

        response = requests.post(
            url,
            data={
                "username": MARZBAN_USERNAME,
                "password": MARZBAN_PASSWORD,
            },
            timeout=30,
        )

        response.raise_for_status()

        TOKEN = response.json()["access_token"]

        return TOKEN

    # ======================================================
    # Headers
    # ======================================================

    def headers(self):

        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        # ==========================================================
# Create User
# ==========================================================

    def create_service(
        self,
        volume,
        days
    ):

        url = f"{self.base_url}/api/user"

        payload = {

            "username": None,

            "proxies": {
                "vmess": {},
                "vless": {},
                "trojan": {},
                "shadowsocks": {}
            },

            "expire": days * 86400,

            "data_limit": volume * 1024 * 1024 * 1024 if volume else 0,

            "data_limit_reset_strategy": "no_reset",

            "status": "active",

            "note": "Zeus Shop VPN"

        }

        response = requests.post(

            url,

            headers=self.headers(),

            json=payload,

            timeout=30

        )

        response.raise_for_status()

        user = response.json()

        return {

            "username": user["username"],

            "subscription_url": user["subscription_url"]

        }


# ==========================================================
# Get User
# ==========================================================

    def get_user(
        self,
        username
    ):

        url = f"{self.base_url}/api/user/{username}"

        response = requests.get(

            url,

            headers=self.headers(),

            timeout=30

        )

        response.raise_for_status()

        return response.json()
        # ==========================================================
# Update User
# ==========================================================

    def update_service(
        self,
        username,
        volume,
        days
    ):

        url = f"{self.base_url}/api/user/{username}"

        payload = {

            "data_limit": (
                volume * 1024 * 1024 * 1024
                if volume > 0
                else 0
            ),

            "expire": days * 86400,

            "status": "active"

        }

        response = requests.put(

            url,

            headers=self.headers(),

            json=payload,

            timeout=30

        )

        response.raise_for_status()

        return response.json()


# ==========================================================
# Delete User
# ==========================================================

    def delete_service(
        self,
        username
    ):

        url = f"{self.base_url}/api/user/{username}"

        response = requests.delete(

            url,

            headers=self.headers(),

            timeout=30

        )

        response.raise_for_status()

        return True


# ==========================================================
# Enable User
# ==========================================================

    def enable_service(
        self,
        username
    ):

        url = f"{self.base_url}/api/user/{username}"

        payload = {

            "status": "active"

        }

        response = requests.put(

            url,

            headers=self.headers(),

            json=payload,

            timeout=30

        )

        response.raise_for_status()

        return response.json()


# ==========================================================
# Disable User
# ==========================================================

    def disable_service(
        self,
        # ==========================================================
# Users List
# ==========================================================

    def get_users(self):

        url = f"{self.base_url}/api/users"

        response = requests.get(
            url,
            headers=self.headers(),
            timeout=30
        )

        response.raise_for_status()

        return response.json()


# ==========================================================
# System Stats
# ==========================================================

    def get_system_stats(self):

        url = f"{self.base_url}/api/system"

        response = requests.get(
            url,
            headers=self.headers(),
            timeout=30
        )

        response.raise_for_status()

        return response.json()


# ==========================================================
# Get Subscription Link
# ==========================================================

    def get_subscription(self, username):

        user = self.get_user(username)

        return user.get("subscription_url")


# ==========================================================
# Check User Exists
# ==========================================================

    def user_exists(self, username):

        try:

            self.get_user(username)

            return True

        except Exception:

            return False


# ==========================================================
# Get User Usage
# ==========================================================

    def get_usage(self, username):

        user = self.get_user(username)

        return {

            "used": user.get("used_traffic", 0),

            "limit": user.get("data_limit", 0),

            "status": user.get("status", "unknown"),

            "expire": user.get("expire", 0)

            }
        # ==========================================================
# Extra Functions
# Part 5/5
# ==========================================================

    def refresh_token(self):
        """
        دریافت مجدد توکن در صورت منقضی شدن
        """

        global TOKEN

        TOKEN = None

        self.token = self.login()

        return self.token


# ==========================================================
# Connection Test
# ==========================================================

    def ping(self):

        try:

            url = f"{self.base_url}/api/system"

            response = requests.get(
                url,
                headers=self.headers(),
                timeout=10
            )

            return response.status_code == 200

        except Exception:

            return False


# ==========================================================
# Create Username
# ==========================================================

    def generate_username(self, user_id):

        import random
        import string

        rand = "".join(
            random.choice(
                string.ascii_lowercase + string.digits
            )
            for _ in range(6)
        )

        return f"z{user_id}{rand}"


# ==========================================================
# Close Session
# ==========================================================

    def close(self):
        pass


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    panel = Marzban()

    if panel.ping():

        print("✅ Marzban Connected")

    else:

        print("❌ Marzban Connection Failed")
