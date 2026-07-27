# ==========================================================
# Zeus Shop VPN PRO
# admin.py
# Part 1/4
# ==========================================================

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from config import MARZBAN_URL


from database import (
    get_stats
)


# ==========================================================
# دکمه ساز
# ==========================================================

def button(
    text,
    callback
):

    return InlineKeyboardButton(
        text,
        callback_data=callback
    )


# ==========================================================
# پنل اصلی ادمین
# ==========================================================

def admin_panel():

    keyboard = [

        [
            button(
                "📊 داشبورد",
                "admin_stats"
            )
        ],

        [
            button(
                "👥 کاربران",
                "admin_users"
            ),

            button(
                "📋 سفارش‌ها",
                "admin_orders"
            )
        ],

        [
            button(
                "💳 پرداخت‌ها",
                "admin_payments"
            ),

            button(
                "🌐 سرویس‌ها",
                "admin_services"
            )
        ],

        [
            button(
                "🖥 پنل‌ها",
                "admin_panels"
            )
        ],

        [
            button(
                "🎟 کد تخفیف",
                "coupon_menu"
            )
        ],

        [
            button(
                "📢 پیام همگانی",
                "broadcast"
            )
        ],

        [
            button(
                "⚙️ تنظیمات",
                "settings"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# برگشت ادمین
# ==========================================================

def back_admin():

    return InlineKeyboardMarkup(
        [

            [

                button(
                    "🔙 بازگشت",
                    "admin_back"
                )

            ]

        ]
    )



# ==========================================================
# داشبورد
# ==========================================================

def admin_dashboard():

    stats = get_stats()


    text = f"""

👑 Zeus Shop VPN PRO

📊 داشبورد مدیریت

━━━━━━━━━━━━

👥 کاربران:
{stats['users']}

🆕 امروز:
{stats['today_users']}

🛒 فروش موفق:
{stats['sales']}

💰 درآمد:
{stats['income']:,} تومان

🌐 سرویس فعال:
{stats['subscriptions']}

⏳ پرداخت انتظار:
{stats['pending']}

━━━━━━━━━━━━
"""


    keyboard = [

        [
            button(
                "🔄 بروزرسانی",
                "admin_stats"
            )
        ],

        [
            button(
                "🔙 بازگشت",
                "admin_back"
            )
        ]

    ]


    return (
        text,
        InlineKeyboardMarkup(
            keyboard
        )
    )



# ==========================================================
# پایان Part 1
# ==========================================================
# ==========================================================
# Users Menu
# ==========================================================


def users_menu():

    keyboard = [

        [
            button(
                "📋 لیست کاربران",
                "users_list"
            )
        ],

        [
            button(
                "🔍 جستجوی کاربر",
                "search_user"
            )
        ],

        [
            button(
                "🔙 بازگشت",
                "admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# Orders Menu
# ==========================================================


def orders_menu():

    keyboard = [

        [
            button(
                "⏳ سفارش‌های در انتظار",
                "pending_orders"
            )
        ],

        [
            button(
                "📦 همه سفارش‌ها",
                "all_orders"
            )
        ],

        [
            button(
                "🗑 حذف سفارش",
                "delete_order"
            )
        ],

        [
            button(
                "🔙 بازگشت",
                "admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# Payments Menu
# ==========================================================


def payments_menu():

    keyboard = [

        [
            button(
                "⏳ پرداخت‌های در انتظار",
                "pending_payments"
            )
        ],

        [
            button(
                "✅ پرداخت تایید شده",
                "approved_payments"
            )
        ],

        [
            button(
                "❌ پرداخت رد شده",
                "rejected_payments"
            )
        ],

        [
            button(
                "🔙 بازگشت",
                "admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# Services Menu
# ==========================================================


def services_menu():

    keyboard = [

        [
            button(
                "🟢 سرویس‌های فعال",
                "active_services"
            )
        ],

        [
            button(
                "⏳ سرویس‌های منقضی",
                "expired_services"
            )
        ],

        [
            button(
                "🔄 تمدید سرویس",
                "renew_service"
            )
        ],

        [
            button(
                "🗑 حذف سرویس",
                "delete_service"
            )
        ],

        [
            button(
                "🔙 بازگشت",
                "admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# پایان Part 2
# ==========================================================
# ==========================================================
# Panels Menu
# ==========================================================


def panels_menu():

    keyboard = [

        [
            button(
                "🟢 Marzban",
                "panel_marzban"
            )
        ],

        [
            button(
                "⚡ 3x-ui",
                "panel_3xui"
            )
        ],

        [
            button(
                "➕ افزودن پنل",
                "add_panel"
            )
        ],

        [
            button(
                "🔙 بازگشت",
                "admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# Settings Menu
# ==========================================================


def settings_menu():

    keyboard = [

        [
            button(
                "💳 تغییر شماره کارت",
                "change_card"
            )
        ],

        [
            button(
                "📢 تغییر کانال",
                "change_channel"
            )
        ],

        [
            button(
                "🔗 تنظیم Marzban",
                "marzban_settings"
            )
        ],

        [
            button(
                "🔙 بازگشت",
                "admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# Coupon Menu
# ==========================================================


def coupon_menu():

    keyboard = [

        [
            button(
                "➕ ساخت کد تخفیف",
                "create_coupon"
            )
        ],

        [
            button(
                "📋 لیست کدها",
                "coupon_list"
            )
        ],

        [
            button(
                "🗑 حذف کد",
                "delete_coupon"
            )
        ],

        [
            button(
                "🔙 بازگشت",
                "admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# Broadcast Menu
# ==========================================================


def broadcast_menu():

    keyboard = [

        [
            button(
                "📢 ارسال پیام",
                "send_broadcast"
            )
        ],

        [
            button(
                "🔙 بازگشت",
                "admin_back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# Marzban Create Subscription
# ==========================================================


def create_subscription(volume):

    try:

        from marzban import Marzban


        marzban = Marzban()


        if not marzban.login():

            print(
                "❌ Marzban Login Failed"
            )

            return None



        user = marzban.create_user(

            data_limit=int(volume)

        )


        if not user:

            return None



        username = user.get(
            "username"
        )


        if not username:

            return None



        subscription = marzban.subscription(
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

            "username":
                username,


            "subscription":
                subscription

        }



    except Exception as error:

        print(
            "CREATE SUB ERROR:",
            error
        )

        return None



# ==========================================================
# Panel Information
# ==========================================================


def panel_info():

    return """

🖥 وضعیت پنل‌ها

━━━━━━━━━━━━

🟢 Marzban:
فعال ✅


⚡ 3x-ui:
آماده اتصال ⏳


━━━━━━━━━━━━

"""



# ==========================================================
# Marzban Information
# ==========================================================


def marzban_info():

    return f"""

🔗 اطلاعات Marzban

━━━━━━━━━━━━

🌐 آدرس:

{MARZBAN_URL}


🟢 وضعیت:

فعال ✅


━━━━━━━━━━━━

"""


# ==========================================================
# پایان Part 3
# ==========================================================
# ==========================================================
# Admin Home
# ==========================================================


def admin_home():

    keyboard = [

        [
            button(
                "📊 داشبورد",
                "admin_stats"
            )
        ],

        [
            button(
                "👥 کاربران",
                "admin_users"
            ),

            button(
                "📋 سفارش‌ها",
                "admin_orders"
            )
        ],

        [
            button(
                "💳 پرداخت‌ها",
                "admin_payments"
            ),

            button(
                "🌐 سرویس‌ها",
                "admin_services"
            )
        ],

        [
            button(
                "🖥 پنل‌ها",
                "admin_panels"
            )
        ],

        [
            button(
                "🎟 کد تخفیف",
                "coupon_menu"
            )
        ],

        [
            button(
                "📢 پیام همگانی",
                "broadcast"
            )
        ],

        [
            button(
                "⚙️ تنظیمات",
                "settings"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# ==========================================================
# Test Marzban Connection
# ==========================================================


def test_marzban():

    try:

        from marzban import Marzban


        marzban = Marzban()


        if marzban.login():

            return True


        return False



    except Exception as error:

        print(
            "MARZBAN TEST ERROR:",
            error
        )


        return False



# ==========================================================
# پایان admin.py
# Zeus Shop VPN PRO
# ==========================================================
