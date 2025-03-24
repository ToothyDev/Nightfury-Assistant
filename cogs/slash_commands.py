import datetime

import discord
from discord import slash_command, option

from utils import Colors


class SlashCommands(discord.Cog, name="slash_commands"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="Send an embed with up to three fields")
    @option("description", description="The description of the embed")
    @option("title", description="The title of the embed", required=False)
    @option("color", int, description="The color of the embed",
            autocomplete=discord.utils.basic_autocomplete(Colors.color_options), required=False,
            default=discord.Color.default())
    @option("image", discord.Attachment, description="The image of the embed", required=False)
    @option("thumbnail", bool, description="Make the image show as thumbnail?", required=False, default=False)
    @option("author", description="Set the author name", required=False)
    @option("author_url", description="Set the author url", required=False)
    @option("author_icon_url", description="Set the author icon url", required=False)
    @option("footer", description="Set the footer text", required=False)
    @option("footer_icon_url", description="Set the footer icon url", required=False)
    @option("url", description="The url of the embed", required=False)
    @option("timestamp", float, description="The timestamp of the embed", required=False)
    @option("field1", description="Title|Content of field 1", required=False)
    @option("field2", description="Title|Content of field 2", required=False)
    @option("field3", description="Title|Content of field 3", required=False)
    async def embed(self, ctx: discord.ApplicationContext, description: str, title: str, image: discord.Attachment,
                    thumbnail: bool, author: str, author_url: str, author_icon_url: str, footer: str,
                    footer_icon_url: str, url: str, timestamp: float, field1: str, field2: str,
                    field3: str, color: discord.Color):
        embed = discord.Embed(title=title, description=description, color=color)
        if image:
            if thumbnail:
                embed.set_thumbnail(url=image.url)
            else:
                embed.set_image(url=image.url)

        if author:
            embed.set_author(name=author, url=author_url, icon_url=author_icon_url)

        if footer:
            embed.set_footer(text=footer, icon_url=footer_icon_url)

        if url:
            embed.url = url

        if timestamp:
            embed.timestamp = datetime.datetime.fromtimestamp(timestamp)

        for field in [field1, field2, field3]:
            if field:
                embed.add_field(name=field.split("|")[0], value=field.split("|")[1])

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(SlashCommands(bot))
