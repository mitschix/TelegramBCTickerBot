from db.db_handler import db_read_borders, db_read_currency
from telegram.ext import ContextTypes
from utils.btc_query import get_btcrate_currency
from utils.messages import MSG_DYNAMIC


async def schedule_user_job(
    context: ContextTypes.DEFAULT_TYPE, user_id: int, hours: int
):
    await cancel_user_job(context, user_id)

    if hours <= 0:
        return

    context.job_queue.run_repeating(
        check_user_btc,
        interval=hours * 3600,
        first=0,
        chat_id=user_id,
        name=f"ticker_{user_id}",
    )


async def cancel_user_job(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    jobs = context.job_queue.get_jobs_by_name(f"ticker_{user_id}")
    for job in jobs:
        job.schedule_removal()


async def check_user_btc(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.chat_id

    borders = db_read_borders(user_id)
    if not borders:
        return

    low, high = borders
    if low is None or high is None:
        return

    curr = db_read_currency(user_id)
    btc_res, symbol = get_btcrate_currency(curr)

    if btc_res >= float(high):
        msg = MSG_DYNAMIC["high_reached"] % (curr, btc_res, symbol)
        await context.bot.send_message(chat_id=user_id, text=msg)

    elif btc_res <= float(low):
        msg = MSG_DYNAMIC["low_reached"] % (curr, btc_res, symbol)
        await context.bot.send_message(chat_id=user_id, text=msg)
