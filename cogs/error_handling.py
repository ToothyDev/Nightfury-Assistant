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
            log.warning("AI API rate limit hit for /%s by %s", ctx.command, ctx.author.global_name)
            await ctx.respond("You are using this command too much! Please try again in a few seconds", ephemeral=True)
            return

        if isinstance(err, openai.BadRequestError):
            if err.message == "context deadline exceeded":
                log.warning("AI API request timed out for /%s by %s: %s", ctx.command, ctx.author.global_name,
                            err.message)
                await ctx.respond("The request has timed out! Please try again", ephemeral=True)
                return

        if isinstance(err, openai.APIStatusError):
            if err.message.startswith("Request too large for model"):
                log.warning("AI API request too large for /%s by %s", ctx.command, ctx.author.global_name)
                await ctx.respond("The chat history is too big! Try again later.", ephemeral=True)
                return

        if isinstance(err, openai.NotFoundError):
            log.warning("AI API error for /%s by %s: %s", ctx.command, ctx.author.global_name,
                        err.message)
            await ctx.respond("Something went wrong!", ephemeral=True)
            return

        if isinstance(err, openai.InternalServerError):
            log.warning("AI API error for /%s by %s: %s", ctx.command, ctx.author.global_name, err.message)
            await ctx.respond("The API returned an error! Please try again.", ephemeral=True)
            return

        await ctx.respond("An unknown error occured! This will be logged and fixed!", ephemeral=True)
        log.error(
            "%s used /%s which caused '%s', error class: %s",
            ctx.author.global_name, ctx.command, err, err.__class__.__name__,
            exc_info=(type(err), err, err.__traceback__))


def setup(bot):
    bot.add_cog(ErrorHandling(bot))
