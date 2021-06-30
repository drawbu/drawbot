import os.path

import discord
from discord.ext import commands


class Informations(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        name='help', aliases=('h', 'aide'),
    )
    async def help_command(self, ctx):
        help_embed = discord.Embed(
            title="Help of the Pronote",
            description="Un bot qui traque vos devoir pronote et vous les notifient sur discord",
            color=self.client.embed_color
        )

        await ctx.send(embed=help_embed)


def setup(client):
    client.add_cog(Informations(client))
