import discord
from discord.ext import commands, tasks
from discord import app_commands
import calendar
import json
import os

from datetime import datetime, timedelta
from bot.messages import MESSAGES_PL as MESSAGES
from bot.config import CATEGORY_NAME, DISCORD_TOKEN, GUILD_ID, CHANNEL_NAME, MANAGER_ROLE_ID


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "payment_config.json")


def validate_amount(new_value: int, current_value: int):
    errs = MESSAGES["errors"]

    if new_value <= 0:
        return False, errs["amount_must_be_positive"]

    if new_value == current_value:
        return False, errs["amount_same_as_current"].format(current=current_value)

    return True, None


def select_reminder_message(days_left: int, date_str: str, amount: int, messages: dict):
    r = messages["reminders"]

    if days_left == 7:
        return r["week_before_due"].format(date=date_str, amount=amount)
    if days_left == 1:
        return r["day_before_due"].format(date=date_str, amount=amount)
    if days_left == 0:
        return r["due_today"].format(date=date_str, amount=amount)
    return None


def manager_only():
    async def predicate(interaction: discord.Interaction):
        return any(r.id == MANAGER_ROLE_ID for r in interaction.user.roles)
    return app_commands.check(predicate)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        data = {"normal": 650, "holiday": 350}
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
        return data
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


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


def run_bot():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)
    current_date = datetime(2025, 1, 20)
    config = load_config()

    @bot.event
    async def on_ready():
        guild_obj = discord.Object(id=GUILD_ID)
        await bot.tree.sync(guild=guild_obj)
        print(f"[INFO] Synced commands to guild {GUILD_ID}")
        print(f"[INFO] Logged in as {bot.user}")
        simulate_days.start()
        
        
    @bot.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error):
        from discord.app_commands import CheckFailure

        if isinstance(error, CheckFailure):
            await interaction.response.send_message(
                MESSAGES["errors"]["missing_manager_role"].format(role_id=MANAGER_ROLE_ID),
                ephemeral=True
            )
            return


    async def get_or_create_category(guild: discord.Guild, name: str) -> discord.CategoryChannel:
        category = discord.utils.get(guild.categories, name=name)
        if not category:
            category = await guild.create_category(name)
            # await category.edit(position=len(guild.categories) - 1)
        return category

    
    async def get_or_create_channel(guild: discord.Guild, name: str) -> discord.TextChannel:
        category = await get_or_create_category(guild, CATEGORY_NAME)

        channel = discord.utils.get(category.channels, name=name)
        if channel:
            return channel

        existing = discord.utils.get(guild.text_channels, name=name)
        if existing and existing.category is None:
            await existing.edit(category=category)
            return existing

        channel = await category.create_text_channel(name)
        return channel


    @bot.tree.command(
        name="set_normal", 
        description="Set the normal (non-holiday) monthly payment amount",
        guild=discord.Object(id=GUILD_ID),
    )
    @manager_only()
    async def set_normal(interaction: discord.Interaction, value: int):
        is_valid, error_message = validate_amount(value, config["normal"])

        if not is_valid:
            await interaction.response.send_message(error_message, ephemeral=True)
            return

        config["normal"] = value
        save_config(config)

        await interaction.response.send_message(
            MESSAGES["confirmations"]["normal_payment_updated"].format(value=value),
            ephemeral=True
        )

        channel = await get_or_create_channel(interaction.guild, CHANNEL_NAME)
        await channel.send(
            MESSAGES["broadcasts"]["normal_payment_changed"].format(value=value)
        )


    @bot.tree.command(
        name="set_holiday",
        description="Set the holiday (July/August) monthly payment amount",
        guild=discord.Object(id=GUILD_ID),
    )
    @manager_only()
    async def set_holiday(interaction: discord.Interaction, value: int):
        is_valid, error_message = validate_amount(value, config["holiday"])

        if not is_valid:
            await interaction.response.send_message(error_message, ephemeral=True)
            return

        config["holiday"] = value
        save_config(config)

        await interaction.response.send_message(
            MESSAGES["confirmations"]["holiday_payment_updated"].format(value=value),
            ephemeral=True
        )

        channel = await get_or_create_channel(interaction.guild, CHANNEL_NAME)
        await channel.send(
            MESSAGES["broadcasts"]["holiday_payment_changed"].format(value=value)
        )
        
        
    @bot.tree.command(
        name="debug_status",
        description="Show internal bot debug information (manager only).",
        guild=discord.Object(id=GUILD_ID)
    )
    @manager_only()
    async def debug_status(interaction: discord.Interaction):
        guild = interaction.guild

        category = discord.utils.get(guild.categories, name=CATEGORY_NAME)

        channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)

        normal = config.get("normal")
        holiday = config.get("holiday")

        has_role = any(r.id == MANAGER_ROLE_ID for r in interaction.user.roles)

        msg = (
            "### 🧩 Debug — Tuition Reminder Bot\n"
            f"**Guild ID:** `{GUILD_ID}`\n\n"

            "#### 💰 Payment configuration\n"
            f"- Normal payment: **{normal} zł**\n"
            f"- Holiday payment: **{holiday} zł**\n\n"

            "#### 📁 Category\n"
            f"- Name: **{CATEGORY_NAME}**\n"
            f"- Exists: **{category is not None}**\n"
            f"- ID: `{category.id if category else 'N/A'}`\n\n"

            "#### 💬 Channel\n"
            f"- Name: **{CHANNEL_NAME}**\n"
            f"- Exists: **{channel is not None}**\n"
            f"- ID: `{channel.id if channel else 'N/A'}`\n"
            f"- Category matched: **{channel.category.id == category.id if (channel and category) else 'N/A'}**\n\n"

            "#### 🔐 Role\n"
            f"- Manager role ID: `{MANAGER_ROLE_ID}`\n"
            f"- User has role: **{has_role}**\n\n"

            "#### 🗂 Config file\n"
            f"- Path: `{CONFIG_FILE}`\n"
        )

        await interaction.response.send_message(msg, ephemeral=True)
       

    @tasks.loop(seconds=1)
    async def simulate_days():
        nonlocal current_date
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            return

        channel = await get_or_create_channel(guild, CHANNEL_NAME)
        last_day = calendar.monthrange(current_date.year, current_date.month)[1]
        days_left = last_day - current_date.day
        amount = get_payment_amount(current_date.month, config)
        date_str = current_date.strftime("%Y-%m-%d")

        msg = select_reminder_message(days_left, date_str, amount, MESSAGES)

        if msg:
            await channel.send(msg)

        current_date = get_next_date(current_date)

    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    run_bot()