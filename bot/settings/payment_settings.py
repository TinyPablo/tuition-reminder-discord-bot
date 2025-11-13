import json
import os
from bot.settings.paths import PAYMENT_CONFIG_FILE

DEFAULT_CONFIG = {
    "normal": 650,
    "holiday": 350,
}


def load_payment_config() -> dict:
    if not os.path.exists(PAYMENT_CONFIG_FILE):
        save_payment_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(PAYMENT_CONFIG_FILE, "r") as f:
        return json.load(f)


def save_payment_config(data: dict):
    with open(PAYMENT_CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)