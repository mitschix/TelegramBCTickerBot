#!/usr/bin/env python3
"""
BitCoinTicker as telegram bot
with a bit user maanagement for borders and amount
"""

from db_handler import db_create, db_user_exist, db_read, db_change, \
    db_user_create, db_users, DB_NAME
from telegram import InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackQueryHandler, ConversationHandler

import os
from typing import Optional

from tel_token import bot_token
from btc_query import get_btcrate_currency
from bot_keyboards import KEYBOARDS
from bot_msg import MSG_STATIC, MSG_DYNAMIC

# set conversation handler vars
LOW, HIGH, CURRENT = range(3)


# handler functions for bot
# start function called with /start
def start(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=MSG_STATIC['start'])


def register(update, context) -> None:
    chat_id = update.message.chat_id
    db_user_create(chat_id)
    context.bot.send_message(chat_id=update.message.chat_id, text=MSG_STATIC['user_new'])


# show different menus
def main_menu(update, context) -> int:
    reply_markup = InlineKeyboardMarkup(KEYBOARDS['main'])
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=MSG_STATIC['main'], reply_markup=reply_markup)
    return LOW


def menu_markup(context, update, keyboard, msg=MSG_STATIC['main']) -> None:
    context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, text=msg,
                                  message_id=update.callback_query.message.message_id, reply_markup=InlineKeyboardMarkup(keyboard))


def border_low(update, context) -> int:
    low_bd = update.message.text
    user = update.message.chat_id
    db_change(user, "lowborder", low_bd)
    context.bot.send_message(chat_id=update.message.chat_id, text=MSG_DYNAMIC['low_set'] % low_bd)
    return HIGH


def border_high(update, context) -> int:
    high_bd = int(update.message.text)
    user = update.message.chat_id
    borders = db_read(user, "borders")
    low_bd, _ = borders[0]
    if high_bd < low_bd:
        context.bot.send_message(chat_id=user, text=MSG_STATIC['error_high'])
        return HIGH
    else:
        db_change(user, "highborder", high_bd)
        context.bot.send_message(chat_id=user,
                                 text=MSG_DYNAMIC['high_set'] % high_bd,
                                 reply_markup=InlineKeyboardMarkup(KEYBOARDS['main']))
        db_change(user, "cnt_reset")
        check_btc_rate_eur(context)
        return ConversationHandler.END


def current_btc(update, context) -> int:
    user = update.message.chat_id
    current_amount = float(update.message.text)
    db_change(user, "chamount", current_amount)
    context.bot.send_message(chat_id=user, text=MSG_DYNAMIC['amount_set'] % current_amount,
                             reply_markup=InlineKeyboardMarkup(KEYBOARDS['main']))
    return ConversationHandler.END


def wrong_conv(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=MSG_STATIC['error_number'])


def handle_opt_main(update, context, data: str) -> None:
    use_keyboard = {
        "main": KEYBOARDS['main'],
        "btc": KEYBOARDS['btc'],
        "ticker": KEYBOARDS['ticker'],
        "user": KEYBOARDS['user'],
    }
    menu_markup(context, update, use_keyboard[data])


def handle_opt_user(update, context, data: str, user_id: int) -> Optional[int]:
    if data == "deluser":
        db_change(user_id, "deluser")
        menu_markup(context, update, KEYBOARDS['main'], MSG_STATIC['user_del'])

    if data == "chdef":
        menu_markup(context, update, KEYBOARDS['curr_set'], MSG_STATIC['curr_default'])

    if data == "setcurrent":
        msg_id = update.callback_query.message.message_id
        context.bot.edit_message_text(
            chat_id=user_id, text=MSG_STATIC['amount_new'], message_id=msg_id)
        return CURRENT

    if data == "showcurrent":
        amount = db_read(user_id, "showamount")
        amount, = amount[0]
        if amount:
            msg = MSG_DYNAMIC['show_amount'] % amount
        else:
            msg = MSG_STATIC['no_amount']
        menu_markup(context, update, KEYBOARDS['user'], msg)
    return None


def handle_opt_chdef(update, context, data: str, user_id: int) -> None:
    curr = data
    db_change(user_id, "currency", curr)
    menu_markup(context, update, KEYBOARDS['main'], MSG_DYNAMIC['default_changed'] % curr)


def handle_opt_btc(update, context, data: str, user_id: int) -> None:
    if data == "getbtc":
        menu_markup(context, update, KEYBOARDS['curr_get'], MSG_STATIC['curr_select'])
    if data == "getbtcdef":
        curr = db_read(user_id, "currency")
        curr, = curr[0]
        btc_res, symbol = get_btcrate_currency(curr)

        amount = db_read(user_id, "showamount")
        amount, = amount[0]
        if amount:
            btc_usr = btc_res * amount
            btc_usr = round(btc_usr, 2)
            msg = MSG_DYNAMIC['current+anount'] % (curr, btc_res, symbol, btc_usr, symbol)
        else:
            msg = MSG_DYNAMIC['curernt'] % (curr, btc_res, symbol)
        menu_markup(context, update, KEYBOARDS['main'], msg)


