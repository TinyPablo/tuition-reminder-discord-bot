import discord
from discord.ext import commands, tasks
from discord import app_commands
import calendar
import json
import os

from datetime import datetime, timedelta
from bot.messages import MESSAGES_PL as MESSAGES
from bot.config import DISCORD_TOKEN, GUILD_ID, CHANNEL_NAME, MANAGER_ROLE_ID


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "payment_config.json")


def select_reminder_message(days_left: int, date_str: str, amount: int, messages: dict) -> str | None:
        if days_left == 7:
            return messages["reminder_week_before_due"].format(date=date_str, amount=amount)
        elif days_left == 1:
            return messages["reminder_day_before_due"].format(date=date_str, amount=amount)
        elif days_left == 0:
            return messages["reminder_due_today"].format(date=date_str, amount=amount)
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
                MESSAGES["error_missing_manager_role"].format(role_id=MANAGER_ROLE_ID),
                ephemeral=True
            )
            return


    async def get_or_create_channel(guild: discord.Guild, name: str) -> discord.TextChannel:
        ch = discord.utils.get(guild.text_channels, name=name)
        if not ch:
            ch = await guild.create_text_channel(name)
        return ch


    @bot.tree.command(
        name="set_normal",
        description="Set the normal (non-holiday) monthly payment amount",
        guild=discord.Object(id=GUILD_ID),
    )
    @manager_only()
    async def set_normal(interaction: discord.Interaction, value: int):
        config["normal"] = value
        save_config(config)

        await interaction.response.send_message(
            MESSAGES["confirm_normal_payment_updated"].format(value=value),
            ephemeral=True
        )

        channel = await get_or_create_channel(interaction.guild, CHANNEL_NAME)
        await channel.send(
            MESSAGES["broadcast_normal_payment_changed"].format(
                value=value
            )
        )


    @bot.tree.command(
        name="set_holiday",
        description="Set the holiday (July/August) monthly payment amount",
        guild=discord.Object(id=GUILD_ID),
    )
    @manager_only()
    async def set_holiday(interaction: discord.Interaction, value: int):
        config["holiday"] = value
        save_config(config)

        await interaction.response.send_message(
            MESSAGES["confirm_holiday_payment_updated"].format(value=value),
            ephemeral=True
        )

        channel = await get_or_create_channel(interaction.guild, CHANNEL_NAME)
        await channel.send(
            MESSAGES["broadcast_holiday_payment_changed"].format(
                value=value
            )
        )
       

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