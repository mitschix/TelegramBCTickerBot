from telegram import Update
from telegram.ext import ContextTypes
from utils.messages import MSG_STATIC


async def help_output(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MSG_STATIC["help"])
