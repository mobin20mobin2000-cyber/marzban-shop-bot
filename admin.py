# =========================
# admin.py
# Zeus Shop VPN PRO
# =========================


from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from config import (
    MARZBAN_URL
)


from database import (
    get_stats,
    pending_orders,
    subscriptions_count
)


from marzban import Marzban



# =========================
# پنل اصلی مدیریت
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


def admin_dashboard():


    stats = get_stats()



    text = f"""
👑 داشبورد Zeus Shop VPN

━━━━━━━━━━━━━━

👥 تعداد کاربران:
{stats['users']}

💰 فروش تایید شده:
{stats['income']:,} تومان

🛒 تعداد فروش:
{stats['sales']}

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

        InlineKeyboardMarkup(
            keyboard
        )

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
                "🔍 جستجو کاربر",
                callback_data="search_user"
            )

        ],


        [

            InlineKeyboardButton(
                "🚫 مسدود کردن",
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
                "✅ پرداخت تایید شده",
                callback_data="approved_payments"
            )

        ],


        [

            InlineKeyboardButton(
                "❌ پرداخت رد شده",
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
                "🔗 تنظیم مرزبان",
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
# ساخت سرویس مرزبان
# =========================


def create_subscription(
    volume
):

    try:


        marzban = Marzban()



        # ورود به پنل

        login = marzban.login()


        if not login:


            print(
                "❌ Marzban login failed"
            )

            return None




        print(
            "✅ Marzban login success"
        )



        # ساخت کاربر


        user = marzban.create_user(

            username=None,

            data_limit=int(volume)

        )



        if not user:


            print(
                "❌ Create user failed"
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
            "✅ Created:",
            username
        )



        # دریافت لینک اشتراک


        subscription = marzban.subscription(

            username

        )



        if not subscription:


            print(
                "❌ Subscription empty"
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
# اطلاعات پنل
# =========================


def panel_info():


    return """

🖥 اطلاعات پنل‌ها

━━━━━━━━━━━━━━

🟢 Marzban:
فعال

⚡ 3x-ui:
غیرفعال

━━━━━━━━━━━━━━

"""





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
