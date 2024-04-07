from dotenv import load_dotenv
import os
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from functions import *

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
bot = Bot(token=BOT_TOKEN)

# Dictionary to store users' questions tagged to user ID
user_questions = {}

async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=
        "*Enter your question:* \n"
        , parse_mode = ParseMode.MARKDOWN
    )
    user_id = update.effective_user.id  # Retrieve user ID 
    user_questions[user_id] = {'question': False,
                               'options': False, 
                               'num_options': False,
                               'poll_confirmed': False,
                               'poll_posted': False}  # Initialize a dictionary for user's question
    print("user_questions:", user_questions) # Just to view the updating of dictionary in your terminal when program is running

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  # Retrieve user ID

    # If user typed something before initialising /poll 
    if user_id not in user_questions:
        await update.message.reply_text("Please start by using /poll first before sending your question.")
        return
    
    user_questions[user_id]['question'] = update.message.text # Retrive text sent by user after initialising /poll and store in dictionary

    # Construct inline keyboard with a "Continue" button
    keyboard = [[InlineKeyboardButton("Continue", callback_data="continue")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Ask for confirmation with "Continue" inline button
    await update.message.reply_text(
        text=
        "Your Question: " + user_questions[user_id]['question'] + "\n"
        "\n"
        "Mistyped your question? Just send it again below \n",
        reply_markup=reply_markup
    )

    print("user_questions:", user_questions) # Just to view the updating of dictionary in your terminal when program is running

# Function to handle options, can only be called through button_callback and "continue" callback_data
async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id # Retrieve user ID

    # Construct inline keyboard with 9 buttons in rows of 3
    keyboard = []
    row = [] # Temporary list to hold buttons for each row
    for i in range(1, 10):
        row.append(InlineKeyboardButton(str(i), callback_data=f"option_{i}"))
        if len(row) == 3:  # Row has 3 buttons
            keyboard.append(row)
            row = []  # Reset the row

    reply_markup = InlineKeyboardMarkup(keyboard)

    await bot.send_message(
        chat_id=user_id,
        text="*How many options?:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )

# Function to handle all buttons 
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query # Retrive the callback_data from buttons (etc "continue" callback_data from "Continue" button)

    if query.data == "continue":
        # User has clicked "Continue", proceed to handle options (either through buttons too or user input)
        await handle_options(update, context)

async def canitalk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bot.send_message(chat_id=CHANNEL_ID, text="IM TALKING")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start)) # Tags start to /start
    app.add_handler(CommandHandler('info', info)) # Tags info to /info
    app.add_handler(CommandHandler('poll', poll)) # Tags poll to /poll
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))  # Handles the user's input 
    app.add_handler(CommandHandler('canitalk', canitalk)) 
    app.add_handler(CallbackQueryHandler(button_callback)) # Handles all buttons' callback_data
    app.run_polling()

if __name__ == '__main__':
    main()