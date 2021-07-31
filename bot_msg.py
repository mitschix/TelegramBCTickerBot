START_MESSAGE = """
Welcome! Calculating is on! :D
please use /menu to access the Main Menu at any time!
If you are new, might consider to hit /register to use the Ticker and a default currency!

If you have any ideas, request or bugs, don´t hasitate to contact me!
Thx for using my bot! Hope you will enjoy it!
- @mitschix
"""

HELP_MSG = """
/start                        - Start the bot
/register                     - add user to bot database for borders and default currency
/menu                         - access main menu for further aproach
/help                         - show this info
"""

MSG_STATIC = {'start': START_MESSAGE,
              'register': "You need to be registered to use this function!\nPlease consider using /register to add you user to the database.",
              'user_new': "User registered!\nWelcome! (:\n\nNow you can use the whole /menu !\n\n If you don´t want to use the bot anymore, might consider deleting your User.",
              'user_del': "User deleted from the database!\nThx for trying the bot! (:",
              'main': "What do you want to do?",
              'curr_select': "Which currency do you want to choose?",
              'curr_default': "Which currency should be the default?",
              'set_low': "Please set the LOW Border first!\n-\nOnly numbers are allowed!",
              'amount_new': "Please set your current amount of bitcoin!\n-\nOnly numbers are allowed! Also with commas (e.g. 0.001)\n\nnot checked yet from the bot!",
              'no_amount': "You do not have any amount set.\n--\nWhat do you want to do next?",
              'no_borders': "No borders set!\n--\nWhat do you want to do next?",
              'ticker_disable': "Ticker disables - borders unset!\nIf you want to enable it again please set new borders!",
              'error_high': "ERROR! -- HIGH border is lower than LOW border!\n-\nPlease set a new higher border.",
              'error_number': "sorry.. the given value is wrong! Are you sure it is a number?",
              'error_cmd': "Sorry unrecogniced message :/\n Maybe try /menu",
              'help': HELP_MSG
              }

MSG_DYNAMIC = {
    'low_set': "LOW Border set to %s\n--\nPlease tell me now the HIGH Border!\n-\n Need to be higher than LOW and a number!\n(The ticker will not work if only LOW is set!)",
    'high_set': "HIGH border set to %s!\nTicker is online!\n--\nWhat do you want to do next?",
    'amount_set': "Amount set to %s\n--\nWhat do you want to do next?",
    'borders': "Your Borders are:\nLow: %s\nHigh: %s\n--\nWhat do you want to do next?",
    'show_amount': "Your current Bitcoin amount is %s\n--\nWhat do you want to do next?",
    'default_changed': "Default changed to %s!\n--\nWhat do you want to do next?",
    'high_reached': "HIGH border reached %s %d %s",
    'low_reached': "LOW border reached %s %d %s",
    'curernt': "Current: %s %d %s\n--\nWhat do you want to do next?",
    'current+anount': "Current: %s %d %s\nYours: %d %s\n--\nWhat do you want to do next?"
}


def main():
    print("helper script to allfbot.py")


if __name__ == "__main__":
    main()
