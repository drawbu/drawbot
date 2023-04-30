import os
from typing import Optional

from colorama import Fore, Style
from discord import LoginFailure, Intents
from discord.ext import commands
from discord.ext.commands import NoEntryPointError

from .utils import json_wr, JsonData


class Bot(commands.Bot):

    def __init__(self, config_dir: str):
        """Initialize the bot and load config for token and prefix."""
        self.embed_color: int = 0x1E744F
        self._token: Optional[str] = None

        default_config: JsonData = {
            "token": "",
            "channelID": "",
            "username": "",
            "password": "",
            "url": "",
        }

        self.config_dir = config_dir
        self.config: JsonData = json_wr(f"{self.config_dir}/config.json")

        for key in default_config.keys():
            if self.config.get(key) is None:
                print(
                    f'Veuillez indiquer remplir la valeur "{key}" '
                    "dans le fichier vars/config.json"
                )

                self.is_configured = False
                return

        super().__init__(command_prefix=";", intents=Intents.default())
        self._token = self.config.get("token")
        self.config.pop("token")

        self.remove_command("help")
        self.is_configured = True

    def run(self, **kwargs) -> bool:
        try:
            super().run(self._token, **kwargs)

        except LoginFailure:
            print(
                "Echec de la connexion au client."
                "Veuillez vérifier que votre token est correct."
            )
            return False

        return True

    async def on_ready(self):
        await self.load_cogs()
        print(f"Connecté en temps que {self.user.name} !")

    async def load_cogs(self):
        for command in self.tree.get_commands():
            await self.unload_extension(command.name)

        for filename in os.listdir("drawbot/cogs"):
            if not filename.endswith(".py"):
                continue

            try:
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(
                    f" -> Loaded extension {Fore.BLUE}{Style.BRIGHT}"
                    f"{filename}{Style.RESET_ALL}"
                )

            except NoEntryPointError:
                print(
                    f"-> {filename} was not loaded because there was"
                    "no setup() function."
                )

        await self.tree.sync()
