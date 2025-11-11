import calendar
from datetime import datetime
from bot.main import get_payment_amount
from bot.messages import MESSAGES_PL

def get_test_message(days_left, amount, date_str):
    if days_left == 7:
        return MESSAGES_PL["week_left"].format(date=date_str, amount=amount)
    elif days_left == 1:
        return MESSAGES_PL["day_left"].format(date=date_str, amount=amount)
    elif days_left == 0:
        return MESSAGES_PL["due_today"].format(date=date_str, amount=amount)
    return None

def test_message_selection():
    date_str = "2025-11-24"
    msg = get_test_message(7, 650, date_str)
    assert "📅" in msg
    assert "650" in msg

    msg = get_test_message(1, 650, date_str)
    assert "⚠️" in msg

    msg = get_test_message(0, 650, date_str)
    assert "🚨" in msg