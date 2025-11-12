from bot.main import select_reminder_message
from bot.messages import MESSAGES_PL as MESSAGES


def test_week_before_due_message():
    msg = select_reminder_message(7, "2025-11-24", 650, MESSAGES)
    print(msg, type(msg))
    assert "📅" in msg
    assert "650" in msg
    assert "2025-11-24" in msg


def test_day_before_due_message():
    msg = select_reminder_message(1, "2025-11-30", 650, MESSAGES)
    assert "⚠️" in msg
    assert "650" in msg


def test_due_today_message():
    msg = select_reminder_message(0, "2025-11-30", 650, MESSAGES)
    assert "🚨" in msg
    assert "650" in msg


def test_no_message_other_days():
    msg = select_reminder_message(5, "2025-11-20", 650, MESSAGES)
    assert msg is None