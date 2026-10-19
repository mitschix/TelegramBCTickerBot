from typing import Optional

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from db.db_handler import (
    db_clear_borders,
    db_read_borders,
    db_read_interval,
    db_set_high,
    db_set_low,
)
from utils.keyboards import KEYBOARDS
from utils.messages import MSG_DYNAMIC, MSG_STATIC

from .conversations import HIGH, LOW
from .jobs import cancel_user_job, schedule_user_job


async def border_low(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    try:
        low_bd = float(update.message.text)
    except ValueError:
        await update.message.reply_text(MSG_STATIC["error_number"])
        return LOW

    db_set_low(user_id, low_bd)
    await update.message.reply_text(MSG_DYNAMIC["low_set"] % low_bd)
    return HIGH


async def border_high(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    try:
        high_bd = float(update.message.text)
    except ValueError:
        await update.message.reply_text(MSG_STATIC["error_number"])
        return HIGH

    borders = db_read_borders(user_id)
    if not borders or borders[0] is None:
        await update.message.reply_text(MSG_STATIC["error_number"])
        return ConversationHandler.END

    low_bd, _ = borders
    if high_bd < low_bd:
        await update.message.reply_text(MSG_STATIC["error_high"])
        return HIGH

    db_set_high(user_id, high_bd)
    await update.message.reply_text(
        MSG_DYNAMIC["high_set"] % high_bd,
        reply_markup=InlineKeyboardMarkup(KEYBOARDS["main"]),
    )

    interval_hours = db_read_interval(user_id)
    await schedule_user_job(context, user_id, interval_hours)

    return ConversationHandler.END


async def handle_opt_ticker(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: str, user_id: int
) -> Optional[int]:
    query = update.callback_query

    if data == "showborder":
        borders = db_read_borders(user_id)
        if borders and borders[0] is not None and borders[1] is not None:
            low, high = borders
            interval = db_read_interval(user_id)
            interval_text = (
                MSG_DYNAMIC["interval_set"] % interval
                if interval
                else MSG_STATIC["notifs_off"]
            )
            msg = f"{interval_text}\n{MSG_DYNAMIC['borders'] % (low, high)}"
        else:
            msg = MSG_STATIC["no_borders"]

        await query.edit_message_text(
            msg,
            reply_markup=InlineKeyboardMarkup(KEYBOARDS["main"]),
        )

    elif data == "delborder":
        db_clear_borders(user_id)
        await cancel_user_job(context, user_id)
        await query.edit_message_text(
            MSG_STATIC["ticker_disable"],
            reply_markup=InlineKeyboardMarkup(KEYBOARDS["main"]),
        )

    elif data == "setborder":
        await query.edit_message_text(MSG_STATIC["set_low"])
        return LOW

    elif data == "interval":
        await query.edit_message_text(
            MSG_STATIC["interval_select"],
            reply_markup=InlineKeyboardMarkup(KEYBOARDS["interval"]),
        )

    return None
