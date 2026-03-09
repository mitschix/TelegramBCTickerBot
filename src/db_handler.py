import sqlite3
from typing import Union

DB_NAME = "telfinbot_kb.sqlite"


def db_create() -> None:
    db_query("CREATE TABLE borders_btc (user,bd_low,bd_high,cnt,currency,amount)")


def db_query(qry: str) -> list:
    print(qry)
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        resc = c.execute(qry)
        conn.commit()
        return [row for row in resc]


def db_user_exist(user_id: int) -> bool:
    resp = db_query(f"SELECT user from borders_btc WHERE user={user_id}")
    users = [user for user in resp if user_id in user]
    if users:
        return True
    return False


def db_user_create(user_id: int) -> None:
    if not db_user_exist(user_id):
        db_query(f"INSERT INTO borders_btc (user,bd_low,bd_high,cnt,currency,amount) values({user_id}, NULL, NULL, 0, 'EUR',NULL)")


def db_users() -> list[int]:
    users = []
    resp = db_query("SELECT user from borders_btc")
    users = [user[0] for user in resp]
    return users


def db_read(usr: int, method: str):
    mapping = {
        "borders": "bd_low,bd_high",
        "currency": "currency",
        "count": "cnt",
        "showamount": "amount",
    }

    sql = "SELECT {} FROM borders_btc WHERE user={}".format(
        mapping[method], usr)
    resp = db_query(sql)
    return resp


def db_change(usr: int, method: str, info: Union[str, float, int] = None) -> None:
    methods = {
        "currency": "Update borders_btc SET currency='{}' WHERE user={}".format(info, usr),
        "cnt_reset": "UPDATE borders_btc SET cnt=0 WHERE user={}".format(usr),
        "cnt_inc": "UPDATE borders_btc SET cnt=cnt+1 WHERE user={}".format(usr),
        "deluser": "DELETE from borders_btc WHERE user={}".format(usr),
        "delborders": "UPDATE borders_btc SET bd_low=Null,bd_high=Null WHERE user={}".format(usr),
        "lowborder": "UPDATE borders_btc SET bd_low={} WHERE user={}".format(info, usr),
        "highborder": "UPDATE borders_btc SET bd_high={} WHERE user={}".format(info, usr),
        "chamount": "UPDATE borders_btc SET amount={} WHERE user={}".format(info, usr)
    }
    db_query(methods[method])
