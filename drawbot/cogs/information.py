import discord
from discord import Embed
from discord.ext import commands
from discord import app_commands, Interaction

from utils import json_wr, JsonDict


@app_commands.guild_only()
class InformationCommandsGroup(app_commands.Group, name="information"):
    @app_commands.command(name="help")
    async def help_command(self, interaction: Interaction):
        help_embed: Embed = discord.Embed(
            title="Help of the Pronote",
            description=(
                "Un bot qui traque vos devoir pronote "
                "et vous les notifient sur discord."
            ),
            color=self.client.embed_color,
        ).add_field(
            name="/here",
            value="change le salon d'envoi des nouveaux devoirs",
        )

        await interaction.response.send_message(embed=help_embed)

    @app_commands.command(name="here")
    async def here(self, interaction: Interaction):
        pronote_config: JsonDict = json_wr("pronote")
        pronote_config["channelID"] = interaction.channel_id
        json_wr("pronote", data=pronote_config)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Changement de salon",
                description=(
                    "Le salon pour envoyer les nouveaux devoirs "
                    "à bien été mis à jour"
                ),
                color=self.client.embed_color,
            )
        )


async def setup(client: commands.Bot) -> None:
    client.tree.add_command(InformationCommandsGroup())
