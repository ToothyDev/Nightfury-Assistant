import re

import discord
from discord import message_command

import views.ask_ai_modal
from utils import Colors


class MessageCommands(discord.Cog, name="message_commands"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @message_command(name="yoink sticker")
    async def yoink_sticker(self, ctx: discord.ApplicationContext, message: discord.Message) -> None:
        if not message.stickers:
            await ctx.respond("No stickers found!", ephemeral=True)
            return
        embed = discord.Embed(color=Colors.tailfin).set_image(url=message.stickers[0].url)
        embed.set_footer(text="Nightfury Assistant", icon_url=self.bot.user.avatar.url)
        await ctx.respond(embed=embed, ephemeral=True)

    @message_command(name="yoink emoji")
    async def yoink_emoji(self, ctx: discord.ApplicationContext, message: discord.Message) -> None:
        if not message.content:
            await ctx.respond("No emoji found!", ephemeral=True)
            return

        emoji_pattern = r'<a?:\w+:\d+>'  # Black magic; matches the emoji syntax for custom emojis <:name:id>
        matches = re.findall(emoji_pattern, message.content)
        if not matches:
            await ctx.respond("No custom emoji found!", ephemeral=True)
            return

        emojis = []
        for match in matches:
            emojis.append(match.split(':')[2][:-1])

        embeds = []
        for emoji in emojis:
            embed = discord.Embed(url="https://google.com",
                                  color=Colors.tailfin).set_image(
                url=f"https://cdn.discordapp.com/emojis/{emoji}.webp?animated=true")
            embed.set_footer(text="Nightfury Assistant", icon_url=self.bot.user.avatar.url)
            embeds.append(embed)

        await ctx.respond(embeds=embeds, ephemeral=True)

    @message_command()
    async def fxlink(self, ctx: discord.ApplicationContext, message: discord.Message) -> None:
        if not message.content:
            await ctx.respond("No link found!", ephemeral=True)
            return

        twitter_pattern = r'(https?://)(www\.)?(twitter\.com|x\.com)'
        reddit_pattern = r'(https?://)(www\.)?(reddit\.com)'
        tiktok_pattern = r'(https?://)(www\.)?((vm\.)?tiktok\.com)'
        instagram_pattern = r'(https?://)(www\.)?(instagram\.com)'
        replacements = {
            'twitter.com': 'fxtwitter.com',
            'x.com': 'fixupx.com',
            'reddit.com': 'rxddit.com',
            'tiktok.com': 'tfxktok.com',
            'vm.tiktok.com': 'tfxktok.com',
            'instagram.com': 'ddinstagram.com'
        }

        patterns = [twitter_pattern, reddit_pattern, tiktok_pattern, instagram_pattern]

        for pattern in patterns:
            match = re.search(pattern, message.content)
            if match:
                new_url = message.content
                for old, new in replacements.items():
                    new_url = re.sub(rf'https?://(www\.)?{old}', rf'https://{new}', new_url)
                await ctx.respond(new_url, ephemeral=True)
                return

        await ctx.respond("No supported link found!", ephemeral=True)

    @message_command(name="ask ai")
    async def ask_ai(self, ctx: discord.ApplicationContext, message: discord.Message) -> None:
        await ctx.send_modal(views.ask_ai_modal.AskAIModal(original_message=message.content))


def setup(bot):
    bot.add_cog(MessageCommands(bot))
