# =========================
# admin.py
# Zeus Shop VPN
# =========================


from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from marzban import Marzban

from config import (
    MARZBAN_URL,
    MARZBAN_USERNAME,
    MARZBAN_PASSWORD
)



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


    return InlineKeyboardMarkup(keyboard)



# =========================
# دکمه رسید پرداخت
# =========================

def admin_buttons(user_id):

    keyboard = [

        [
            InlineKeyboardButton(
                "✅ تایید پرداخت",
                callback_data=f"approve_{user_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "❌ رد پرداخت",
                callback_data=f"reject_{user_id}"
            )
        ]

    ]


    return InlineKeyboardMarkup(keyboard)




# =========================
# ساخت سرویس مرزبان
# =========================

def create_subscription(volume):

    try:

        marzban = Marzban(

            MARZBAN_URL,

            MARZBAN_USERNAME,

            MARZBAN_PASSWORD

        )


        user = marzban.create_user(

            data_limit=volume * 1024 * 1024 * 1024

        )


        if not user:

            return None



        username = user.get(
            "username"
        )


        if not username:

            return None



        subscription = marzban.get_subscription(

            username

        )



        if not subscription:

            return None



        if subscription.startswith("/"):

            subscription = (

                MARZBAN_URL.rstrip("/")

                +

                subscription

            )



        return {

            "username": username,

            "subscription": subscription

        }



    except Exception as e:

        print(
            "Marzban Error:",
            e
        )

        return None
