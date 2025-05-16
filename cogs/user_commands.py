import discord
from discord import user_command


class UserCommands(discord.Cog, name="user_commands"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @user_command()
    async def avatar(self, ctx: discord.ApplicationContext, member: discord.Member) -> None:
        user = await self.bot.fetch_user(member.id)  # Color attribute is only available via fetch
        embed = discord.Embed(color=user.accent_color)
        embed.set_image(url=member.display_avatar.with_size(4096))
        embed.set_footer(text="Nightfury Assistant", icon_url=self.bot.user.avatar.url)
        await ctx.respond(embed=embed, ephemeral=True)

    @user_command()
    async def banner(self, ctx: discord.ApplicationContext, member: discord.Member) -> None:
        user = await self.bot.fetch_user(member.id)  # Banner is only available via fetch
        embed = discord.Embed(color=user.accent_color)
        if not user.banner:
            await ctx.respond("Member has no banner set!", ephemeral=True)
            return
        embed.set_image(url=user.banner.with_size(4096))
        embed.set_footer(text="Nightfury Assistant", icon_url=self.bot.user.avatar.url)
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(UserCommands(bot))
