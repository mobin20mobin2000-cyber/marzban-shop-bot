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
                "👥 کاربران",
                callback_data="admin_users"
            ),

            InlineKeyboardButton(
                "📋 سفارش‌ها",
                callback_data="admin_orders"
            )

        ],


        [

            InlineKeyboardButton(
                "💳 پرداخت‌ها",
                callback_data="admin_payments"
            ),

            InlineKeyboardButton(
                "🌐 سرویس‌ها",
                callback_data="admin_services"
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
                "🎟 کد تخفیف",
                callback_data="coupon_menu"
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
# داشبورد مدیریت
# =========================


def admin_dashboard():


    stats = get_stats()



    text = f"""

👑 داشبورد Zeus Shop VPN

━━━━━━━━━━━━

👥 کاربران:

{stats['users']}


🆕 کاربران امروز:

{stats['today_users']}


🛒 فروش موفق:

{stats['sales']}


💰 درآمد:

{stats['income']:,} تومان


🌐 سرویس‌ها:

{stats['subscriptions']}


⏳ پرداخت منتظر:

{stats['pending']}

━━━━━━━━━━━━

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

                "🔍 جستجو کاربر",

                callback_data="search_user"

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
# منوی پرداخت‌ها
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
# منوی مدیریت پنل‌ها
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
# منوی کد تخفیف
# =========================


def coupon_menu():


    keyboard = [


        [

            InlineKeyboardButton(

                "➕ ساخت کد تخفیف",

                callback_data="create_coupon"

            )

        ],


        [

            InlineKeyboardButton(

                "📋 لیست کدها",

                callback_data="coupon_list"

            )

        ],


        [

            InlineKeyboardButton(

                "🗑 حذف کد",

                callback_data="delete_coupon"

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
# منوی پیام همگانی
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


        from marzban import Marzban



        marzban = Marzban()



        if not marzban.login():


            print(
                "❌ Marzban Login Failed"
            )

            return None





        user = marzban.create_user(

            username=None,

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





    except Exception as e:


        print(

            "Marzban Error:",

            e

        )


        return None
        # =========================
# اطلاعات پنل‌ها
# =========================


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





# =========================
# اطلاعات Marzban
# =========================


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





# =========================
# صفحه اصلی ادمین
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

                "👥 کاربران",

                callback_data="admin_users"

            ),


            InlineKeyboardButton(

                "📋 سفارش‌ها",

                callback_data="admin_orders"

            )

        ],


        [

            InlineKeyboardButton(

                "💳 پرداخت‌ها",

                callback_data="admin_payments"

            ),


            InlineKeyboardButton(

                "🌐 سرویس‌ها",

                callback_data="admin_services"

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

                "🎟 کد تخفیف",

                callback_data="coupon_menu"

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
# تست اتصال Marzban
# =========================


def test_marzban():


    try:


        from marzban import Marzban



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





# =========================
# پایان admin.py
# Zeus Shop VPN PRO
# =========================
