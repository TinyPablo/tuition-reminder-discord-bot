import pytest
from datetime import datetime
from bot.main import get_payment_amount, get_next_date, validate_amount


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
    
    
def test_validate_amount_positive_change():
    ok, msg = validate_amount(700, 650)
    assert ok is True
    assert msg is None


def test_validate_amount_zero():
    ok, msg = validate_amount(0, 650)
    assert ok is False
    assert "musi być większa niż 0" in msg


def test_validate_amount_negative():
    ok, msg = validate_amount(-50, 650)
    assert ok is False
    assert "musi być większa niż 0" in msg


def test_validate_amount_same_value():
    ok, msg = validate_amount(650, 650)
    assert ok is False
    assert "taka sama jak obecna" in msg