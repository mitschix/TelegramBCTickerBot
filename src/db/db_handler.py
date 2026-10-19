import os
import sqlite3
from typing import Optional, Tuple, List

# /data is the docker volume; DB_PATH overrides it for local runs
DB_NAME = os.getenv("DB_PATH", "/data/telfinbot_kb.sqlite")


def run(query: str, *params, one: bool = False, all: bool = False):
    """Generic helper for executing SQL with automatic connection handling."""
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute(query, params)
        if one:
            return cur.fetchone()
        if all:
            return cur.fetchall()
        conn.commit()
        return None


def db_create() -> None:
    run(
        """
        CREATE TABLE IF NOT EXISTS borders_btc (
            user INTEGER PRIMARY KEY,
            bd_low REAL,
            bd_high REAL,
            currency TEXT DEFAULT 'EUR',
            amount REAL,
            interval INTEGER DEFAULT 4
        )
        """
    )


def db_user_exist(user_id: int) -> bool:
    row = run("SELECT 1 FROM borders_btc WHERE user=? LIMIT 1", user_id, one=True)
    return row is not None


def db_user_create(user_id: int) -> None:
    if not db_user_exist(user_id):
        run(
            """
            INSERT INTO borders_btc (user, bd_low, bd_high, currency, amount, interval)
            VALUES (?, NULL, NULL, 'EUR', NULL, 4)
            """,
            user_id,
        )


def db_users() -> List[int]:
    rows = run("SELECT user FROM borders_btc", all=True)
    return [r[0] for r in rows]


def db_read_borders(user_id: int) -> Optional[Tuple[Optional[float], Optional[float]]]:
    return run(
        "SELECT bd_low, bd_high FROM borders_btc WHERE user=?",
        user_id,
        one=True,
    )


def db_read_currency(user_id: int) -> str:
    row = run("SELECT currency FROM borders_btc WHERE user=?", user_id, one=True)
    return row[0] if row else "EUR"


def db_read_amount(user_id: int) -> Optional[float]:
    row = run("SELECT amount FROM borders_btc WHERE user=?", user_id, one=True)
    return row[0] if row else None


def db_read_interval(user_id: int) -> int:
    row = run("SELECT interval FROM borders_btc WHERE user=?", user_id, one=True)
    return int(row[0]) if row and row[0] else 4


def db_set_currency(user_id: int, currency: str) -> None:
    run("UPDATE borders_btc SET currency=? WHERE user=?", currency, user_id)


def db_set_low(user_id: int, value: float) -> None:
    run("UPDATE borders_btc SET bd_low=? WHERE user=?", value, user_id)


def db_set_high(user_id: int, value: float) -> None:
    run("UPDATE borders_btc SET bd_high=? WHERE user=?", value, user_id)


def db_set_amount(user_id: int, value: float) -> None:
    run("UPDATE borders_btc SET amount=? WHERE user=?", value, user_id)


def db_set_interval(user_id: int, hours: int) -> None:
    run("UPDATE borders_btc SET interval=? WHERE user=?", hours, user_id)


def db_clear_borders(user_id: int) -> None:
    run(
        "UPDATE borders_btc SET bd_low=NULL, bd_high=NULL WHERE user=?",
        user_id,
    )


def db_delete_user(user_id: int) -> None:
    run("DELETE FROM borders_btc WHERE user=?", user_id)
