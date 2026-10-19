from typing import Optional

from db.db_handler import db_set_currency, db_user_exist
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils.keyboards import KEYBOARDS
from utils.messages import MSG_DYNAMIC, MSG_STATIC

from .btc import handle_opt_btc, handle_opt_getbtc
from .intervals import handle_opt_interval
from .ticker import handle_opt_ticker
from .user import handle_opt_user


async def buttons_control(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Optional[int]:
    query = update.callback_query
    await query.answer()

    user_id = query.message.chat.id

    try:
        option, data = query.data.split("_", 1)
    except ValueError:
        return None

    user_required = {"user", "ticker", "getbtcdef"}
    if data in user_required and not db_user_exist(user_id):
        await query.edit_message_text(
            MSG_STATIC["register"],
            reply_markup=InlineKeyboardMarkup(KEYBOARDS["no_user"]),
        )
        return None

    if option == "main":
        # edit the existing message; update.message is None for callback queries
        await query.edit_message_text(
            MSG_STATIC["main"],
            reply_markup=InlineKeyboardMarkup(KEYBOARDS["main"]),
        )

    elif option == "user":
        return await handle_opt_user(update, context, data, user_id)

    elif option == "chdef":
        db_set_currency(user_id, data)
        await query.edit_message_text(
            MSG_DYNAMIC["default_changed"] % data,
            reply_markup=InlineKeyboardMarkup(KEYBOARDS["main"]),
        )

    elif option == "btc":
        await handle_opt_btc(update, context, data, user_id)

    elif option == "getbtc":
        await handle_opt_getbtc(update, context, data, user_id)

    elif option == "ticker":
        return await handle_opt_ticker(update, context, data, user_id)

    elif option == "interval":
        await handle_opt_interval(update, context, data, user_id)

    return None
