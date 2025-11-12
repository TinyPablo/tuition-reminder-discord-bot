from datetime import datetime
from bot.messages import MESSAGES_PL


def generate_test_message(days_left, amount, date_str):

    if days_left == 7:
        return MESSAGES_PL["reminder_week_before_due"].format(date=date_str, amount=amount)

    if days_left == 1:
        return MESSAGES_PL["reminder_day_before_due"].format(date=date_str, amount=amount)

    if days_left == 0:
        return MESSAGES_PL["reminder_due_today"].format(date=date_str, amount=amount)

    return None


def test_message_selection():
    date_str = "2025-11-24"
    amount = 650

    msg = generate_test_message(7, amount, date_str)
    assert "📅" in msg
    assert str(amount) in msg

    msg = generate_test_message(1, amount, date_str)
    assert "⚠️" in msg

    msg = generate_test_message(0, amount, date_str)
    assert "🚨" in msg