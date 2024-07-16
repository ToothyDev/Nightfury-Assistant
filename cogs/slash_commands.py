import discord
from discord import slash_command, option

from utils import color_options


class SlashCommands(discord.Cog, name="slash_commands"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="Send an embed with up to three fields")
    @option("description", description="The description of the embed")
    @option("title", description="The title of the embed", required=False)
    @option("color", int, description="The color of the embed", choices=color_options, required=False,
            default=discord.Color.default())
    @option("image", discord.Attachment, description="The image of the embed", required=False)
    @option("thumbnail", bool, description="Make the image the thumbnail?", required=False, default=False)
    @option("field1", description="Title|Content of field 1", required=False)
    @option("field2", description="Title|Content of field 2", required=False)
    @option("field3", description="Title|Content of field 3", required=False)
    async def embed(self, ctx: discord.ApplicationContext, description: str, title: str, image: discord.Attachment,
                    thumbnail: bool, field1: str, field2: str, field3: str, color: discord.Color):
        embed = discord.Embed(title=title, description=description, color=color)
        if image:
            if not thumbnail:
                embed.set_image(url=image.url)
            else:
                embed.set_thumbnail(url=image.url)
        if field1:
            embed.add_field(name=field1.split("|")[0], value=field1.split("|")[1])
        if field2:
            embed.add_field(name=field2.split("|")[0], value=field2.split("|")[1])
        if field3:
            embed.add_field(name=field3.split("|")[0], value=field3.split("|")[1])

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(SlashCommands(bot))
