from dotenv import load_dotenv
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Define the start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a Telegram bot.")

# Define the message handler
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Set up the bot handlers
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.text & ~filters.command, echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()



