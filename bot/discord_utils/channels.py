import discord
from bot.settings.discord_settings import CATEGORY_NAME
from bot.settings.logging_settings import logger


async def get_or_create_category(guild: discord.Guild) -> discord.CategoryChannel:
    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
    if not category:
        logger.info(
            "Creating category '%s' in guild %s",
            CATEGORY_NAME, guild.id
        )
        category = await guild.create_category(CATEGORY_NAME)
    return category


async def get_or_create_channel(guild: discord.Guild, name: str) -> discord.TextChannel:
    category = await get_or_create_category(guild)

    channel = discord.utils.get(category.channels, name=name)
    if channel:
        return channel

    existing = discord.utils.get(guild.text_channels, name=name)
    if existing and existing.category is None:
        logger.info(
            "Moving existing channel '%s' into category '%s' in guild %s",
            name, CATEGORY_NAME, guild.id
        )
        await existing.edit(category=category)
        return existing

    logger.info(
        "Creating new channel '%s' in category '%s' in guild %s",
        name, CATEGORY_NAME, guild.id
    )
    return await category.create_text_channel(name)