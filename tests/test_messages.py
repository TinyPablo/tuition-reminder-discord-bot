from bot.messages import MESSAGES_PL


def flatten_messages(data, prefix=""):
    flat = {}
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten_messages(value, prefix=full_key))
        else:
            flat[full_key] = value
    return flat


def test_message_structure_not_empty():
    assert isinstance(MESSAGES_PL, dict)
    assert len(MESSAGES_PL) > 0


def test_messages_not_empty():
    flat = flatten_messages(MESSAGES_PL)
    for msg in flat.values():
        assert isinstance(msg, str)
        assert msg.strip() != ""


def test_reminder_placeholders():
    reminders = MESSAGES_PL["reminders"]

    required = {"{date}", "{amount}"}
    for key, msg in reminders.items():
        for placeholder in required:
            assert placeholder in msg, f"Missing {placeholder} in reminders.{key}"


def test_broadcast_placeholders():
    broadcasts = MESSAGES_PL["broadcasts"]

    required = {"{value}"}
    for key, msg in broadcasts.items():
        for placeholder in required:
            assert placeholder in msg, f"Missing {placeholder} in broadcasts.{key}"


def test_confirmation_placeholders():
    confirmations = MESSAGES_PL["confirmations"]

    required = {"{value}"}
    for key, msg in confirmations.items():
        for placeholder in required:
            assert placeholder in msg, f"Missing {placeholder} in confirmations.{key}"


def test_error_placeholders():
    errors = MESSAGES_PL["errors"]

    for key, msg in errors.items():
        if key == "missing_manager_role":
            assert "{role_id}" in msg
        elif key == "amount_same_as_current":
            assert "{current}" in msg
        else:
            assert "{" not in msg or msg.count("{") == 0


def test_system_messages_have_no_placeholders():
    system = MESSAGES_PL["system"]

    for key, msg in system.items():
        assert "{" not in msg, f"System message '{key}' shouldn't contain placeholders"