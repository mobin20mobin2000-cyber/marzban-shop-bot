# ==========================================================
# handlers.py
# Zeus Shop VPN PRO
# ==========================================================

# ---------- Imports ----------
...

# ---------- Helper Functions ----------
is_admin()
main_menu()
check_join()

# ---------- User Commands ----------
start()
buy_subscription()
my_service()
support()

# ---------- Payment ----------
receive_receipt()
create_order()
apply_coupon()

# ---------- Admin ----------
admin_start()
show_dashboard()
show_users()
show_orders()
show_payments()
show_services()
show_panels()
show_settings()

# ---------- Coupons ----------
show_coupons()
create_coupon_start()
receive_coupon()

# ---------- Broadcast ----------
show_broadcast()
start_broadcast()
send_broadcast()

# ---------- Register ----------
register_handlers()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    add_user(
        user.id,
        user.username
    )

    text = f"""
👋 سلام {user.first_name}

به Zeus Shop VPN خوش آمدید.

از منوی زیر استفاده کنید.
"""

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )
    from telegram import ReplyKeyboardMarkup, KeyboardButton

def main_menu():

    keyboard = [

        [
            KeyboardButton("🛒 خرید اشتراک")
        ],

        [
            KeyboardButton("📦 سرویس من"),
            KeyboardButton("💳 پرداخت")
        ],

        [
            KeyboardButton("🎁 کد تخفیف"),
            KeyboardButton("🆘 پشتیبانی")
        ]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
)
    app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    CommandHandler(
        "admin",
        admin_start
    )
)
