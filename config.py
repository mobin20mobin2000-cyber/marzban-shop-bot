# =========================
# config.py
# Zeus Shop VPN
# =========================

import os


# =========================
# Telegram
# =========================

BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)

ADMIN_ID = int(
    os.getenv(
        "ADMIN_ID",
        0
    )
)



# =========================
# Marzban
# =========================

MARZBAN_URL = os.getenv(
    "MARZBAN_URL"
)

MARZBAN_USERNAME = os.getenv(
    "MARZBAN_USERNAME"
)

MARZBAN_PASSWORD = os.getenv(
    "MARZBAN_PASSWORD"
)



# =========================
# بررسی تنظیمات
# =========================

if not BOT_TOKEN:
    print("❌ BOT_TOKEN تنظیم نشده")


if not ADMIN_ID:
    print("❌ ADMIN_ID تنظیم نشده")


if not MARZBAN_URL:
    print("❌ MARZBAN_URL تنظیم نشده")


if not MARZBAN_USERNAME:
    print("❌ MARZBAN_USERNAME تنظیم نشده")


if not MARZBAN_PASSWORD:
    print("❌ MARZBAN_PASSWORD تنظیم نشده")
