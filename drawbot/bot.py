import os
import sys
from typing import Optional

from discord import LoginFailure, Intents
from discord.ext import commands
from colorama import Fore, Style

from .utils import json_wr, JsonData


class Bot(commands.Bot):
    def __init__(self):
        """Initialize the bot and load config for token and prefix."""
        self.embed_color: int = 0x1E744F
        self._token: Optional[str] = None

        default_config: JsonData = {
            "token": "",
            "prefix": "!",
            "channelID": "",
            "username": "",
            "password": "",
            "url": "",
        }

        self.config: JsonData = json_wr("config")

        for key in default_config.keys():
            if self.config.get(key, "") == "":
                print(
                    f'Veuillez indiquer remplir la valeur "{key}" '
                    "dans le fichier vars/config.json"
                )
                sys.exit()

        super().__init__(command_prefix=";", intents=Intents.default())
        self._token = self.config.get("token")
        self.config.pop("token")

        self.remove_command("help")

    def run(self):
        try:
            super().run(self._token)
        except LoginFailure:
            print(
                "Echec de la connexion au client."
                "Veuillez vérifier que votre token est correct."
            )

    async def on_ready(self):
        await self.load_cogs()
        print(f"Connecté en temps que {self.user.name} !")

    async def load_cogs(self):
        for command in self.tree.get_commands():
            await self.unload_extension(command.name)

        for filename in os.listdir("drawbot/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f" -> Loaded extension "
                      f"{Fore.BLUE}{Style.BRIGHT}{filename}{Style.RESET_ALL}")
        await self.tree.sync()
