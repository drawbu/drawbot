import os
import sys
from typing import Optional

from discord.ext import commands

from .types import JsonData
from .utils import json_wr


class Bot(commands.Bot):

    def __init__(self) -> None:
        """Initialize the bot and load config for token and prefix."""
        self.embed_color: int = 0x1E744F
        self._token: Optional[str] = None

        default_config: JsonData = {
            "token": "",
            "prefix": "!",
            "channelID": "",
            "username": "",
            "password": "",
            "url": ""
        }

        self.config: JsonData = json_wr("config")

        for key in default_config.keys():
            if self.config.get(key, "") == "":
                print(
                    f"Veuillez indiquer remplir la valeur \"{key}\" "
                    "dans le fichier vars/config.json"
                )
                sys.exit()

        super().__init__(self.config.get("prefix", ";"))
        self._token = self.config.get("token")
        self.config.pop("token")

        self.remove_command("help")

        for filename in os.listdir("drawbot/cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"drawbot.cogs.{filename[:-3]}")

    def run(self) -> None:
        super().run(self._token)

    async def on_ready(self) -> None:
        print(f"Connecté en temps que {self.user.name} !")
