import json
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

    @commands.command(
        name='channel', aliases=('here',),
    )
    async def change_channel(self, ctx):
        pronote_config = open_file('app/', 'pronote', 'r')
        pronote_config['channelID'] = ctx.channel.id
        open_file('app/', 'pronote', 'w', pronote_config)
        await ctx.send(embed=discord.Embed(
            title="Changement de salon",
            description="Le salon pour envoyer les nouveaux devoirs à bien été mis à jour",
            color=self.client.embed_color
        ))


def setup(client):
    client.add_cog(Informations(client))


def open_file(repertory, file, action, file_data=None):
    with open(repertory + file + '.json', action) as json_file:
        if action == 'r':
            file_data = json.load(json_file)
        elif action == 'w':
            json.dump(file_data, json_file, indent=4)
        return file_data
