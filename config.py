# ==========================================================
# Zeus Shop VPN PRO
# config.py
# ==========================================================

import os


# ==========================================================
# Telegram
# ==========================================================

BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    ""
)


ADMIN_ID = int(
    os.getenv(
        "ADMIN_ID",
        "0"
    )
)


# ==========================================================
# Channel
# ==========================================================

CHANNEL_USERNAME = os.getenv(
    "CHANNEL_USERNAME",
    "Vpn1_v2rayNG"
)


CHANNEL_ID = os.getenv(
    "CHANNEL_ID",
    "@Vpn1_v2rayNG"
)


CHANNEL_LINK = os.getenv(
    "CHANNEL_LINK",
    "https://t.me/Vpn1_v2rayNG"
)


# ==========================================================
# Payment
# ==========================================================

CARD_NUMBER = os.getenv(
    "CARD_NUMBER",
    "0000-0000-0000-0000"
)


CARD_OWNER = os.getenv(
    "CARD_OWNER",
    "Zeus Shop"
)


# ==========================================================
# Marzban
# ==========================================================

MARZBAN_URL = os.getenv(
    "MARZBAN_URL",
    ""
)


MARZBAN_USERNAME = os.getenv(
    "MARZBAN_USERNAME",
    ""
)


MARZBAN_PASSWORD = os.getenv(
    "MARZBAN_PASSWORD",
    ""
)


# ==========================================================
# Plans
# ==========================================================

PLANS = {

    "plan_30": {

        "name": "یک ماهه",

        "days": 30,

        "volume": 50,

        "price": 50000

    },


    "plan_60": {

        "name": "دو ماهه",

        "days": 60,

        "volume": 100,

        "price": 90000

    },


    "plan_90": {

        "name": "سه ماهه",

        "days": 90,

        "volume": 200,

        "price": 150000

    }

}


# ==========================================================
# Config Check
# ==========================================================

def check_config():

    errors = []


    if not BOT_TOKEN:

        errors.append(
            "BOT_TOKEN"
        )


    if not ADMIN_ID:

        errors.append(
            "ADMIN_ID"
        )


    if not MARZBAN_URL:

        errors.append(
            "MARZBAN_URL"
        )


    if not MARZBAN_USERNAME:

        errors.append(
            "MARZBAN_USERNAME"
        )


    if not MARZBAN_PASSWORD:

        errors.append(
            "MARZBAN_PASSWORD"
        )


    if errors:

        print(
            "❌ تنظیمات ناقص است:"
        )


        for item in errors:

            print(
                f" - {item}"
            )


        return False


    print(
        "✅ Config loaded successfully"
    )


    return True
