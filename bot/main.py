import discord
from discord.ext import commands, tasks
import calendar

from datetime import datetime, timedelta
from bot.messages import MESSAGES_PL as MESSAGES
from bot.config import DISCORD_TOKEN, GUILD_ID, CHANNEL_NAME


def get_payment_amount(month: int) -> int:
    return 350 if month in (7, 8) else 650


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

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")
        simulate_days.start()

    async def get_or_create_channel(guild: discord.Guild, name: str) -> discord.TextChannel:
        ch = discord.utils.get(guild.text_channels, name=name)
        if not ch:
            ch = await guild.create_text_channel(name)
        return ch

    @tasks.loop(seconds=1)
    async def simulate_days():
        nonlocal current_date
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            return

        channel = await get_or_create_channel(guild, CHANNEL_NAME)
        last_day = calendar.monthrange(current_date.year, current_date.month)[1]
        days_left = last_day - current_date.day
        amount = get_payment_amount(current_date.month)
        date_str = current_date.strftime("%Y-%m-%d")

        if days_left == 7:
            msg = MESSAGES["week_left"].format(date=date_str, amount=amount)
        elif days_left == 1:
            msg = MESSAGES["day_left"].format(date=date_str, amount=amount)
        elif days_left == 0:
            msg = MESSAGES["due_today"].format(date=date_str, amount=amount)
        else:
            msg = None

        if msg:
            await channel.send(msg)

        current_date = get_next_date(current_date)

    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    run_bot()