def handle_opt_getbtc(update, context, data: str, user_id: int) -> None:
    curr = data
    btc_res, symbol = get_btcrate_currency(curr)
    amount = db_read(user_id, "showamount")
    if amount:
        amount, = amount[0]
        btc_usr = btc_res * amount
        btc_usr = round(btc_usr, 2)
        msg = MSG_DYNAMIC['current+anount'] % (curr, btc_res, symbol, btc_usr, symbol)
    else:
        msg = MSG_DYNAMIC['curernt'] % (curr, btc_res, symbol)
    menu_markup(context, update, KEYBOARDS['main'], msg)
    # get_btc(bot, update, data)


def handle_opt_ticker(update, context, data: str, user_id: int) -> Optional[int]:
    if data == "showborder":
        borders = db_read(user_id, "borders")
        low, high = borders[0]
        if low and high:
            msg = MSG_DYNAMIC['borders'] % (low, high)
        else:
            msg = MSG_STATIC['no_borders']
        menu_markup(context, update, KEYBOARDS['main'], msg)

    if data == "delborder":
        db_change(user_id, "delborders")
        menu_markup(context, update, KEYBOARDS['main'], MSG_STATIC['ticker_disable'])

    if data == "setborder":
        msg_id = update.callback_query.message.message_id
        context.bot.edit_message_text(
            chat_id=user_id, text=MSG_STATIC['set_low'], message_id=msg_id)
        return LOW
    return None


def buttons_control(update, context) -> Optional[int]:
    user = update.callback_query.message.chat_id
    option = update.callback_query.data.split("_")[0]
    data = update.callback_query.data.split("_")[1]

    user_needed = ["user", "ticker", "getbtcdef"]
#    user_needed = ["chdef", "getbtcdef", "showborder", "setborder", "deluser", "delborder", "current"]

    if data in user_needed and not db_user_exist(user):
        menu_markup(context, update, KEYBOARDS['no_user'], MSG_STATIC['register'])
        return None

    callback_int = None
    if option == "main":
        handle_opt_main(update, context, data)
    if option == "user":
        callback_int = handle_opt_user(update, context, data, user)
    if option == "chdef":
        handle_opt_chdef(update, context, data, user)
    if option == "btc":
        handle_opt_btc(update, context, data, user)
    if option == "getbtc":
        handle_opt_getbtc(update, context, data, user)
    if option == "ticker":
        callback_int = handle_opt_ticker(update, context, data, user)

    return callback_int


def echo(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=MSG_STATIC['error_cmd'])


def help_output(update, context) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text=MSG_STATIC['help'])


# job to check bitcoin and borders regulary
def check_btc_rate_eur(context) -> None:
    chat_ids = db_users()
    for user in chat_ids:
        curr = db_read(user, "currency")
        curr, = curr[0]

        btc_res, symbol = get_btcrate_currency(curr)
        borders = db_read(user, "borders")
        low, high = borders[0]
        if low and high:
            counter = db_read(user, "count")
            counter, = counter[0]
            # check counter for user if 0; decrease 3 times > 3 hours delay
            if btc_res >= float(high):
                if counter == 0:
                    msg = MSG_STATIC['high_reached'] % (curr, btc_res, symbol)
                    context.bot.send_message(chat_id=user, text=msg)
                db_change(user, "cnt_inc")
            elif btc_res <= float(low):
                if counter == 0:
                    msg = MSG_DYNAMIC['low_reached'] % (curr, btc_res, symbol)

                    context.bot.send_message(chat_id=user, text=msg)
                db_change(user, "cnt_inc")

            if counter == 3:
                db_change(user, "cnt_reset")


def main() -> None:
    """
    set variables and setup bot
    """
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher
    jobs = updater.job_queue

    # once per day: 86400
    # 21600 - 6 hour interval
    jobs.run_repeating(check_btc_rate_eur, interval=3600, first=0)

    # handler
    start_handler = CommandHandler('start', start)
    register_handler = CommandHandler('register', register)
    help_handler = CommandHandler('help', help_output)
    main_handler = CommandHandler('menu', main_menu)
    button_handler = CallbackQueryHandler(buttons_control)

    conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[button_handler],
        states={
            LOW: [MessageHandler(Filters.regex(r'^(\d*)$'), border_low, pass_user_data=True)],
            HIGH: [MessageHandler(Filters.regex(r'^(\d*)$'), border_high, pass_user_data=True)],
            CURRENT: [MessageHandler(Filters.regex(r'^(\d+\.)?\d+$'), current_btc,
                                     pass_user_data=True)],
        },
        fallbacks=[MessageHandler(
            Filters.text, wrong_conv, pass_user_data=True)]
    )

    # add handler to dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(register_handler)
    dispatcher.add_handler(main_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(conv_handler)

    # start the bot
    print("starting all_finance_bot")
    if not os.path.exists(DB_NAME):
        db_create()
    updater.start_polling()
    # run the bot until it receives Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
    print("User forced me to stop... i am sorrey ):")
