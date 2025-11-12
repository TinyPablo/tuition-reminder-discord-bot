import os
import dotenv

dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
MANAGER_ROLE_ID = int(os.getenv("MANAGER_ROLE_ID", "0"))

