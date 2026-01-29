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
STOCK_INTERVAL = 10
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
    },
]

paid_users = set()

def is_in_stock(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    return "out of stock" not in soup.get_text().lower()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    if uid in paid_users:
        await update.message.reply_text("✅ You are a PAID member.")
    else:
        await update.message.reply_text(
            "💰 VIP ACCESS REQUIRED\n"
            "Price: ₹99\n"
            "UPI: sheinvipbot@ptyes\n\n"
            "Payment করে screenshot পাঠাও"
        )

async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    await update.message.forward(chat_id=ADMIN_ID)
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Payment proof received\nApprove: /approve {uid}"
    )
    await update.message.reply_text("✅ Screenshot received")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_ID:
        return
    uid = int(context.args[0])
    paid_users.add(uid)
    await context.bot.send_message(uid, "🎉 Payment approved!")

async def stock_loop(context: ContextTypes.DEFAULT_TYPE):
    sent = context.bot_data.setdefault("sent", set())
    for p in PRODUCTS:
        if p["url"] in sent:
            continue
        if is_in_stock(p["url"]):
            msg = f"🔥 STOCK ALERT\n{p['name']}\n{p['url']}"
            for uid in paid_users:
                await context.bot.send_message(uid, msg)
            sent.add(p["url"])

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(MessageHandler(filters.PHOTO, handle_payment))
    app.job_queue.run_repeating(stock_loop, interval=STOCK_INTERVAL, first=5)
    print("🚀 BOT RUNNING AUTO MODE ON")
    app.run_polling()

if __name__ == "__main__":
    main()
