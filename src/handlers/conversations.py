from db.db_handler import db_set_amount
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.keyboards import KEYBOARDS
from utils.messages import MSG_DYNAMIC, MSG_STATIC

LOW, HIGH, CURRENT = range(3)


async def current_btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    try:
        amount = float(update.message.text)
    except ValueError:
        await update.message.reply_text(MSG_STATIC["error_number"])
        return CURRENT

    db_set_amount(user_id, amount)
    await update.message.reply_text(
        MSG_DYNAMIC["amount_set"] % amount,
        reply_markup=InlineKeyboardMarkup(KEYBOARDS["main"]),
    )
    return ConversationHandler.END


async def wrong_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MSG_STATIC["error_number"])
