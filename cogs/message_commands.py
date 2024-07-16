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
        tiktok_pattern = r'(https?://)(www\.)?(vm.tiktok\.com)(/[\w\-/]*)?'
        replacements = {
            'twitter.com': 'fxtwitter.com',
            'x.com': 'fixupx.com',
            'reddit.com': 'rxddit.com',
            'tiktok.com': 'tfxktok.com',
        }

        matches = [re.search(twitter_pattern, message.content), re.search(reddit_pattern, message.content),
                   re.search(tiktok_pattern, message.content)]
        matched = False
        for sitematch in matches:
            if sitematch:
                matched = True
                new_url = sitematch.group(0)
                for old, new in replacements.items():
                    new_url = new_url.replace(old, new)
                await ctx.respond(new_url, ephemeral=True)
        if not matched:
            return await ctx.respond("No supported link found!", ephemeral=True)

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
