from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from marzban import Marzban



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
# ساخت سرویس در Marzban
# =========================

def create_subscription(volume):

    marzban = Marzban()


    user = marzban.create_user(

        username=None,

        data_limit=volume

    )


    if not user:

        return None



    return {

        "username": user.get(
            "username"
        ),

        "subscription": user.get(
            "subscription_url"
        )

    }
