import logging

import discord
import openai
from discord.ext import commands

log = logging.getLogger(__name__)


class ErrorHandling(discord.Cog, name="error_handling"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext,
                                           err: discord.ApplicationCommandInvokeError):
        if isinstance(err, commands.BotMissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            await ctx.respond(f"**I'm missing {perms} permissions**", ephemeral=True)
            return

        if isinstance(err, commands.MemberNotFound):
            await ctx.respond(f"**Could not find user `{err.argument}`", ephemeral=True)
            return

        if isinstance(err, discord.NotFound):
            await ctx.respond("I could not find the argument you have provided.", ephemeral=True)
            return

        err: Exception = err.original  # Unwrap the exception to catch any non-discord errors

        if isinstance(err, openai.RateLimitError):
            log.warning("AI API ratelimit error")
            await ctx.respond("You are using this command too much! Please try again in a few seconds", ephemeral=True)
            return

        if isinstance(err, openai.BadRequestError):
            if err.message == "context deadline exceeded":
                log.warning("AI API request timed out")
                await ctx.respond("The request has timed out! Please try again", ephemeral=True)
                return

        if isinstance(err, openai.InternalServerError):
            log.warning("AI API internal service error")
            await ctx.respond("The service this command uses had an error. Try again later.", ephemeral=True)
            return

        if isinstance(err, openai.APIStatusError):
            if err.message.startswith("Request too large for model"):
                log.warning("AI API request too large for model")
                await ctx.respond("The chat history is too big! Try again later.", ephemeral=True)
                return

        await ctx.respond("An unknown error occured! This will be logged and fixed!", ephemeral=True)
        log.error(
            f"{ctx.author.global_name} used /{ctx.command} which caused '{err}', error class: {err.__class__.__name__}",
            exc_info=(type(err), err, err.__traceback__))


def setup(bot):
    bot.add_cog(ErrorHandling(bot))
