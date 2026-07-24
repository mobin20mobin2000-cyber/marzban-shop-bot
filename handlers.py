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

            "📦 لطفاً پلن مورد نظر را انتخاب کنید:",

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


        if plan is None:


            await query.message.reply_text(

                "❌ پلن پیدا نشد."

            )

            return



        order_id = create_order(

            user_id,

            plan["name"],

            plan["volume"],

            plan["days"],

            plan["price"]

        )



        await query.message.reply_text(

            get_payment_text(order_id)

            +

            f"""

━━━━━━━━━━━━━━

📦 پلن انتخابی:

{plan['name']}


💾 حجم:

{plan['volume']} GB


⏳ مدت:

{plan['days']} روز


💰 مبلغ:

{plan['price']:,} تومان


🧾 شماره سفارش:

{order_id}


━━━━━━━━━━━━━━


📸 بعد از پرداخت، عکس رسید را ارسال کنید.

"""

        )

        return



# =========================
# نمایش سرویس من
# =========================

async def show_service(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id


    service = get_subscription(

        user_id

    )


    if service is None:


        await query.message.reply_text(

            "❌ هنوز سرویس فعالی ندارید."

        )

        return



    await query.message.reply_text(

f"""
🔐 سرویس من

━━━━━━━━━━━━━━

👤 نام کاربری مرزبان:

{service["marzban_username"]}


🔗 لینک اشتراک:

{service["subscription_url"]}


📅 تاریخ انقضا:

{service["expire_date"] or "نامشخص"}

━━━━━━━━━━━━━━
"""

    )



# =========================
# پشتیبانی
# =========================

async def show_support(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        SUPPORT_TEXT

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

            "📦 لطفاً پلن مورد نظر را انتخاب کنید:",

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



        if plan is None:


            await query.message.reply_text(

                "❌ پلن پیدا نشد."

            )

            return



        order_id = create_order(

            user_id,

            plan["name"],

            plan["volume"],

            plan["days"],

            plan["price"]

        )



        await query.message.reply_text(

            get_payment_text(order_id)

            +

            f"""



📦 پلن انتخابی:

{plan['name']}


💾 حجم:

{plan['volume']} گیگ


⏳ مدت:

{plan['days']} روز


💰 مبلغ:

{plan['price']:,} تومان


🧾 شماره سفارش:

{order_id}



بعد از پرداخت، عکس رسید را ارسال کنید.

"""

        )

        return




# =========================
# نمایش سرویس من
# =========================

async def show_service(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id



    service = get_subscription(

        user_id

    )



    if service is None:


        await query.message.reply_text(

            "❌ هنوز سرویس فعالی ندارید."

        )

        return



    await query.message.reply_text(

f"""
🔐 سرویس من

━━━━━━━━━━━━━━

👤 نام کاربری:

{service["marzban_username"]}


🔗 لینک اشتراک:

{service["subscription_url"]}


📅 انقضا:

{service["expire_date"] or "نامشخص"}

━━━━━━━━━━━━━━
"""

    )





# =========================
# پشتیبانی
# =========================

async def show_support(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()



    await query.message.reply_text(

        SUPPORT_TEXT

    )
    # =========================
# دریافت رسید پرداخت
# =========================

async def receipt_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id



    order = last_order(

        user_id

    )



    if order is None:


        await update.message.reply_text(

            "❌ ابتدا یک سفارش ثبت کنید."

        )

        return



    photo = update.message.photo[-1]



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,


        caption=f"""
📥 رسید پرداخت جدید

━━━━━━━━━━━━━━

👤 کاربر:

{user_id}


🧾 شماره سفارش:

{order["id"]}


📦 پلن:

{order["plan"]}


💾 حجم:

{order["volume"]} گیگ


⏳ مدت:

{order["days"]} روز


💰 مبلغ:

{order["price"]:,} تومان

━━━━━━━━━━━━━━
""",


        reply_markup=admin_buttons(

            user_id

        )

    )



    await update.message.reply_text(

"""
✅ رسید شما دریافت شد.

⏳ منتظر تایید مدیریت باشید.
"""

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



    user_id = int(

        query.data.replace(

            "approve_",

            ""

        )

    )



    order = last_order(

        user_id

    )



    if order is None:


        await query.message.reply_text(

            "❌ سفارش پیدا نشد."

        )

        return



    # ساخت سرویس مرزبان

    result = create_subscription(

        order["volume"]

    )



    if result is None:


        await query.message.reply_text(

            "❌ خطا در ساخت سرویس مرزبان."

        )

        return



    # ذخیره اشتراک

    save_subscription(

        user_id,

        order["id"],

        result["username"],

        result["subscription"],

        None

    )



    # تایید سفارش

    db_approve_payment(

        order["id"]

    )



    # ارسال سرویس برای کاربر

    await context.bot.send_message(

        chat_id=user_id,

        text=f"""
🎉 پرداخت شما تایید شد.

━━━━━━━━━━━━━━

📦 سرویس شما آماده است.


👤 نام کاربری:

{result["username"]}


🔗 لینک اشتراک:

{result["subscription"]}


━━━━━━━━━━━━━━

با تشکر از خرید شما ❤️
"""

    )



    await query.message.reply_text(

        "✅ سرویس ساخته شد و برای کاربر ارسال گردید."

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



    if query.from_user.id != ADMIN_ID:

        return



    user_id = int(

        query.data.replace(

            "reject_",

            ""

        )

    )



    order = last_order(

        user_id

    )



    if order:


        db_reject_payment(

            order["id"]

        )


        await context.bot.send_message(

            chat_id=user_id,

            text="""
❌ پرداخت شما رد شد.

در صورت اشتباه بودن، دوباره رسید ارسال کنید.
"""

        )



    await query.message.reply_text(

        "✅ پرداخت رد شد."

    )





# =========================
# ثبت Handler ها
# =========================

def register_handlers(app):


    from telegram.ext import (

        CommandHandler,

        CallbackQueryHandler,

        MessageHandler,

        filters

    )



    app.add_handler(

        CommandHandler(

            "start",

            start

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            button,

            pattern="^(buy|plan_)"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_service,

            pattern="^my_service$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            show_support,

            pattern="^support$"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            approve_payment,

            pattern="^approve_"

        )

    )



    app.add_handler(

        CallbackQueryHandler(

            reject_payment,

            pattern="^reject_"

        )

    )



    # دریافت عکس رسید

    app.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_photo

        )

    )
