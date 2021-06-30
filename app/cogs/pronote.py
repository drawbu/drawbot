from discord.ext import commands


class Pronote(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Pronote(client))
