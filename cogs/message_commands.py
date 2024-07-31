import io
import random
import re

import aiohttp
import discord
from discord import message_command


class MessageCommands(discord.Cog, name="message_commands"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @message_command()
    async def fxlink(self, ctx: discord.ApplicationContext, message: discord.Message):
        if not message.content:
            return await ctx.respond("No link found!", ephemeral=True)

        twitter_pattern = r'(https?://)(www\.)?(twitter\.com|x\.com)(/[\w\-/]*)?'
        reddit_pattern = r'(https?://)(www\.)?(reddit\.com)(/[\w\-/]*)?'
        tiktok_pattern = r'(https?://)(www\.)?((vm\.)?tiktok\.com)(/[\w\-\/]*)?'
        replacements = {
            'twitter.com': 'fxtwitter.com',
            'x.com': 'fixupx.com',
            'reddit.com': 'rxddit.com',
            'tiktok.com': 'tfxktok.com',
            'vm.tiktok.com': 'tfxktok.com'
        }

        patterns = [twitter_pattern, reddit_pattern, tiktok_pattern]

        for pattern in patterns:
            match = re.search(pattern, message.content)
            if match:
                new_url = message.content
                for old, new in replacements.items():
                    new_url = re.sub(rf'https?://(www\.)?{old}', rf'https://{new}', new_url)
                return await ctx.respond(new_url, ephemeral=True)

        await ctx.respond("No supported link found!", ephemeral=True)

    @message_command()
    async def tweet(self, ctx: discord.ApplicationContext, message: discord.Message):
        if not message.content:
            return await ctx.respond("Message is empty!", ephemeral=True)
        link = "https://some-random-api.com/canvas/misc/tweet/"
        link += f"?avatar={message.author.avatar.url}"
        link += f"&username={message.author.name}"
        link += f"&displayname={message.author.global_name}"
        link += f"&comment={message.content.replace(" ", "+")}"
        link += f"&theme=dark"
        link += f"&likes={random.randint(50, 200)}"
        link += f"&retweets={random.randint(50, 200)}"
        link += f"&replies={random.randint(50, 200)}"

        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                image_data = io.BytesIO(await response.read())
                file = discord.File(image_data, filename="tweet.png")

        await ctx.respond(file=file)


def setup(bot):
    bot.add_cog(MessageCommands(bot))
