from dotenv import load_dotenv
import os
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from functions import start, info

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
bot = Bot(token=BOT_TOKEN)

# Dictionary to store user's questions
user_questions = {}

async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=
        "*Enter your question:* \n"
        , parse_mode = ParseMode.MARKDOWN
    )
    chat_id = update.effective_chat.id
    user_questions[chat_id] = {}  # Initialize an empty dictionary for user's question
    print("user_questions:", user_questions)

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in user_questions:
        await update.message.reply_text("Please start by using /poll first before sending your question.")
        return
    user_questions[chat_id]['question'] = update.message.text

    # Construct inline keyboard with a "Continue" button
    keyboard = [[InlineKeyboardButton("Continue", callback_data="continue")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=
        "Your Question: " + user_questions[chat_id]['question'] + "\n"
        "\n"
        "Mistyped your question? Just send it again below \n",
        reply_markup=reply_markup
    )
    print("user_questions:", user_questions)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "continue":
        # Here you can proceed to handling options after the user has clicked "Continue"
        await handle_options(update, context)

async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id

    await bot.send_message(
        chat_id=chat_id,
        text="*How many options?:*",
        parse_mode=ParseMode.MARKDOWN
    )

async def canitalk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bot.send_message(chat_id=CHANNEL_ID, text="IM TALKING")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('info', info))
    app.add_handler(CommandHandler('poll', poll))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))  # Handle the user's question
    app.add_handler(CommandHandler('canitalk', canitalk))
    app.add_handler(CallbackQueryHandler(button_callback)) # Handle "Continue" button after user sends question
    app.run_polling()

if __name__ == '__main__':
    main()
