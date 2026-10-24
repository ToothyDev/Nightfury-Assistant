import logging

import discord

import log_setup
from config import BOT_TOKEN

log_setup.setup_logging(logging.INFO)
log = logging.getLogger(__name__)

bot = discord.Bot(intents=discord.Intents.default(),
                  default_command_integration_types=[discord.IntegrationType.user_install])

bot.load_extensions("cogs")
log.info("Loaded cogs: " + ', '.join(bot.cogs))


@bot.listen()
async def on_connect():
    log.info('Connected to Discord!')


@bot.listen()
async def on_ready():
    log.info(f'Logged in as {bot.user}')
    log.info('------')


bot.run(BOT_TOKEN)
