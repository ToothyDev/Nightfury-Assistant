import datetime
import io

import discord
from discord import slash_command, option

import config
import utils
from utils import Colors


class SlashCommands(discord.Cog, name="slash_commands"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="Send an embed with up to three fields")
    @option("description", description="The description of the embed", required=False)
    @option("title", description="The title of the embed", required=False)
    @option("color", int, description="The color of the embed",
            autocomplete=discord.utils.basic_autocomplete(Colors.color_options), required=False,
            default=discord.Color.default())
    @option("image", discord.Attachment, description="The image of the embed", required=False)
    @option("thumbnail", bool, description="Show the image as a thumbnail?", required=False, default=False)
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
                    field3: str, color: discord.Color) -> None:
        if not any([description, title, image, author, footer, field1, field2, field3]):
            await ctx.respond("No required argument was provided!\n"
                              "At least one of these is required to send the embed: Description, "
                              "title, image, author, footer, or any of the fields.", ephemeral=True)
            return

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

    @discord.slash_command(description="Ask AI something")
    async def ai(self, ctx: discord.ApplicationContext, prompt: str) -> None:
        await ctx.defer()
        ai_response = await utils.ask_ai(prompt)
        await ctx.respond(
            f"""-# Prompt: {prompt}
{config.emojis["ai_chat_bubble"]} {ai_response}
-# Model: {config.llm_model_name}""")

    @discord.slash_command(description="Send a CV2 message with any components")
    @discord.option("buttons", bool, description="Show buttons?", required=False, default=False)
    @discord.option("select", bool, description="Show a select menu?", required=False, default=False)
    @discord.option("file", discord.Attachment, description="The file to send in the CV2 message", required=False)
    @discord.option("image", discord.Attachment, description="The image to send in the CV2 message", required=False)
    async def cv2(self, ctx: discord.ApplicationContext, buttons: bool, select: bool, file: discord.Attachment,
                  image: discord.Attachment):
        await ctx.defer(ephemeral=True)

        button_components = []
        if buttons:
            button_components.extend([
                discord.ui.Separator(),
                discord.ui.TextDisplay(content="\nAll the kinds of buttons"),
                discord.ui.Button(
                    url="https://google.com",
                    style=discord.ButtonStyle.link,
                    label="Link Button!",
                ),
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    label="Blue Button!"
                ),
                discord.ui.Button(
                    style=discord.ButtonStyle.secondary,
                    label="Grey Button!"
                ),
                discord.ui.Button(
                    style=discord.ButtonStyle.danger,
                    label="Red Button!"
                )]
            )

        select_components = []
        if select:
            select_components.extend([
                discord.ui.Separator(),
                discord.ui.TextDisplay(content="\nA select menu"),
                discord.ui.Select(
                    min_values=1,
                    max_values=3,
                    options=[
                        discord.SelectOption(
                            label="Test selection",
                            value="44c530edcff948c5e63764303419e252",
                            description="test",
                            emoji="😜",
                            default=True,
                        ),
                        discord.SelectOption(
                            label="Other selection",
                            value="b"
                        ),
                        discord.SelectOption(
                            label="Yet another selection",
                            value="a"
                        )
                    ]
                ),
            ])

        file_components = []
        if file:
            file_components.extend([
                discord.ui.Separator(),
                discord.ui.TextDisplay(content="\nA file owo"),
                discord.ui.File(f"attachment://{file.filename}")
            ])

        image_components = []
        if image:
            image_components.extend([
                discord.ui.Separator(),
                discord.ui.TextDisplay(content="\nLe image"),
                discord.ui.MediaGallery(
                    discord.MediaGalleryItem(
                        url=image.url,
                    ),
                )
            ])

        components = [
            discord.ui.Container(
                discord.ui.TextDisplay(content="This is a pure text component."),
                *button_components,
                *select_components,
                *file_components,
                *image_components,
                color=discord.Color(9225410),
            ),
        ]

        if file:
            data = await file.read()  # read file into bytes
            file = discord.File(fp=io.BytesIO(data), filename=file.filename)
            await ctx.respond(view=discord.ui.View(*components), file=file, ephemeral=True)
            return
        await ctx.respond(view=discord.ui.View(*components), ephemeral=True)


def setup(bot):
    bot.add_cog(SlashCommands(bot))
