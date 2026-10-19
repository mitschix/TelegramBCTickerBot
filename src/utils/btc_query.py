import requests

CURR_LIST = ["EUR", "USD", "CHF", "CAD", "RUB", "BRL"]
BLOCKCHAIN_URL = "https://blockchain.info"


def get_btcrate_currency(curr: str = "EUR") -> float:
    r = requests.get(f"{BLOCKCHAIN_URL}/ticker", timeout=10)
    r.raise_for_status()
    all_info = r.json()
    return float(all_info[curr]["last"])
