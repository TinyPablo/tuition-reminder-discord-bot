from bot.messages import MESSAGES_PL

REMINDER_KEYS = {
    "reminder_week_before_due",
    "reminder_day_before_due",
    "reminder_due_today",
}

BROADCAST_KEYS = {
    "admin_broadcast_normal_payment_changed",
    "admin_broadcast_holiday_payment_changed",
}

CONFIRM_KEYS = {
    "user_confirm_normal_payment_updated",
    "user_confirm_holiday_payment_updated",
}

SYSTEM_KEYS = {
    "system_config_saved",
}


def test_message_placeholders():
    for key, text in MESSAGES_PL.items():

        if key in REMINDER_KEYS:
            assert "{date}" in text
            assert "{amount}" in text

        elif key in BROADCAST_KEYS:
            assert "{value}" in text
            assert "{user}" in text

        elif key in CONFIRM_KEYS:
            assert "{value}" in text

        elif key in SYSTEM_KEYS:
            assert "{" not in text 