import os
import threading
import asyncio
from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import uvicorn

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))

# ---------------- Telegram Bot ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👙 *Perfect Fit*\n\n"
        "Type:\n"
        "• bra size\n"
        "• sports bra under 1000\n"
        "• comfortable bra",
        parse_mode="Markdown"
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "sports" in text:
        reply = "🏃 *Sports Bra*\n• High support\n• Non-wired"
    elif "size" in text:
        reply = "📏 *Bra Size Tip*\nMeasure underbust snugly."
    else:
        reply = "👙 *Daily Comfort*\nCotton, wireless bras work best."
    await update.message.reply_text(reply, parse_mode="Markdown")

def run_bot():
    async def bot_main():
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
        await app.initialize()
        await app.start()
        await app.bot.initialize()
        await app.updater.start_polling()
        await asyncio.Event().wait()

    asyncio.run(bot_main())

# ---------------- FastAPI Web Server ----------------
api = FastAPI()

@api.get("/")
def root():
    return {"status": "Perfect Fit bot running"}

# ---------------- Main ----------------
if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    uvicorn.run(api, host="0.0.0.0", port=PORT)
    
