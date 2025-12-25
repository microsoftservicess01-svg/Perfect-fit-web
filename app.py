import os
import threading
from fastapi import FastAPI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import uvicorn

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))

# ---------------- Telegram Bot ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👙 Perfect Fit\n\n"
        "Type:\n• bra size\n• sports bra under 1000\n• comfortable bra"
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "sports" in text:
        reply = "🏃 Sports Bra: High support, non-wired."
    elif "size" in text:
        reply = "📏 Measure snug underbust for correct size."
    else:
        reply = "👙 Cotton, wireless bras are best for daily comfort."
    await update.message.reply_text(reply)

def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.run_polling()

# ---------------- FastAPI Web Server ----------------
api = FastAPI()

@api.get("/")
def root():
    return {"status": "Perfect Fit bot running"}

def start_server():
    uvicorn.run(api, host="0.0.0.0", port=PORT)

# ---------------- Main ----------------
if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    start_server()