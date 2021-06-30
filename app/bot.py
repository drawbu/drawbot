import json
import os
from discord.ext import commands


class Bot(commands.Bot):

    def __init__(self):
        with open('app/config.json') as f:
            config = json.load(f)

        super().__init__(config.get('prefix'))
        self._token = config.get('token')

        for filename in os.listdir("cogs"):
            if filename.endswith('.py'):
                self.load_extension(f'app.cogs.{filename[:-3]}')

    def run(self):
        if not self._token:
            print('no token found')
            return

        super().run(self._token)

    async def on_ready(self):
        print(f'Connecté en temps que {self.user.name} !')
