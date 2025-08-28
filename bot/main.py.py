import os
import discord
import aiohttp
from discord.ext import tasks, commands

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1196023684633202751
UNIVERSE_ID = 7257273362

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def fetch_playercount():
    url = f"https://games.roblox.com/v1/games?universeIds={UNIVERSE_ID}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data["data"][0]["playing"]
            return None

@tasks.loop(minutes=1)
async def update_embed():
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None or not hasattr(bot, "status_message"):
        return

    count = await fetch_playercount()
    if count is None:
        description = "⚠️ Could not fetch player count."
    else:
        description = f"👥 Current Players: **{count}**"

    embed = discord.Embed(
        title="Roblox Game Player Count",
        description=description,
        color=discord.Color.blurple()
    )

    await bot.status_message.edit(embed=embed)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        # Send one embed only when bot first connects
        count = await fetch_playercount()
        if count is None:
            description = "⚠️ Could not fetch player count."
        else:
            description = f"👥 Current Players: **{count}**"

        embed = discord.Embed(
            title="Roblox Game Player Count",
            description=description,
            color=discord.Color.blurple()
        )

        bot.status_message = await channel.send(embed=embed)

    update_embed.start()

bot.run(TOKEN)

