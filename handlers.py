# =========================
# handlers.py
# Zeus Shop VPN
# نسخه هماهنگ با database.py
# =========================


from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from telegram.ext import (
    ContextTypes
)


from config import ADMIN_ID


from texts import (
    WELCOME_TEXT,
    SUPPORT_TEXT,
    MY_SERVICE_TEXT
)


from plans import (
    PLANS,
    get_plan
)


from payment import (
    get_payment_text
)


from database import (
    add_user,
    create_order,
    get_subscription,
    save_subscription,
    get_order,
    approve_payment as db_approve_payment,
    reject_payment as db_reject_payment,
    pending_orders,
    users_count,
    total_sales
)


from admin_panel import admin_panel


from marzban import Marzban



# =========================
# منوی کاربر
# =========================

def user_menu():


    keyboard = [


        [
            InlineKeyboardButton(
                "🛒 خرید اشتراک",
                callback_data="buy"
            )
        ],


        [
            InlineKeyboardButton(
                "📦 سرویس من",
                callback_data="my_service"
            )
        ],


        [
            InlineKeyboardButton(
                "💬 پشتیبانی",
                callback_data="support"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )




# =========================
# منوی پلن ها
# =========================

def plans_keyboard():


    keyboard = []


    for key, plan in PLANS.items():


        keyboard.append(

            [

                InlineKeyboardButton(

                    f"📦 {plan['name']} | 💰 {plan['price']:,} تومان",

                    callback_data=f"plan_{key}"

                )

            ]

        )


    return InlineKeyboardMarkup(
        keyboard
    )




# =========================
# شروع ربات
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    user = update.effective_user


    add_user(

        user.id,

        user.username

    )


    if user.id == ADMIN_ID:


        await update.message.reply_text(

            "👑 پنل مدیریت Zeus Shop VPN",

            reply_markup=admin_panel()

        )

        return



    await update.message.reply_text(

        WELCOME_TEXT,

        reply_markup=user_menu()

    )
    # =========================
# مدیریت دکمه‌ها
# =========================

async def button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id

    data = query.data



    # =====================
    # خرید اشتراک
    # =====================

    if data == "buy":


        await query.message.reply_text(

            "📦 پلن مورد نظر را انتخاب کنید:",

            reply_markup=plans_keyboard()

        )


        return




    # =====================
    # انتخاب پلن
    # =====================

    if data.startswith("plan_"):


        plan_id = data.replace(
            "plan_",
            ""
        )


        plan = get_plan(plan_id)



        if not plan:


            await query.message.reply_text(

                "❌ پلن پیدا نشد."

            )

            return




        # ساخت سفارش در دیتابیس

        order_id = create_order(

            telegram_id=user_id,

            plan=plan["name"],

            volume=plan["volume"],

            days=30,

            price=plan["price"]

        )



        await query.message.reply_text(

            get_payment_text(

                order_id

            )

            +

            f"""



📦 پلن انتخابی:

{plan['name']}



💰 مبلغ:

{plan['price']:,} تومان



بعد از پرداخت، عکس رسید را ارسال کنید.

"""

        )


        return






    # =====================
    # سرویس من
    # =====================

    if data == "my_service":


        service = get_subscription(

            user_id

        )



        if not service:


            await query.message.reply_text(

                "❌ هنوز سرویس فعالی ندارید."

            )

            return



        await query.message.reply_text(

            f"""

🔐 سرویس من


👤 نام کاربری مرزبان:

{service[3]}



🔗 لینک اتصال:

{service[4]}



📅 انقضا:

{service[5]}



"""

        )


        return





    # =====================
    # پشتیبانی
    # =====================

    if data == "support":


        await query.message.reply_text(

            SUPPORT_TEXT

        )


        return
