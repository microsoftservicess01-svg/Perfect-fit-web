import os
import threading
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
import uvicorn

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))

user_state = {}

# ================= HELPERS =================
def calculate_bra_size(underbust, bust):
    band = round(underbust / 5) * 5
    diff = bust - underbust
    cup_map = {10: "A", 12: "B", 14: "C", 16: "D", 18: "DD"}
    cup = cup_map.get(min(cup_map.keys(), key=lambda x: abs(x - diff)), "B")
    return f"{int(band / 2)}{cup}"

# ================= BOT HANDLERS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_state[uid] = {"step": "UNDERBUST"}

    await update.message.reply_text(
        "👙 *Welcome to Perfect Fit* 💖\n\n"
        "Find your *correct bra size* and get *perfect bra recommendations* in minutes.\n\n"
        "📏 Let’s start.\n"
        "What is your *underbust measurement (in cm)*?",
        parse_mode="Markdown"
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text.strip()

    if uid not in user_state:
        await start(update, context)
        return

    step = user_state[uid]["step"]

    # STEP 1: UNDERBUST
    if step == "UNDERBUST":
        if not text.isdigit():
            await update.message.reply_text("❗ Please enter a number (cm).")
            return

        user_state[uid]["underbust"] = int(text)
        user_state[uid]["step"] = "BUST"

        await update.message.reply_text(
            "📐 Great! Now tell me your *bust measurement (in cm)*:",
            parse_mode="Markdown"
        )

    # STEP 2: BUST
    elif step == "BUST":
        if not text.isdigit():
            await update.message.reply_text("❗ Please enter a number (cm).")
            return

        under = user_state[uid]["underbust"]
        bust = int(text)
        size = calculate_bra_size(under, bust)

        user_state[uid]["size"] = size
        user_state[uid]["step"] = "TYPE"

        keyboard = [
            [InlineKeyboardButton("Daily Comfort", callback_data="TYPE_DAILY")],
            [InlineKeyboardButton("Sports", callback_data="TYPE_SPORTS")],
            [InlineKeyboardButton("Party / Occasion", callback_data="TYPE_PARTY")],
        ]

        await update.message.reply_text(
            f"✅ Your bra size is *{size}*\n\n"
            "What type of bra are you looking for?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ================= BUTTON HANDLER =================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    data = query.data

    # STEP 3: BRA TYPE
    if data.startswith("TYPE_"):
        user_state[uid]["type"] = data.replace("TYPE_", "")
        user_state[uid]["step"] = "PRICE"

        keyboard = [
            [InlineKeyboardButton("Under ₹700", callback_data="PRICE_LOW")],
            [InlineKeyboardButton("₹700 – ₹1500", callback_data="PRICE_MID")],
            [InlineKeyboardButton("Premium", callback_data="PRICE_HIGH")],
        ]

        await query.edit_message_text(
            "💰 What’s your budget?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # STEP 4: PRICE → SHOW BRANDS
    elif data.startswith("PRICE_"):
        size = user_state[uid]["size"]
        bra_type = user_state[uid]["type"]

        await query.edit_message_text(
            f"🛍 *Top Bra Recommendations for You*\n\n"
            f"👙 Size: *{size}*\n"
            f"🎯 Type: *{bra_type}*\n\n"
            "• **Zivame Cotton Non-Wired** – ₹649\n"
            "https://www.zivame.com/\n\n"
            "• **Clovia Comfort Cotton** – ₹599\n"
            "https://www.clovia.com/\n\n"
            "• **Enamor Soft Touch** – ₹699\n"
            "https://www.amazon.in/s?k=enamor+bra\n\n"
            "• **Jockey Cotton Comfort** – ₹749\n"
            "https://www.amazon.in/s?k=jockey+bra\n\n"
            "• **Hanes Everyday Support** – ₹699\n"
            "https://www.amazon.in/s?k=hanes+bra\n\n"
            "• **Triumph Premium Fit** – ₹1299\n"
            "https://www.triumphindia.com/\n\n"
            "✨ Want to try again? Type /start",
            parse_mode="Markdown"
        )

# ================= FASTAPI =================
api = FastAPI()

@api.get("/")
def health():
    return {"status": "Perfect Fit running"}

# ================= RUN =================
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    uvicorn.run(api, host="0.0.0.0", port=PORT)
    
