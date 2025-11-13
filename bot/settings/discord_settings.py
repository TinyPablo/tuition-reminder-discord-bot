import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_NAME = os.getenv("CHANNEL_NAME")
CATEGORY_NAME = os.getenv("CATEGORY_NAME")
MANAGER_ROLE_ID = int(os.getenv("MANAGER_ROLE_ID"))