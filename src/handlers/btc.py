import asyncio
from typing import Optional

from db.db_handler import db_read_amount, db_read_currency
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils.btc_query import get_btcrate_currency
from utils.keyboards import KEYBOARDS
from utils.messages import MSG_DYNAMIC, MSG_STATIC


async def show_btc(curr: str, user_id: int, query) -> None:
    """Show the current btc price for a currency and the user's amount, if set."""
    btc_res, symbol = await asyncio.to_thread(get_btcrate_currency, curr)
    amount = db_read_amount(user_id)

    if amount is not None:
        btc_usr = round(btc_res * amount, 2)
        msg = MSG_DYNAMIC["current+amount"] % (curr, btc_res, symbol, btc_usr, symbol)
    else:
        msg = MSG_DYNAMIC["current"] % (curr, btc_res, symbol)

    await query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(KEYBOARDS["main"]),
    )


async def handle_opt_btc(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: str, user_id: int
):
    query = update.callback_query

    if data == "getbtc":
        await query.edit_message_text(
            MSG_STATIC["curr_select"],
            reply_markup=InlineKeyboardMarkup(KEYBOARDS["curr_get"]),
        )

    elif data == "getbtcdef":
        await show_btc(db_read_currency(user_id), user_id, query)


async def handle_opt_getbtc(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: str, user_id: int
):
    await show_btc(data, user_id, update.callback_query)
