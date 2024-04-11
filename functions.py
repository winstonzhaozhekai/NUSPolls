from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import random
import hashlib




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text = 
        "*Welcome to NUSPolls* 📊\n" 
        "\n"
        "Do you have a heartburning question you wish to ask? Do you find it hard to relate to PaisehQs?\n"
        "\n"
        "Click /poll to start a poll on our channel now: <insert link> \n"
        "\n"
        "Simply type in your question, select how many options you want and it will be posted *anonymously* on the channel \n"
        "\n"
        "Want to respond to polls beyond voting? Introducing our *completely anonymous* comment function. Click on /comment beneath the poll and you will be able to type your reply to the bot *anonymously* (No one will see your user typing in the comment section!) \n"
        "\n"
        "Fret not, the username displayed in each poll's comments are independent of each other, so your identity is protected \n"
        "\n"
        "A completely anonymous platform that prioritises your anonymity, made by *NUS Students for NUS Students*.\n"
        "\n"
        "More info here @ /info \n"
        , parse_mode = ParseMode.MARKDOWN
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text = 
        "*How do we guarantee your annonymity?* \n"
        "\n"
        "We use hashing to hide every user's identity. Unlike encryption, hashing cannot be undone. Your unique user ID is directly pipelined into the hashing function, with no interactions between so your true user ID is never revealed to anyone, *including us*\n"
        "\n"
        "*How do we address users who are misusing the platform?*\n"
        "\n"
        "We admins have the capabilities to ban or timeout users who have misused the platform. We do not rely on AI so you, the users can freely send in anything you wish. However keep in mind, we can ban you. We don't need to know your true user ID, since hashing will produce the same output given the same input, it is not random. So we will know your anonymous identity and stop you from using the platform without ever compromising on anonymity. \n"
        "\n"
        "*I still do not understand how hashing works, how does it protect me?* \n"
        "\n"
        "Let's say your user ID is 0001, and after hashing, it becomes 888b19a. This hashed ID can never be traced back to 0001, so no one can never find out who is 888b19a. But no other user ID other than 0001 will be hased into 888b19a. So we will never know your true identity but we will know your given anonymous identity, still giving us the ability to regulate the channel while protecting your identity \n"
        , parse_mode = ParseMode.MARKDOWN
    )


