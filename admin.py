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
# پنل مدیریت حرفه‌ای
# =========================

def admin_panel():


    keyboard = [


        [
            InlineKeyboardButton(
                "📊 داشبورد",
                callback_data="admin_stats"
            )
        ],


        [
            InlineKeyboardButton(
                "📋 سفارش‌ها",
                callback_data="admin_orders"
            ),

            InlineKeyboardButton(
                "👥 کاربران",
                callback_data="admin_users"
            )
        ],


        [
            InlineKeyboardButton(
                "🌐 سرویس‌ها",
                callback_data="admin_services"
            ),

            InlineKeyboardButton(
                "💳 پرداخت‌ها",
                callback_data="admin_payments"
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
                "🖥 مدیریت پنل‌ها",
                callback_data="admin_panels"
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
# دکمه برگشت ادمین
# =========================

def back_admin():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="admin_back"
            )
        ]

    ])
    # =========================
# دکمه تایید رسید پرداخت
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
# داشبورد مدیریت
# =========================

def admin_dashboard(
    users=0,
    sales=0,
    active=0,
    pending=0
):

    text = f"""
👑 داشبورد Zeus Shop VPN

━━━━━━━━━━━━━━

👥 کاربران:
{users}

💰 فروش کل:
{sales:,} تومان

🟢 سرویس فعال:
{active}

⏳ پرداخت در انتظار:
{pending}

━━━━━━━━━━━━━━
"""


    keyboard = [

        [
            InlineKeyboardButton(
                "🔄 بروزرسانی",
                callback_data="admin_stats"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="admin_back"
            )
        ]

    ]


    return (
        text,
        InlineKeyboardMarkup(keyboard)
    )



# =========================
# منوی کاربران
# =========================

def users_menu():


    keyboard = [


        [
            InlineKeyboardButton(
                "🔍 جستجوی کاربر",
                callback_data="search_user"
            )
        ],


        [
            InlineKeyboardButton(
                "📋 لیست کاربران",
                callback_data="users_list"
            )
        ],


        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# منوی سفارش‌ها
# =========================

def orders_menu():


    keyboard = [

        [
            InlineKeyboardButton(
                "⏳ سفارش‌های جدید",
                callback_data="pending_orders"
            )
        ],

        [
            InlineKeyboardButton(
                "📦 همه سفارش‌ها",
                callback_data="all_orders"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )
    # =========================
# مدیریت پنل‌ها
# =========================

def panels_menu():


    keyboard = [

        [
            InlineKeyboardButton(
                "🟢 Marzban",
                callback_data="panel_marzban"
            )
        ],

        [
            InlineKeyboardButton(
                "⚡ 3x-ui",
                callback_data="panel_3xui"
            )
        ],

        [
            InlineKeyboardButton(
                "➕ افزودن پنل",
                callback_data="add_panel"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# مدیریت سرویس‌ها
# =========================

def services_menu():


    keyboard = [

        [
            InlineKeyboardButton(
                "🟢 سرویس‌های فعال",
                callback_data="active_services"
            )
        ],

        [
            InlineKeyboardButton(
                "⏳ سرویس‌های منقضی",
                callback_data="expired_services"
            )
        ],

        [
            InlineKeyboardButton(
                "🔄 تمدید سرویس",
                callback_data="renew_service"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# مدیریت پرداخت‌ها
# =========================

def payments_menu():


    keyboard = [

        [
            InlineKeyboardButton(
                "⏳ پرداخت‌های در انتظار",
                callback_data="pending_payments"
            )
        ],

        [
            InlineKeyboardButton(
                "✅ پرداخت‌های تایید شده",
                callback_data="approved_payments"
            )
        ],

        [
            InlineKeyboardButton(
                "❌ پرداخت‌های رد شده",
                callback_data="rejected_payments"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# تنظیمات
# =========================

def settings_menu():


    keyboard = [

        [
            InlineKeyboardButton(
                "💳 تغییر شماره کارت",
                callback_data="change_card"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 تغییر کانال",
                callback_data="change_channel"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="admin_back"
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


        # =========================
        # ورود به مرزبان
        # =========================

        if not marzban.login():

            print(
                "❌ Marzban Login Failed"
            )

            return None


        print(
            "✅ Marzban Login Success"
        )



        # =========================
        # ساخت کاربر
        # =========================

        user = marzban.create_user(

            username=None,

            data_limit=int(volume)

        )


        if not user:

            print(
                "❌ User creation failed"
            )

            return None



        username = user.get(
            "username"
        )



        if not username:

            print(
                "❌ Username not found"
            )

            return None



        print(
            f"✅ User Created: {username}"
        )



        # =========================
        # گرفتن لینک اشتراک
        # =========================

        subscription = marzban.subscription(
            username
        )


        if not subscription:

            print(
                "❌ Subscription link failed"
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
            "❌ Marzban Error:",
            e
        )


        return None
