from discord import app_commands
from bot.settings.discord_settings import MANAGER_ROLE_ID


def manager_only():
    async def predicate(interaction):
        return any(r.id == MANAGER_ROLE_ID for r in interaction.user.roles)
    return app_commands.check(predicate)