from dotenv import load_dotenv
import os
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from functions import start, info
import re
from nlp_functions import check_language

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

    user_questions[user_id] = {'question': None,
                               'question_confirmed': False,
                               'options': None, 
                               'num_options': None,
                               'options_confirmed': False,
                               }  # Initialize a dictionary for user's question
    print("user_questions:", user_questions) # Just to view the updating of dictionary in your terminal when program is running

async def handle_inputs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  # Retrieve user ID

    # If user typed something before initialising /poll 
    if user_id not in user_questions:
        await update.message.reply_text("Please start by using /poll first before sending your question.")
        return
    
    # If user has not confirmed question
    if not user_questions[user_id]['question_confirmed']:
        user_questions[user_id]['question'] = update.message.text # Retrive text sent by user after initialising /poll and store in dictionary

        # Construct inline keyboard with a "Continue" button
        keyboard = [[InlineKeyboardButton("Continue", callback_data="continue")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = user_questions[user_id]['question']

        confidence_score = check_language(text)

        print("Confidence Score:", confidence_score)

        if confidence_score > 0.2: # Threshold for us to set
            # Ask for confirmation with "Continue" inline button
            await update.message.reply_text(
                text=
                "Your Question: " + user_questions[user_id]['question'] + "\n"
                "\n"
                "Mistyped your question? Just send it again below \n",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                text=
                "Your poll does not seem to be in English, please retry\n"
            )

    # If user has not confirmed options
    elif not user_questions[user_id]['options_confirmed']:
        user_input = update.message.text
        output_string = re.sub(r'\n+', '\n', user_input) #trims all extra \n s
        responses = output_string.strip().splitlines()

        user_questions[user_id]['options'] = responses
        user_questions[user_id]['num_options'] = len(responses)
        #calls back the prev function if too long or too short
        if user_questions[user_id]['num_options'] > 10 or user_questions[user_id]['num_options'] < 2: 
            many_or_little = lambda x: 'many' if x > 10 else 'few'
            message = f"You have indicated too {many_or_little(user_questions[user_id]['num_options'])} options!"
            await update.message.reply_text(
                text=message,
            )
            user_questions[user_id]['options'] = None
            user_questions[user_id]['num_options'] = None
            await handle_options(update, context)
            return
        message = "This is your poll: \n\n"
        message += "*" + "Question: " + user_questions[user_id]['question'] + "*\n\n"
        for response in responses:
            message += response + "\n"
        
        message += "\nMistyped your options? Just send it again below \n"

        keyboard = [[InlineKeyboardButton("Post", callback_data="post")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    print("user_questions:", user_questions) # Just to view the updating of dictionary in your terminal when program is running

# Function to handle options, can only be called through button_callback and "continue" callback_data
async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id # Retrieve user ID

    user_questions[user_id]['question_confirmed'] = True # Update dictionary

    await bot.send_message(
        chat_id=user_id,
        text=
        "*2-10 options allowed*\n\n"
        "*Type options below, leave a line for a new option*\n\n"
        "_Template:_ \n"
        "M - Yes\n"
        "M - No\n"
        "F - Yes\n"
        "F - No\n"
        "Check Answers\n"
        ,
        parse_mode=ParseMode.MARKDOWN
    )

# Post Poll on Channel
async def post_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id # Retrieve user ID
    user_questions[user_id]['options_confirmed'] = True # Update dictionary (A little redundant not gonna lie)

    # Sends poll to channel
    await bot.send_poll(
        chat_id=CHANNEL_ID,
        question="Question: " + user_questions[user_id]['question'],
        options=user_questions[user_id]['options'],
        type="regular"
    )

    del user_questions[user_id] # Deletes user dictionary once poll is sent to channel

    print("user_questions:", user_questions)

# Function to handle all buttons 
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query # Retrive the callback_data from buttons (etc "continue" callback_data from "Continue" button)

    if query.data == "continue":
        # User has clicked "Continue", proceed to handle options (either through buttons too or user input)
        await handle_options(update, context)
    elif query.data == "post":
        await post_poll(update, context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start)) # Tags start to /start
    app.add_handler(CommandHandler('info', info)) # Tags info to /info
    app.add_handler(CommandHandler('poll', poll)) # Tags poll to /poll
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_inputs))  # Handles the user's inputs
    app.add_handler(CallbackQueryHandler(button_callback)) # Handles all buttons' callback_data
    app.run_polling()

if __name__ == '__main__':
    main()
