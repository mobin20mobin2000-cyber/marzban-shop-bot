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
# دکمه رسید
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
# ساخت اشتراک مرزبان
# =========================

def create_subscription(volume):

    try:


        marzban = Marzban()



        # ورود

        login = marzban.login()


        if not login:

            print(
                "❌ ورود به مرزبان ناموفق بود"
            )

            return None



        print(
            "✅ Marzban Login OK"
        )



        # ساخت کاربر


        user = marzban.create_user(

            data_limit=int(volume)

        )



        if not user:


            print(
                "❌ ساخت کاربر مرزبان شکست خورد"
            )

            return None




        username = user.get(
            "username"
        )



        if not username:


            print(
                "❌ Username دریافت نشد"
            )

            return None




        print(
            "✅ User Created:",
            username
        )



        # گرفتن لینک اشتراک


        subscription = marzban.subscription(

            username

        )



        if not subscription:


            print(
                "❌ لینک اشتراک پیدا نشد"
            )

            return None




        # اگر لینک نسبی بود


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

            "❌ Marzban Exception:",

            e

        )


        return None
