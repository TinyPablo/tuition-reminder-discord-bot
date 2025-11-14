from datetime import datetime, timedelta
import calendar

from bot.settings.logging_settings import logger
from bot.messages import MESSAGES_PL as MESSAGES


def validate_amount(new_value: int, current_value: int):
    errs = MESSAGES["errors"]

    if new_value <= 0:
        logger.debug("Validation failed: non-positive amount (%s)", new_value)
        return False, errs["amount_must_be_positive"]

    if new_value == current_value:
        logger.debug(
            "Validation failed: new amount equal to current (%s)",
            current_value
        )
        return False, errs["amount_same_as_current"].format(current=current_value)

    logger.debug("Validation passed: %s -> %s", current_value, new_value)
    return True, None


def select_reminder_message(days_left: int, date_str: str, amount: int):
    r = MESSAGES["reminders"]

    if days_left == 7:
        return r["week_before_due"].format(date=date_str, amount=amount)
    if days_left == 1:
        return r["day_before_due"].format(date=date_str, amount=amount)
    if days_left == 0:
        return r["due_today"].format(date=date_str, amount=amount)
    return None


def get_payment_amount(month: int, config: dict) -> int:
    return config["holiday"] if month in (7, 8) else config["normal"]


def get_next_date(current_date: datetime) -> datetime:
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    next_date = current_date + timedelta(days=1)
    if next_date.day > last_day:
        next_month = current_date.month + 1 if current_date.month < 12 else 1
        next_year = current_date.year + 1 if next_month == 1 else current_date.year
        next_date = next_date.replace(year=next_year, month=next_month, day=1)
    return next_date