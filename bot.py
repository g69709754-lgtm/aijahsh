import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.business_message
    if not message or not message.text:
        return
    try:
        response = model.generate_content(message.text)
        await message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))
    app.run_polling()
