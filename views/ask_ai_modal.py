import discord

import config
from utils import ask_ai_about_message


class AskAIModal(discord.ui.DesignerModal):
    def __init__(self, *args, original_message: str, **kwargs):
        super().__init__(*args, **kwargs, title="Ask AI")
        self.original_message = original_message
        self.prompt_input = discord.ui.InputText(placeholder="Explain what the user means",
                                                 style=discord.InputTextStyle.long,
                                                 custom_id="prompt")
        self.ephemeral_select = discord.ui.Select(
            discord.ComponentType.string_select,
            custom_id="ephemeral",
            options=[
                discord.SelectOption(label="No", value="no", default=True),
                discord.SelectOption(label="Yes", value="yes")
            ]
        )

        self.add_item(discord.ui.Label("Prompt", self.prompt_input))
        self.add_item(discord.ui.Label("Should the message be ephemeral?", self.ephemeral_select))

    async def callback(self, interaction: discord.Interaction):
        ephemeral_choice = self.ephemeral_select.values[0] == "yes"
        await interaction.response.defer(invisible=False, ephemeral=ephemeral_choice)
        ai_response = await ask_ai_about_message(
            [
                {
                    "role": "user",
                    "content": self.original_message
                },
                {
                    "role": "user",
                    "content": self.prompt_input.value
                }
            ]
        )

        await interaction.respond(
            f"""-# Prompt: {self.prompt_input.value}
{config.emojis["ai_chat_bubble"]} {ai_response}
-# Model: {config.llm_model_name}""", ephemeral=ephemeral_choice)
