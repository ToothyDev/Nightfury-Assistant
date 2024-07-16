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

        twitter_match = re.search(twitter_pattern, message.content)
        reddit_match = re.search(reddit_pattern, message.content)
        tiktok_match = re.search(tiktok_pattern, message.content)

        if twitter_match:
            url = twitter_match.group(0)
            if 'twitter.com' in url:
                new_url = url.replace('twitter.com', 'fxtwitter.com')
            elif 'x.com' in url:
                new_url = url.replace('x.com', 'fixupx.com')
            else:
                return await ctx.respond("No Twitter link found!", ephemeral=True)
            await ctx.respond(new_url, ephemeral=True)
        elif reddit_match:
            url = reddit_match.group(0)
            new_url = url.replace('reddit.com', 'rxddit.com')
            await ctx.respond(new_url, ephemeral=True)
        elif tiktok_match:
            url = tiktok_match.group(0)
            new_url = url.replace('tiktok.com', 'tfxktok.com')
            await ctx.respond(new_url, ephemeral=True)
        else:
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
