import discord
from discord import user_command


class UserCommands(discord.Cog, name="user_commands"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(UserCommands(bot))
