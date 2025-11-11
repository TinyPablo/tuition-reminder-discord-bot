import random
import discord
from discord.ext import commands, tasks

from config import DISCORD_TOKEN
from config import GUILD_ID
from config import CHANNEL_NAME
 

def run_bot():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")
        test_loop.start()

    async def get_or_create_channel(guild: discord.Guild, name: str) -> discord.TextChannel:
        ch = discord.utils.get(guild.text_channels, name=name)
        if not ch:
            ch = await guild.create_text_channel(name)
        return ch


    @tasks.loop(seconds=1)
    async def test_loop():
        guild = bot.get_guild(GUILD_ID)
        print(guild) # None
        if not guild:
            return

        channel = await get_or_create_channel(guild, CHANNEL_NAME)
        
        msg = f"message {random.random()}"
        
        if msg:
            await channel.send(msg)
        
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    run_bot()