from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from marzban import Marzban

from config import MARZBAN_URL





# =========================
# دکمه های تایید رسید
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


    return InlineKeyboardMarkup(keyboard)





# =========================
# ساخت اشتراک Marzban
# =========================

def create_subscription(volume):

    marzban = Marzban()


    user = marzban.create_user(

        username=None,

        data_limit=volume

    )



    if not user:

        return None




    subscription = user.get(
        "subscription_url"
    )



    # تبدیل مسیر /sub به لینک کامل

    if subscription and subscription.startswith("/"):

        subscription = (

            MARZBAN_URL.rstrip("/")

            +

            subscription

        )



    return {

        "username": user.get(
            "username"
        ),

        "subscription": subscription

    }
