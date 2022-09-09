import time

import discord
from discord import app_commands, Interaction
from discord.ext import commands

from ..utils import json_wr, JsonDict


@app_commands.guild_only()
class PronoteCommandsGroup(app_commands.Group, name="pronote"):
    @app_commands.command(name="help")
    async def help_command(self, interaction: Interaction):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Help of the Pronote",
                description=(
                    "Un bot qui traque vos devoir pronote "
                    "et vous les notifient sur discord."
                ),
                color=interaction.client.embed_color,
            ).add_field(
                name="/pronote help",
                value="Affiche ce message",
            ).add_field(
                name="/pronote here",
                value=("Change le salon d'envoi des nouveaux messages "
                       "pour pronote (nouveaux devoirs et notes)"),
            ).add_field(
                name="/pronote incoming",
                value="Affiche les prochains devoirs",
            )
        )

    @app_commands.command()
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
                color=interaction.client.embed_color,
            )
        )

    @app_commands.command(description="Donne la liste des prochains devoirs")
    async def incoming(self, interaction: Interaction):
        homeworks: JsonDict = json_wr("devoirs")

        embed = discord.Embed(
            title="Prochains devoirs",
            color=interaction.client.embed_color
        )

        today = time.time()
        homeworks_dict = {}
        for date, homeworks_list in homeworks.items():

            date_timestamp = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
            if date_timestamp >= today:
                homeworks_dict[date_timestamp] = homeworks_list

        homeworks_dict = {
            key: homeworks_dict[key]
            for key in sorted(homeworks_dict)
        }

        for date, homeworks_list in homeworks_dict.items():
            embed.add_field(
                name=f"Pour le <t:{date}:D>",
                value="\n".join(
                    f"**- {h['subject']} :** {h['description']}"
                    for h in homeworks_list
                ),
                inline=False,
            )

        await interaction.response.send_message(embed=embed)


async def setup(client: commands.Bot) -> None:
    client.tree.add_command(PronoteCommandsGroup())
