import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    breakpoint()
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Parse the message content
    content = message.content
    author = message.author
    channel = message.channel
    breakpoint()

    # Your parsing logic here

bot.run("MTE2MzAyMDUzMDI0OTY0NjExMA.GT30Cm.3LBqqz6j5pDJG5BFR15gnhGm-UBpiFI-Va9GGg", bot=False)
