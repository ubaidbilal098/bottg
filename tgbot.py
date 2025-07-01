import os
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Initialize Telegram Bot
TELEGRAM_TOKEN = "8004968195:AAHnh7YmF2rKOu8xpjD4QJjtvoMAR_S5K8U"  # Replace with your new token
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Configure Gemini
GEMINI_API_KEY = "AIzaSyD3Ltks10HNcg5Xy3-8m5MHxP2smYNpoxU"  # Replace with your new key
genai.configure(api_key=GEMINI_API_KEY)

# Use the current model name - try these options:
# "gemini-1.5-flash" (fastest)
# "gemini-1.5-pro" (more capable)
# "gemini-1.0-pro" (original)
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I\'m your Gemini AI assistant. Send me a message and I\'ll respond.')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Just type anything and I\'ll generate a response using Gemini AI!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Sorry, I encountered an error: {str(e)}")

def main():
    print("Starting bot...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Polling
    print("Polling...")
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()
