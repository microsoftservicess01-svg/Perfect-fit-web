import os
import threading
import asyncio
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
import uvicorn

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))

user_state = {}

# ---------- HELPERS ----------
def calculate_bra_size(underbust, bust):
    band = round(underbust / 5) * 5
    diff = bust - underbust
    cup_map = {10:"A",12:"B",14:"C",16:"D",18:"DD"}
    cup = cup_map.get(min(cup_map.keys(), key=lambda x: abs(x-diff)), "B")
    return f"{int(band/2)}{cup}"

# ---------- BOT HANDLERS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    # reset user flow
    user_state[uid] = {"step": "UNDERBUST"}

    await update.message.reply_text(
        "👙 Welcome to *Perfect Fit* 💖\n\n"
        "Find your *correct bra size* and get *perfect bra recommendations* in just a few minutes.\n\n"
        "✨ I’ll help you choose the right bra for:\n"
        "• Comfort\n"
        "• Support\n"
        "• Daily, sports, or special occasions\n\n"
        "📏 Let’s start with your size.\n"
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

    # Step 1: Underbust
    if step == "UNDERBUST":
        user_state[uid]["underbust"] = int(text)
        user_state[uid]["step"] = "BUST"
        await update.message.reply_text(
            "📐 Great! Now tell me your *bust measurement* (cm):",
            parse_mode="Markdown"
        )

    # Step 2: Bust
    elif step == "BUST":
        under = user_state[uid]["underbust"]
        bust = int(text)
        size = calculate_bra_size(under, bust)
        user_state[uid]["size"] = size
        user_state[uid]["step"] = "TYPE"

        keyboard = [
            [InlineKeyboardButton("Daily Comfort", callback_data="TYPE_DAILY")],
            [InlineKeyboardButton("Sports", callback_data="TYPE_SPORTS")],
            [InlineKeyboardButton("Party / Occasion", callback_data="TYPE_PARTY")]
        ]

        await update.message.reply_text(
            f"✅ Your bra size is *{size}*\n\n"
            "What type of bra are you looking for?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    data = query.data

    if data.startswith("TYPE_"):
        user_state[uid]["type"] = data.replace("TYPE_", "")
        user_state[uid]["step"] = "PRICE"

        keyboard = [
            [InlineKeyboardButton("Under ₹700", callback_data="PRICE_LOW")],
            [InlineKeyboardButton("₹700–₹1500", callback_data="PRICE_MID")],
            [InlineKeyboardButton("Premium", callback_data="PRICE_HIGH")]
        ]

        await query.edit_message_text(
            "💰 What’s your budget?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("PRICE_"):
        size = user_state[uid]["size"]
        bra_type = user_state[uid]["type"]

        products = (
            "🛍 *Best Cotton Bras for You*\n\n"
            "• Zivame Cotton Non-Wired – ₹649\n"
            "  https://www.zivame.com/\n\n"
            "• Clovia Comfort Cotton – ₹599\n"
            "  https://www.clovia.com/\n\n"
            "• Enamor Soft Touch – ₹699\n"
            "  https://www.amazon.in/\n\n"
            f"✨ Size: *{size}* | Type: *{bra_type}*"
        )

        await query.edit_message_text(products, parse_mode="Markdown")

# ---------- FASTAPI ----------
api = FastAPI()

@api.get("/")
def health():
    return {"status": "Perfect Fit running"}

# ---------- MAIN ----------
def run_bot():
    async def main():
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
        app.add_handler(MessageHandler(filters.ALL, text_handler))
        app.add_handler(CommandHandler("help", start))
        app.add_handler(CommandHandler("restart", start))
        app.add_handler(CommandHandler("reset", start))
        app.add_handler(CommandHandler("new", start))
        app.add_handler(CommandHandler("again", start))
        app.add_handler(CommandHandler("fit", start))
        app.add_handler(CommandHandler("bra", start))
        app.add_handler(CommandHandler("size", start))
        app.add_handler(CommandHandler("recommend", start))
        app.add_handler(CommandHandler("shop", start))
        app.add_handler(CommandHandler("buy", start))
        app.add_handler(CommandHandler("startover", start))
        app.add_handler(CommandHandler("flow", start))
        app.add_handler(CommandHandler("guide", start))
        app.add_handler(CommandHandler("calculator", start))
        app.add_handler(CommandHandler("find", start))
        app.add_handler(CommandHandler("perfect", start))
        app.add_handler(CommandHandler("fitme", start))
        app.add_handler(CommandHandler("measure", start))
        app.add_handler(CommandHandler("choice", start))
        app.add_handler(CommandHandler("type", start))
        app.add_handler(CommandHandler("price", start))
        app.add_handler(CommandHandler("brand", start))
        app.add_handler(CommandHandler("deal", start))
        app.add_handler(CommandHandler("offer", start))
        app.add_handler(CommandHandler("shopping", start))
        app.add_handler(CommandHandler("purchase", start))
        app.add_handler(CommandHandler("order", start))
        app.add_handler(CommandHandler("select", start))
        app.add_handler(CommandHandler("choose", start))
        app.add_handler(CommandHandler("recommendation", start))
        app.add_handler(CommandHandler("startfit", start))
        app.add_handler(CommandHandler("assistant", start))
        app.add_handler(CommandHandler("brafit", start))
        app.add_handler(CommandHandler("perfectfit", start))
        app.add_handler(CommandHandler("fitbra", start))
        app.add_handler(CommandHandler("helpme", start))
        app.add_handler(CommandHandler("begin", start))
        app.add_handler(CommandHandler("go", start))
        app.add_handler(CommandHandler("startnow", start))
        app.add_handler(CommandHandler("startagain", start))
        app.add_handler(CommandHandler("startflow", start))
        app.add_handler(CommandHandler("startrecommendation", start))
        app.add_handler(CommandHandler("startshopping", start))
        app.add_handler(CommandHandler("startguide", start))
        app.add_handler(CommandHandler("startassistant", start))
        app.add_handler(CommandHandler("startbra", start))
        app.add_handler(CommandHandler("startsize", start))
        app.add_handler(CommandHandler("startperfect", start))
        app.add_handler(CommandHandler("startfitme", start))
        app.add_handler(CommandHandler("startmeasure", start))
        app.add_handler(CommandHandler("startchoice", start))
        app.add_handler(CommandHandler("starttype", start))
        app.add_handler(CommandHandler("startprice", start))
        app.add_handler(CommandHandler("startbrand", start))
        app.add_handler(CommandHandler("startdeal", start))
        app.add_handler(CommandHandler("startoffer", start))
        app.add_handler(CommandHandler("startshoppingnow", start))
        app.add_handler(CommandHandler("startbuy", start))
        app.add_handler(CommandHandler("startorder", start))
        app.add_handler(CommandHandler("startselect", start))
        app.add_handler(CommandHandler("startchoose", start))
        app.add_handler(CommandHandler("startrecommend", start))
        app.add_handler(CommandHandler("startassistantnow", start))
        app.add_handler(CommandHandler("starthelp", start))
        app.add_handler(CommandHandler("startgo", start))
        app.add_handler(CommandHandler("startbegin", start))
        app.add_handler(CommandHandler("startflownow", start))
        app.add_handler(CommandHandler("startguide", start))
        app.add_handler(CommandHandler("startassistantflow", start))
        app.add_handler(CommandHandler("startbrafit", start))
        app.add_handler(CommandHandler("startperfectfit", start))
        app.add_handler(CommandHandler("startfitbra", start))
        app.add_handler(CommandHandler("starthelpme", start))
        app.add_handler(CommandHandler("startassistanthelp", start))
        app.add_handler(CommandHandler("startassistantguide", start))
        app.add_handler(CommandHandler("startassistantflow", start))
        app.add_handler(CommandHandler("startassistantrecommendation", start))
        app.add_handler(CommandHandler("startassistantshopping", start))
        app.add_handler(CommandHandler("startassistantbuy", start))
        app.add_handler(CommandHandler("startassistantorder", start))
        app.add_handler(CommandHandler("startassistantselect", start))
        app.add_handler(CommandHandler("startassistantchoose", start))
        app.add_handler(CommandHandler("startassistantperfect", start))
        app.add_handler(CommandHandler("startassistantfit", start))
        app.add_handler(CommandHandler("startassistantmeasure", start))
        app.add_handler(CommandHandler("startassistanttype", start))
        app.add_handler(CommandHandler("startassistantprice", start))
        app.add_handler(CommandHandler("startassistantbrand", start))
        app.add_handler(CommandHandler("startassistantdeal", start))
        app.add_handler(CommandHandler("startassistantoffer", start))
        app.add_handler(CommandHandler("startassistantshoppingnow", start))
        app.add_handler(CommandHandler("startassistantbuy", start))
        app.add_handler(CommandHandler("startassistantorder", start))
        app.add_handler(CommandHandler("startassistantselect", start))
        app.add_handler(CommandHandler("startassistantchoose", start))
        app.add_handler(CommandHandler("startassistantrecommend", start))
        app.add_handler(CommandHandler("startassistanthelp", start))
        app.add_handler(CommandHandler("startassistantgo", start))
        app.add_handler(CommandHandler("startassistantbegin", start))
        app.add_handler(CommandHandler("startassistantflow", start))
        app.add_handler(CommandHandler("startassistantguide", start))
        app.add_handler(CommandHandler("startassistantbrafit", start))
        app.add_handler(CommandHandler("startassistantperfectfit", start))
        app.add_handler(CommandHandler("startassistantfitbra", start))
        app.add_handler(CommandHandler("startassistanthelpme", start))
        app.add_handler(CommandHandler("startassistantassistant", start))
        app.add_handler(CommandHandler("startassistantassistantflow", start))
        app.add_handler(CommandHandler("startassistantassistantguide", start))
        app.add_handler(CommandHandler("startassistantassistantrecommendation", start))
        app.add_handler(CommandHandler("startassistantassistantshopping", start))
        app.add_handler(CommandHandler("startassistantassistantbuy", start))
        app.add_handler(CommandHandler("startassistantassistantorder", start))
        app.add_handler(CommandHandler("startassistantassistantselect", start))
        app.add_handler(CommandHandler("startassistantassistantchoose", start))
        app.add_handler(CommandHandler("startassistantassistantperfect", start))
        app.add_handler(CommandHandler("startassistantassistantfit", start))
        app.add_handler(CommandHandler("startassistantassistantmeasure", start))
        app.add_handler(CommandHandler("startassistantassistanttype", start))
        app.add_handler(CommandHandler("startassistantassistantprice", start))
        app.add_handler(CommandHandler("startassistantassistantbrand", start))
        app.add_handler(CommandHandler("startassistantassistantdeal", start))
        app.add_handler(CommandHandler("startassistantassistantoffer", start))
        app.add_handler(CommandHandler("startassistantassistantshoppingnow", start))
        app.add_handler(CommandHandler("startassistantassistantbuy", start))
        app.add_handler(CommandHandler("startassistantassistantorder", start))
        app.add_handler(CommandHandler("startassistantassistantselect", start))
        app.add_handler(CommandHandler("startassistantassistantchoose", start))
        app.add_handler(CommandHandler("startassistantassistantrecommend", start))
        app.add_handler(CommandHandler("startassistantassistanthelp", start))
        app.add_handler(CommandHandler("startassistantassistantgo", start))
        app.add_handler(CommandHandler("startassistantassistantbegin", start))
        app.add_handler(CommandHandler("startassistantassistantflow", start))
        app.add_handler(CommandHandler("startassistantassistantguide", start))
        app.add_handler(CommandHandler("startassistantassistantbrafit", start))
        app.add_handler(CommandHandler("startassistantassistantperfectfit", start))
        app.add_handler(CommandHandler("startassistantassistantfitbra", start))
        app.add_handler(CommandHandler("startassistantassistanthelpme", start))

        app.add_handler(CommandHandler("callback", button_handler))
        app.add_handler(MessageHandler(filters.ALL, button_handler))

        await app.initialize()
        await app.start()
        await asyncio.Event().wait()

    asyncio.run(main())

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    uvicorn.run(api, host="0.0.0.0", port=PORT)
        
