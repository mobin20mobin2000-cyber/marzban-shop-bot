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


    # دریافت لینک اشتراک
    def subscription(self, username):

        user = self.get_user(username)

        if not user:
            return None

        sub = user.get("subscription_url")

        if not sub:
            return None

        if sub.startswith("http"):
            return sub

        return self.url + sub


    # دریافت لینک VLESS
    def vless_link(self, username):

        user = self.get_user(username)

        if not user:
            return None

        links = user.get("links", [])

        if not links:
            return None

        return links[0]


    # تغییر حجم کاربر
    def update_data_limit(self, username, data_limit):

        if not self.token:
            self.login()

        url = f"{self.url}/api/user/{username}"

        payload = {
            "data_limit": data_limit
        }

        response = requests.put(
            url,
            json=payload,
            headers=self.headers(),
            timeout=20
        )

        return response.status_code == 200
