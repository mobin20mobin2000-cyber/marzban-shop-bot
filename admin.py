# =========================
# admin.py
# Zeus Shop VPN PRO
# =========================

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from config import MARZBAN_URL

from database import (
    get_stats
)

from marzban import Marzban



# =========================
# پنل اصلی ادمین
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
# برگشت
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


    return InlineKeyboardMarkup(
        keyboard
    )
    # =========================
# داشبورد مدیریت
# =========================

def admin_dashboard():

    stats = get_stats()


    text = f"""
👑 داشبورد Zeus Shop VPN

━━━━━━━━━━━━━━

👥 کاربران:
{stats['users']}

🛒 فروش موفق:
{stats['sales']}

💰 درآمد:
{stats['income']:,} تومان

🌐 سرویس فعال:
{stats['subscriptions']}

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
                "📋 لیست کاربران",
                callback_data="users_list"
            )
        ],

        [
            InlineKeyboardButton(
                "🔍 جستجوی کاربر",
                callback_data="search_user"
            )
        ],

        [
            InlineKeyboardButton(
                "🚫 مسدود کردن کاربر",
                callback_data="block_user"
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
                "⏳ سفارش‌های در انتظار",
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
                "🗑 حذف سفارش",
                callback_data="delete_order"
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
# منوی سرویس‌ها
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
                "🗑 حذف سرویس",
                callback_data="delete_service"
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
# تنظیمات ربات
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
                "🔗 تنظیم Marzban",
                callback_data="marzban_settings"
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
# پیام همگانی
# =========================

def broadcast_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "📢 ارسال پیام",
                callback_data="send_broadcast"
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
# ساخت سرویس Marzban
# =========================

def create_subscription(volume):

    try:

        marzban = Marzban()


        # ورود به پنل

        if not marzban.login():

            print(
                "❌ Marzban Login Failed"
            )

            return None



        print(
            "✅ Marzban Connected"
        )



        # ساخت کاربر

        user = marzban.create_user(

            username=None,

            data_limit=int(volume)

        )


        if not user:

            print(
                "❌ User Create Failed"
            )

            return None



        username = user.get(
            "username"
        )


        if not username:

            return None



        print(
            "✅ Created:",
            username
        )



        # گرفتن لینک اشتراک

        subscription = marzban.subscription(

            username

        )


        if not subscription:

            print(
                "❌ Subscription Failed"
            )

            return None



        if subscription.startswith("/"):

            subscription = (

                MARZBAN_URL.rstrip("/")

                +

                subscription

            )



        return {

            "username":
            username,

            "subscription":
            subscription

        }



    except Exception as e:

        print(
            "❌ Marzban Error:",
            e
        )

        return None
        # =========================
# اطلاعات پنل‌ها
# =========================

def panel_info():

    return """

🖥 وضعیت پنل‌ها

━━━━━━━━━━━━━━

🟢 Marzban:
فعال ✅

⚡ 3x-ui:
غیرفعال ❌

━━━━━━━━━━━━━━

"""





# =========================
# نمایش تنظیمات Marzban
# =========================

def marzban_info():

    return f"""

🔗 اطلاعات Marzban

━━━━━━━━━━━━━━

🌐 آدرس پنل:

{MARZBAN_URL}

🟢 وضعیت:
فعال

━━━━━━━━━━━━━━

"""





# =========================
# منوی مدیریت کامل
# =========================

def admin_home():

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
                "🌐 سرویس‌ها",
                callback_data="admin_services"
            )
        ],

        [
            InlineKeyboardButton(
                "💳 پرداخت‌ها",
                callback_data="admin_payments"
            )
        ],

        [
            InlineKeyboardButton(
                "🖥 پنل‌ها",
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
# تست اتصال Marzban
# =========================

def test_marzban():

    try:

        marzban = Marzban()


        if marzban.login():

            return True


        return False


    except Exception as e:

        print(
            "Marzban Test Error:",
            e
        )

        return False
