# =========================
# config.py
# Zeus Shop VPN
# =========================

import os
import sys


# =========================
# Telegram
# =========================

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


# =========================
# Marzban
# =========================

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


# =========================
# بررسی تنظیمات
# =========================

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

        for error in errors:
            print(
                " -",
                error
            )

        sys.exit()


    print(
        "✅ Config loaded successfully"
    )


check_config()
