"""Smoke tests: message templates, db layer, job rescheduling.

Runs with pytest, or standalone: python tests/test_smoke.py
"""
import asyncio
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# DB_PATH must be set before db_handler is imported (read at import time)
_tmp = tempfile.mkdtemp(prefix="bcticker-test-")
os.environ["DB_PATH"] = os.path.join(_tmp, "test.sqlite")

import db.db_handler as db  # noqa: E402
from handlers import jobs  # noqa: E402
from handlers.conversations import CURRENT, HIGH, LOW  # noqa: E402
from utils.messages import MSG_DYNAMIC  # noqa: E402


def test_conversation_constants():
    assert (LOW, HIGH, CURRENT) == (0, 1, 2)


def test_msg_dynamic_templates_format():
    # one entry per template; new templates must be added here too
    args = {
        "low_set": (5000.0,),
        "high_set": (6000.0,),
        "amount_set": (0.5,),
        "borders": (5000.0, 6000.0),
        "show_amount": (0.5,),
        "default_changed": ("EUR",),
        "high_reached": ("EUR", 60000.5, "€"),
        "low_reached": ("EUR", 50000.5, "€"),
        "current": ("EUR", 60000.5, "€"),
        "current+amount": ("EUR", 60000.5, "€", 0.5, "€"),
        "interval_set": (4,),
    }
    assert set(MSG_DYNAMIC) == set(args), "template/args keys out of sync"
    for key, template in MSG_DYNAMIC.items():
        template % args[key]  # raises TypeError on %-count mismatch


def test_db_user_flow_roundtrip():
    db.db_create()
    db.db_create()  # idempotent

    assert not db.db_user_exist(11)
    db.db_user_create(11)
    assert db.db_user_exist(11)

    db.db_set_low(11, 5000.0)
    db.db_set_high(11, 6000.0)
    db.db_set_currency(11, "USD")
    db.db_set_amount(11, 0.5)
    db.db_set_interval(11, 12)

    assert db.db_read_borders(11) == (5000.0, 6000.0)
    assert db.db_read_currency(11) == "USD"
    assert db.db_read_amount(11) == 0.5
    assert db.db_read_interval(11) == 12

    db.db_clear_borders(11)
    assert db.db_read_borders(11) == (None, None)

    db.db_delete_user(11)
    assert not db.db_user_exist(11)


class _FakeJobQueue:
    def __init__(self):
        self.jobs = []

    def run_repeating(self, callback, interval, first, chat_id, name=None):
        self.jobs.append((chat_id, interval, callback))

    def get_jobs_by_name(self, name):
        return []


class _FakeContext:
    def __init__(self):
        self.job_queue = _FakeJobQueue()


def test_reschedule_user_jobs_on_boot():
    db.db_create()
    # 21: borders set, interval 4 -> gets a job
    # 22: no borders -> none
    # 23: interval disabled -> none
    db.db_user_create(21)
    db.db_set_low(21, 1.0)
    db.db_set_high(21, 2.0)
    db.db_user_create(22)
    db.db_user_create(23)
    db.db_set_high(23, 2.0)
    db.db_set_interval(23, 0)

    context = _FakeContext()
    asyncio.run(jobs.reschedule_user_jobs(context))

    jobs_scheduled = context.job_queue.jobs
    assert len(jobs_scheduled) == 1
    chat_id, interval, _callback = jobs_scheduled[0]
    assert chat_id == 21
    assert interval == 4 * 3600


if __name__ == "__main__":
    test_conversation_constants()
    test_msg_dynamic_templates_format()
    test_db_user_flow_roundtrip()
    test_reschedule_user_jobs_on_boot()
    print("all smoke tests passed")
