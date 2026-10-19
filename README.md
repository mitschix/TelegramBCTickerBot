# Telegram BitCoin Ticker Bot

Tiny bot to track bitcoin with borders (low/high price alerts), per-user check
intervals and different currencies. Checkout the result [here](https://t.me/all_finance_bot). (:

## Configuration (environment variables)

| Variable   | Required | Description                                                        |
| ---------- | -------- | ------------------------------------------------------------------ |
| `BOT_TOKEN` | yes      | from [@BotFather](https://t.me/BotFather)                          |
| `ADMIN_ID`  | no       | chat id that gets notified about new registrations                  |
| `DB_PATH`   | no       | sqlite file, default `/data/telfinbot_kb.sqlite` (docker volume)    |

## Run with podman / docker

```sh
podman build -f docker/Dockerfile .
podman run -d --restart unless-stopped \
  -v btcdata:/data \
  -e BOT_TOKEN=123:abc -e ADMIN_ID=123456789 \
  localhost/<image-name>
```

Note: build from the repo root — the Dockerfile needs `src/` as build context.

## Run locally

```sh
python -m venv .venv && .venv/bin/pip install -r src/requirements.txt
cd src
BOT_TOKEN=123:abc python bot.py
```

## Tests

```sh
pip install pytest
pytest tests/
```
