# =========================
# admin.py
# Zeus Shop VPN
# =========================


from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from marzban import Marzban

from config import MARZBAN_URL



# =========================
# پنل مدیریت
# =========================

def admin_panel():

    keyboard = [

        [
            InlineKeyboardButton(
                "📋 سفارش‌ها",
                callback_data="admin_orders"
            )
        ],

        [
            InlineKeyboardButton(
                "👥 کاربران",
                callback_data="admin_users"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 آمار فروش",
                callback_data="admin_stats"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 پیام همگانی",
                callback_data="broadcast"
            )
        ],

        [
            InlineKeyboardButton(
                "⚙️ تنظیمات",
                callback_data="settings"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# تایید پرداخت
# =========================

def admin_buttons(order_id):


    keyboard = [

        [
            InlineKeyboardButton(
                "✅ تایید پرداخت",
                callback_data=f"approve_{order_id}"
            )
        ],


        [
            InlineKeyboardButton(
                "❌ رد پرداخت",
                callback_data=f"reject_{order_id}"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# ساخت اشتراک مرزبان
# =========================

def create_subscription(volume):


    marzban = Marzban()



    user = marzban.create_user(

        data_limit=volume

    )



    if not user:

        return None



    username = user.get(
        "username"
    )



    subscription = marzban.subscription(

        username

    )



    return {


        "username": username,


        "subscription": subscription


    }
