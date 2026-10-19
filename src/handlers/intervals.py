from db.db_handler import db_set_interval
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils.keyboards import KEYBOARDS

from .jobs import cancel_user_job, schedule_user_job


async def handle_opt_interval(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: str, user_id: int
):
    query = update.callback_query
    hours = int(data)

    if hours == 0:
        db_set_interval(user_id, 0)
        await cancel_user_job(context, user_id)
        await query.edit_message_text(
            "Notifications disabled.",
            reply_markup=InlineKeyboardMarkup(KEYBOARDS["ticker"]),
        )
        return

    db_set_interval(user_id, hours)
    await schedule_user_job(context, user_id, hours)

    await query.edit_message_text(
        f"Interval set to every {hours} hours.",
        reply_markup=InlineKeyboardMarkup(KEYBOARDS["ticker"]),
    )
