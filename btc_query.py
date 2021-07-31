import requests

CURR_LIST = ["EUR", "USD", "CHF", "CAD", "RUB", "BRL"]


def get_btcrate_currency(curr: str = 'EUR') -> tuple[float, str]:
    url_blockchain = "https://blockchain.info/ticker"
    r = requests.get(url_blockchain)
    all_info = r.json()
    euro_info = all_info[curr]
    return euro_info['last'], euro_info['symbol']


def conv_curr_in_btc(val: int, curr: str = 'EUR') -> str:
    url_blockchain = "https://blockchain.info/tobtc?currency={}&value={}".format(curr, val)
    r = requests.get(url_blockchain)
    btc_val = r.text
    return "Value for {} in {} is: {} BTC".format(val, curr, btc_val)


def main() -> None:
    val = 50  # TODO variable
    currency = None  # TODO variable
    if not currency:
        currency = 'EUR'
    bc_res, symbol = get_btcrate_currency(currency)
    conv_result = conv_curr_in_btc(val, currency)

    print("Current value for {} is: {} {}".format(currency, bc_res, symbol))


if __name__ == '__main__':
    main()
