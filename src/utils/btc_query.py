from typing import Tuple

import requests

CURR_LIST = ["EUR", "USD", "CHF", "CAD", "RUB", "BRL"]
BLOCKCHAIN_URL = "https://blockchain.info"


def get_btcrate_currency(curr: str = "EUR") -> Tuple[float, str]:
    r = requests.get(f"{BLOCKCHAIN_URL}/ticker", timeout=10)
    r.raise_for_status()
    all_info = r.json()
    info = all_info[curr]
    return float(info["last"]), info["symbol"]


def conv_curr_in_btc(val: float, curr: str = "EUR") -> str:
    params = {"currency": curr, "value": val}
    r = requests.get(f"{BLOCKCHAIN_URL}/tobtc", params=params, timeout=10)
    r.raise_for_status()
    btc_val = r.text
    return f"Value for {val} in {curr} is: {btc_val} BTC"
