import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PAYMENT_CONFIG_FILE = os.path.join(BASE_DIR, "payment_config.json")
LOGS_DIR = os.path.join(BASE_DIR, "../logs")