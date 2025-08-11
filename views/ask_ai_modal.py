import discord

import config
from utils import ask_ai_about_message


class AskAIModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        self.original_message = kwargs.pop("original_message")
        super().__init__(*args, **kwargs, title="Ask AI")
        self.add_item(discord.ui.InputText(label="Question", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(invisible=False)
        ai_response = await ask_ai_about_message(
            [
                {
                    "role": "user",
                    "content": self.original_message
                },
                {
                    "role": "user",
                    "content": self.children[0].value
                }
            ]
        )

        await interaction.respond(
            f"""-# Prompt: {self.children[0].value}
{config.emojis["ai_chat_bubble"]} {ai_response}
-# Model: {config.llm_model_name}""")
