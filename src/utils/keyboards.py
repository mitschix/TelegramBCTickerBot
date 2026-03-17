from telegram import InlineKeyboardButton

from utils.btc_query import CURR_LIST

keyboard_curr_set = [
    [InlineKeyboardButton(curr, callback_data=f"chdef_{curr}")] for curr in CURR_LIST
]
keyboard_curr_set.append([InlineKeyboardButton("Go Back", callback_data="main_btc")])

keyboard_curr_get = [
    [InlineKeyboardButton(curr, callback_data=f"getbtc_{curr}")] for curr in CURR_LIST
]
keyboard_curr_get.append([InlineKeyboardButton("Go Back", callback_data="main_btc")])

keyboard_main = [
    [InlineKeyboardButton("Ticker", callback_data="main_ticker")],
    [InlineKeyboardButton("Bitcoin", callback_data="main_btc")],
    [InlineKeyboardButton("User", callback_data="main_user")],
]

keyboard_btc = [
    [InlineKeyboardButton("Get Bitcoin", callback_data="btc_getbtc")],
    [InlineKeyboardButton("Get Bitcoin Default", callback_data="btc_getbtcdef")],
    [InlineKeyboardButton("Go Back", callback_data="main_main")],
]

keyboard_ticker = [
    [InlineKeyboardButton("Show borders", callback_data="ticker_showborder")],
    [
        InlineKeyboardButton(
            "Delete borders\n(Disables ticker)", callback_data="ticker_delborder"
        )
    ],
    [InlineKeyboardButton("Set borders", callback_data="ticker_setborder")],
    [InlineKeyboardButton("Set interval", callback_data="ticker_interval")],
    [InlineKeyboardButton("Go Back", callback_data="main_main")],
]

keyboard_no_user = [
    [InlineKeyboardButton("Bitcoin", callback_data="main_btc")],
    [InlineKeyboardButton("Go Main Menu", callback_data="main_main")],
]

keyboard_user = [
    [InlineKeyboardButton("Change Default Currency", callback_data="user_chdef")],
    [InlineKeyboardButton("Set Bitcoin amount", callback_data="user_setcurrent")],
    [InlineKeyboardButton("Show Bitcoin amount", callback_data="user_showcurrent")],
    [InlineKeyboardButton("Delete User", callback_data="user_deluser")],
    [InlineKeyboardButton("Go Back", callback_data="main_main")],
]

keyboard_interval = [
    [InlineKeyboardButton("Every 1 hour", callback_data="interval_1")],
    [InlineKeyboardButton("Every 2 hours", callback_data="interval_2")],
    [InlineKeyboardButton("Every 4 hours", callback_data="interval_4")],
    [InlineKeyboardButton("Every 6 hours", callback_data="interval_6")],
    [InlineKeyboardButton("Every 12 hours", callback_data="interval_12")],
    [InlineKeyboardButton("Every 24 hours", callback_data="interval_24")],
    [InlineKeyboardButton("Disable notifications", callback_data="interval_0")],
    [InlineKeyboardButton("Back", callback_data="main_ticker")],
]

KEYBOARDS = {
    "curr_set": keyboard_curr_set,
    "curr_get": keyboard_curr_get,
    "main": keyboard_main,
    "btc": keyboard_btc,
    "ticker": keyboard_ticker,
    "no_user": keyboard_no_user,
    "user": keyboard_user,
    "interval": keyboard_interval,
}
