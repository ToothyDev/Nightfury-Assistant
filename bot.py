import discord

from config import token

bot = discord.Bot(intents=discord.Intents.default(),
                  default_command_integration_types=[discord.IntegrationType.user_install])

bot.load_extensions("cogs")
print("Loaded cogs: " + ', '.join(bot.cogs))


@bot.listen()
async def on_connect():
    print('Connected to Discord!')


@bot.listen()
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------')


bot.run(token)
