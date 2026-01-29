import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ===== CONFIG =====
BOT_TOKEN = "7814761302:AAEHwqongjJ-hfYO9IZqVMIlWCMzKp6rsno"
ADMIN_ID = 8210342937
STOCK_INTERVAL = 60  # seconds
# ==================

PRODUCTS = [
    {
        "name": "Test Product",
        "url": "https://www.sheinindia.in/"
    }
]

paid_users = set()


def is_in_stock(url: str) -> bool:
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    return "out of stock" not in soup.get_text().lower()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is LIVE and running 24×7!")


async def stock_loop(context: ContextTypes.DEFAULT_TYPE):
    for p in PRODUCTS:
        try:
            if is_in_stock(p["url"]):
                for uid in paid_users:
                    await context.bot.send_message(
                        chat_id=uid,
                        text=f"🔥 STOCK ALERT\n{p['name']}\n{p['url']}"
                    )
        except Exception as e:
            print("Error:", e)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.job_queue.run_repeating(
        stock_loop,
        interval=STOCK_INTERVAL,
        first=10
    )

    print("🚀 BOT RUNNING 24×7")
    app.run_polling()


if __name__ == "__main__":
    main()
