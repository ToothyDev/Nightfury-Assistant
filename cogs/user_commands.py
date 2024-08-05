import discord
from discord import user_command

from utils import Colors


class UserCommands(discord.Cog, name="user_commands"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @user_command()
    async def avatar(self, ctx: discord.ApplicationContext, member: discord.Member):
        embed = discord.Embed(color=Colors.tailfin)
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text="Nightfury Assistant", icon_url=self.bot.user.avatar.url)
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(UserCommands(bot))
