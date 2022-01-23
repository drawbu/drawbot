import discord
from discord import Embed
from discord.ext import commands

from discord.ext.commands import Context

from app import JsonDict

from app.utils import json_wr


class Informations(commands.Cog):

    def __init__(self, client):
        """Initialize the different commands."""
        self.client = client

    @commands.command(
        name='help', aliases=('h', 'aide'),
    )
    async def help_command(self, ctx: Context) -> None:
        help_embed: Embed = discord.Embed(
            title="Help of the Pronote",
            description=(
                "Un bot qui traque vos devoir pronote "
                "et vous les notifient sur discord."
            ),
            color=self.client.embed_color
        ).add_field(
            name=f'{ctx.prefix}here',
            value='change le salon d \'envoi des nouveaux devoirs'
        )

        await ctx.send(embed=help_embed)

    @commands.command(
        name='channel', aliases=('here',),
    )
    async def change_channel(self, ctx: Context) -> None:
        pronote_config: JsonDict = json_wr('pronote')
        pronote_config['channelID'] = ctx.channel.id
        json_wr('pronote', data=pronote_config)

        await ctx.send(
            embed=discord.Embed(
                title="Changement de salon",
                description=(
                    "Le salon pour envoyer les nouveaux devoirs "
                    "à bien été mis à jour"
                ),
                color=self.client.embed_color
            )
        )


def setup(client) -> None:
    client.add_cog(Informations(client))
