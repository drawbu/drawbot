import json
import os
from typing import Optional

from discord.ext import commands

from app import JsonData
from app.utils import json_wr


class Bot(commands.Bot):

    def __init__(self) -> None:
        """Initialize the bot and load config for token and prefix."""
        self.embed_color: int = 0x1E744F
        self._token: Optional[str] = None

        if not os.path.isfile('app/config.json'):
            with open('app/config.json', 'w') as f:
                json.dump({'token': "null", 'prefix': ';'}, f, indent=4)
            return

        config: JsonData = json_wr('config')
        super().__init__(config.get('prefix', ';'))

        self._token = config.get('token')
        self.remove_command('help')

        for filename in os.listdir("app/cogs"):
            if filename.endswith('.py'):
                self.load_extension(f'app.cogs.{filename[:-3]}')

    def run(self) -> None:
        if not self._token:
            print('veuillez indiquer token Discord dans le fichier config.json')
            return

        if self._token == "null":
            print('veuillez indiquer token Discord dans le fichier config.json')
            return

        super().run(self._token)

    async def on_ready(self) -> None:
        print(f'Connecté en temps que {self.user.name} !')
