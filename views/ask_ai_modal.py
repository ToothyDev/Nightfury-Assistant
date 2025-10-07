import discord

import config
from utils import ask_ai_about_message


class AskAIModal(discord.ui.DesignerModal):
    def __init__(self, *args, **kwargs):
        self.original_message = kwargs.pop("original_message")
        super().__init__(*args, **kwargs, title="Ask AI")
        self.add_item(discord.ui.Label("Prompt", discord.ui.InputText(placeholder="Explain what the user means",
                                                                      style=discord.InputTextStyle.long,
                                                                      custom_id="prompt")))
        self.add_item(
            discord.ui.Label("Should the message be ephemereal?", discord.ui.Select(
                discord.ComponentType.string_select,
                custom_id="ephemeral",
                options=[
                    discord.SelectOption(label="No", value="no", default=True),
                    discord.SelectOption(label="Yes", value="yes")
                ]
            )
                             )
        )

    async def callback(self, interaction: discord.Interaction):
        ephemeral_choice = self.get_item("ephemeral").values[0] == "yes"
        await interaction.response.defer(invisible=False, ephemeral=ephemeral_choice)
        ai_response = await ask_ai_about_message(
            [
                {
                    "role": "user",
                    "content": self.original_message
                },
                {
                    "role": "user",
                    "content": self.get_item("prompt").value
                }
            ]
        )

        await interaction.respond(
            f"""-# Prompt: {self.children[0].label}
{config.emojis["ai_chat_bubble"]} {ai_response}
-# Model: {config.llm_model_name}""", ephemeral=ephemeral_choice)
