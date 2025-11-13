import discord
from bot.settings.discord_settings import CATEGORY_NAME


async def get_or_create_category(guild: discord.Guild) -> discord.CategoryChannel:
    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
    if not category:
        category = await guild.create_category(CATEGORY_NAME)
    return category


async def get_or_create_channel(guild: discord.Guild, name: str) -> discord.TextChannel:
    category = await get_or_create_category(guild)

    channel = discord.utils.get(category.channels, name=name)
    if channel:
        return channel

    existing = discord.utils.get(guild.text_channels, name=name)
    if existing and existing.category is None:
        await existing.edit(category=category)
        return existing

    return await category.create_text_channel(name)