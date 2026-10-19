from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils.keyboards import KEYBOARDS
from utils.messages import MSG_STATIC


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        MSG_STATIC["main"],
        reply_markup=InlineKeyboardMarkup(KEYBOARDS["main"]),
    )
