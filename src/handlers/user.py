import os
from typing import Optional

from db.db_handler import (
    db_delete_user,
    db_read_amount,
    db_user_create,
)
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils.keyboards import KEYBOARDS
from utils.messages import MSG_DYNAMIC, MSG_STATIC

from .conversations import CURRENT

# optional: bot notifies this chat on new registrations; unset = no notification
ADMIN_ID = os.getenv("ADMIN_ID")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MSG_STATIC["start"])


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user

    db_user_create(chat_id)
    await update.message.reply_text(MSG_STATIC["user_new"])

    if ADMIN_ID:
        await context.bot.send_message(
            chat_id=ADMIN_ID, text=f"New user: {user.username} ({chat_id})"
        )


async def handle_opt_user(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: str, user_id: int
) -> Optional[int]:
    query = update.callback_query

    if data == "deluser":
        db_delete_user(user_id)
        await query.edit_message_text(
            MSG_STATIC["user_del"],
            reply_markup=InlineKeyboardMarkup(KEYBOARDS["main"]),
        )

    elif data == "chdef":
        await query.edit_message_text(
            MSG_STATIC["curr_default"],
            reply_markup=InlineKeyboardMarkup(KEYBOARDS["curr_set"]),
        )

    elif data == "setcurrent":
        await query.edit_message_text(MSG_STATIC["amount_new"])
        return CURRENT

    elif data == "showcurrent":
        amount = db_read_amount(user_id)
        if amount is not None:
            msg = MSG_DYNAMIC["show_amount"] % amount
        else:
            msg = MSG_STATIC["no_amount"]

        await query.edit_message_text(
            msg,
            reply_markup=InlineKeyboardMarkup(KEYBOARDS["user"]),
        )

    return None
