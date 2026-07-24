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
# دکمه تایید رسید
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

    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# ساخت سرویس مرزبان
# =========================

def create_subscription(volume):

    try:


        marzban = Marzban()



        # لاگین

        if not marzban.login():

            print(
                "❌ Marzban Login Failed"
            )

            return None



        print(
            "✅ Marzban Login Success"
        )



        # ساخت کاربر

        user = marzban.create_user(

            username=None,

            data_limit=int(volume)

        )



        if not user:


            print(
                "❌ Marzban Create User Failed"
            )

            return None



        username = user.get(
            "username"
        )



        if not username:


            print(
                "❌ Username Empty"
            )

            return None



        print(
            "✅ Created User:",
            username
        )



        # گرفتن لینک اشتراک

        subscription = marzban.subscription(

            username

        )



        if not subscription:


            print(
                "❌ Subscription URL Empty"
            )

            return None



        # کامل کردن لینک

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
            "❌ Marzban Error:",
            e
        )


        return None
