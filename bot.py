from dotenv import load_dotenv
import os
from telegram import Update, Bot
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
bot = Bot(token=BOT_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text = 
        "Welcome to NUSPolls 📊\n" 
        "Have a heartburning question to ask? \n"
        "A completely anonymous platform made by *NUS Students for NUS Students*.\n"
        , parse_mode = ParseMode.MARKDOWN
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text = 
        "*How do we guarantee your annonymity?* \n"
        "We use hashing to hide every user's identity. Unlike encryption, hashing cannot be undone. \n"
        , parse_mode = ParseMode.MARKDOWN
    )

async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def canitalk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bot.send_message(chat_id=CHANNEL_ID, text="IM TALKING")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('info', info))
    app.add_handler(CommandHandler('canitalk', canitalk))
    app.run_polling()

if __name__ == '__main__':
    main()
