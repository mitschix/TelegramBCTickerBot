from telegram import InlineKeyboardButton

from btc_query import CURR_LIST

# setting up the inline keyboards
keyboard_curr_set = [[InlineKeyboardButton(
    curr, callback_data="chdef_{}".format(curr))] for curr in CURR_LIST]
keyboard_curr_set += [InlineKeyboardButton(
    "Go Back", callback_data="main_btc")],
keyboard_curr_get = [[InlineKeyboardButton(
    curr, callback_data="getbtc_{}".format(curr))] for curr in CURR_LIST]
keyboard_curr_get += [InlineKeyboardButton(
    "Go Back", callback_data="main_btc")],
keyboard_main = [
    [InlineKeyboardButton("Ticker", callback_data="main_ticker")],
    [InlineKeyboardButton("Bitcoin", callback_data="main_btc")],
    [InlineKeyboardButton("User", callback_data="main_user")],
]
keyboard_btc = [
    [InlineKeyboardButton("Get Bitcoin", callback_data="btc_getbtc")],
    [InlineKeyboardButton("Get Bitcoin Default",
                          callback_data="btc_getbtcdef")],
    [InlineKeyboardButton("Go Back", callback_data="main_main")],
]
keyboard_ticker = [
    [InlineKeyboardButton("Show borders", callback_data="ticker_showborder")],
    [InlineKeyboardButton(
        "Delete borders\n(Disables ticker)", callback_data="ticker_delborder")],
    [InlineKeyboardButton("Set borders", callback_data="ticker_setborder")],
    [InlineKeyboardButton("Go Back", callback_data="main_main")],
]
keyboard_no_user = [
    [InlineKeyboardButton("Bitcoin", callback_data="main_btc")],
    [InlineKeyboardButton("Go Main Menu", callback_data="main_main")],
]
keyboard_user = [
    [InlineKeyboardButton("Change Default Currency",
                          callback_data="user_chdef")],
    [InlineKeyboardButton("Set Bitcoin amount",
                          callback_data="user_setcurrent")],
    [InlineKeyboardButton("Show Bitcoin amount",
                          callback_data="user_showcurrent")],
    [InlineKeyboardButton("Delete User", callback_data="user_deluser")],
    [InlineKeyboardButton("Go Back", callback_data="main_main")],
]

KEYBOARDS = {
    'curr_set': keyboard_curr_set,
    'curr_get': keyboard_curr_get,
    'main': keyboard_main,
    'btc': keyboard_btc,
    'ticker': keyboard_ticker,
    'no_user': keyboard_no_user,
    'user': keyboard_user
}


def main() -> None:
    print("helper script to allfbot.py")


if __name__ == "__main__":
    main()
