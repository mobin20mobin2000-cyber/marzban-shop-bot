# =========================
# config.py
# Zeus Shop VPN
# =========================

import os

# =========================
# Telegram
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

ADMIN_ID = int(
    os.getenv("ADMIN_ID", "0")
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
