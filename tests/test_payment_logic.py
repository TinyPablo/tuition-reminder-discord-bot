import pytest
from datetime import datetime
from bot.main import get_payment_amount, get_next_date


def test_payment_amounts():
    cfg = {"normal": 650, "holiday": 350}

    assert get_payment_amount(1, cfg) == 650
    assert get_payment_amount(7, cfg) == 350
    assert get_payment_amount(8, cfg) == 350
    assert get_payment_amount(12, cfg) == 650


def test_next_date_same_month():
    d = datetime(2025, 1, 30)
    result = get_next_date(d)
    assert result.day == 31
    assert result.month == 1


def test_next_date_rollover_february():
    d = datetime(2025, 2, 28)
    result = get_next_date(d)
    assert result.month == 3
    assert result.day == 1


def test_next_date_rollover_december():
    d = datetime(2025, 12, 31)
    result = get_next_date(d)
    assert result.year == 2026
    assert result.month == 1
    assert result.day == 1