# ==========================================================
# Zeus Shop VPN PRO
# main.py
# ==========================================================

from telegram.ext import Application

from config import BOT_TOKEN
from database import init_db
from handlers import register_handlers


# ==========================================================
# ساخت برنامه
# ==========================================================

def build_application():

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    register_handlers(application)

    return application


# ==========================================================
# اجرای برنامه
# ==========================================================

def main():

    print("=" * 50)
    print("🚀 Zeus Shop VPN PRO")
    print("=" * 50)

    if not BOT_TOKEN:
        print("❌ BOT_TOKEN تنظیم نشده است.")
        return

    try:
        print("📂 Initializing Database...")
        init_db()

        print("🤖 Building Telegram Application...")
        application = build_application()

        print("✅ Config loaded successfully")
        print("🚀 Zeus Shop VPN Bot Started")
        print("⏳ Waiting for updates...")

        application.run_polling(
            poll_interval=1.0,
            timeout=30,
            bootstrap_retries=5,
            drop_pending_updates=True,
            allowed_updates=None,
            close_loop=False,
        )

    except KeyboardInterrupt:
        print("🛑 Bot stopped by user.")

    except Exception as error:
        print(f"❌ Fatal Error: {error}")
        raise


# ==========================================================
# Start
# ==========================================================

if __name__ == "__main__":
    main()
