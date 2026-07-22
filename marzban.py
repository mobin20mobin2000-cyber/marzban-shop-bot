# ساخت کاربر جدید
def create_user(
    self,
    username=None,
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

        "expire": 0,

        "data_limit": data_limit

    }

    response = requests.post(

        url,

        json=payload,

        headers=self.headers(),

        timeout=20

    )

    print(response.text)

    if response.status_code in [200, 201]:

        return response.json()

    return None
