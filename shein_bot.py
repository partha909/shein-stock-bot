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
        "name": "Drop Shoulder Graphic Sweatshirt",
        "url": "https://www.sheinindia.in/shein-shein-drop-shoulder-graphic-front-print-crew-sweatshirt/p/443380970_greymelange"
    },
    {
        "name": "Street Cargo Jeans",
        "url": "https://www.sheinindia.in/shein-shein-street-full-length-straight-cargo-jeans-with-pockets/p/443320446_blue"
    },
    {
        "name": "Typographic Print T-Shirt",
        "url": "https://www.sheinindia.in/shein-shein-drop-shoulder-typographic-chest-print-relaxed-fit-tshirt/p/443323021_black"
    },
    {
        "name": "Cargo Track Pants",
        "url": "https://www.sheinindia.in/shein-shein-activewear-side-cargo-flap-pockets-straight-trackpants/p/443317440_grey"
    },
    {
        "name": "Low Rise Track Shorts",
        "url": "https://www.sheinindia.in/shein-shein-elasticated-drawstring-waist-low-rise-track-shorts/p/443332092_dkgrey"
    },
    {
        "name": "Checks Cuban Collar Shirt",
        "url": "https://www.sheinindia.in/shein-shein-checks-print-cuban-collar-short-sleeve-knitted-shirt/p/443317629_green"
    },
    {
        "name": "Graphic Placement T-Shirt",
        "url": "https://www.sheinindia.in/shein-shein-short-sleeves-graphic-placement-print-crew-tshirt/p/443329853_green"
    },
    {
        "name": "Floral Cuban Collar Shirt",
        "url": "https://www.sheinindia.in/shein-shein-cuban-collar-short-sleeves-floral-print-shirt/p/443321661_grey"
    },
    {
        "name": "Distressed Black Jeans",
        "url": "https://www.sheinindia.in/shein-shein-full-length-fixed-waist-mid-wash-distressed-jeans/p/443330229_black"
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
