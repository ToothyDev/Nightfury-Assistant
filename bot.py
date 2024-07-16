import discord

from config import token

bot = discord.Bot(intents=discord.Intents.default(),
                  default_command_integration_types=[discord.IntegrationType.user_install])

bot.load_extensions("cogs")  # Loads all cogs in the cogs folder
print(bot.extensions)
BOOTED = False


@bot.listen()
async def on_connect():
    print('Connected to Discord!')


@bot.listen()
async def on_ready():
    global BOOTED
    if BOOTED:
        print("Reconnect(?)")
    if not BOOTED:
        # await bot.sync_commands() #You might need to uncomment this if the slash commands aren't appearing
        print(f'Logged in as {bot.user}')
        print('------')
        BOOTED = True


bot.run(token)
