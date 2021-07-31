import json
import os
from discord.ext import commands


class Bot(commands.Bot):

    def __init__(self):
        """Initialize the bot and load config for token and prefix."""
        self.embed_color = 0x1E744F
        self._token = None

        if not os.path.isfile('app/config.json'):
            with open('app/config.json', 'w') as f:
                json.dump({'token': "null", 'prefix': ';'}, f, indent=4)
            return

        with open('app/config.json') as f:
            config = json.load(f)

        super().__init__(config.get('prefix', ';'))
        self._token = config.get('token')

        self.remove_command('help')

        for filename in os.listdir("app/cogs"):
            if filename.endswith('.py'):
                self.load_extension(f'app.cogs.{filename[:-3]}')

    def run(self):
        if not self._token:
            print('veuillez indiquer token Discord dans le fichier config.json')
            return

        if self._token == "null":
            print('veuillez indiquer token Discord dans le fichier config.json')
            return

        super().run(self._token)

    async def on_ready(self):
        print(f'Connecté en temps que {self.user.name} !')
