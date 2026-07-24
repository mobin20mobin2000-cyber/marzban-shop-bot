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
# =========================
# دریافت رسید پرداخت
# =========================

async def receipt_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id


    orders = pending_orders()


    user_order = None


    for order in orders:

        if order[1] == user_id:

            user_order = order

            break



    if user_order is None:


        await update.message.reply_text(

            "❌ سفارش پرداختی پیدا نشد."

        )

        return



    photo = update.message.photo[-1]



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,


        caption=f"""

📥 رسید پرداخت جدید


👤 کاربر:

{user_id}



🆔 سفارش:

{user_order[0]}



📦 پلن:

{user_order[2]}



💰 مبلغ:

{user_order[5]:,} تومان



برای تایید یا رد از پنل استفاده کنید.

"""

    )



    await update.message.reply_text(

        "✅ رسید شما ارسال شد.\n\n⏳ منتظر تایید مدیریت باشید."

    )






# =========================
# تایید پرداخت
# =========================

async def approve_payment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()



    if query.from_user.id != ADMIN_ID:

        return



    order_id = int(

        query.data.replace(

            "approve_",

            ""

        )

    )



    order = get_order(

        order_id

    )



    if not order:


        await query.message.reply_text(

            "❌ سفارش پیدا نشد."

        )

        return




    telegram_id = order[1]

    volume = order[3]




    # ساخت کاربر مرزبان

    marzban = Marzban()



    user = marzban.create_user(

        data_limit=volume

    )



    if not user:


        await query.message.reply_text(

            "❌ ساخت سرویس در مرزبان شکست خورد."

        )

        return



    username = user.get(

        "username"

    )



    subscription = marzban.subscription(

        username

    )




    # ذخیره سرویس

    save_subscription(

        telegram_id,

        order_id,

        username,

        subscription,

        None

    )



    # تغییر وضعیت سفارش

    db_approve_payment(

        order_id

    )




    await context.bot.send_message(

        chat_id=telegram_id,


        text=f"""

🎉 پرداخت شما تایید شد.


🔐 سرویس شما آماده است.


👤 نام کاربری:

{username}



🔗 لینک اتصال:

{subscription}



ممنون از اعتماد شما ❤️

"""

    )



    await query.message.reply_text(

        "✅ سرویس ساخته شد و برای مشتری ارسال شد."

    )





# =========================
# رد پرداخت
# =========================

async def reject_payment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()



    order_id = int(

        query.data.replace(

            "reject_",

            ""

        )

    )



    order = get_order(

        order_id

    )



    if order:


        db_reject_payment(

            order_id

        )


        await context.bot.send_message(

            chat_id=order[1],


            text="""

❌ پرداخت شما رد شد.


در صورت اشتباه، دوباره رسید ارسال کنید.

"""

        )



    await query.message.reply_text(

        "✅ سفارش رد شد."

    )
