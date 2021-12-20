import time
from datetime import datetime
from collections import defaultdict

import discord
import pronotepy
from discord.ext import commands, tasks
from typing import List, DefaultDict

from app import JsonData
from app.utils import json_wr


class Pronote(commands.Cog):

    def __init__(self, client):
        """Initialize the search for new homeworks."""
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.homeworks_pronote.start()

    @tasks.loop(seconds=300)
    async def homeworks_pronote(self) -> None:
        default_pronote_config: JsonData = {
            "username": "",
            "password": "",
            "channelID": "",
            "url": ""
        }

        # Does not work at night
        hour = datetime.now().hour
        if hour > 22 or hour < 5:
            return

        config_pronote: JsonData = json_wr("pronote")

        for key in default_pronote_config.keys():
            if config_pronote.get(key, "") == "":
                print(
                    f"Veuillez indiquer remplir la valeur \"{key}\" "
                    "dans le fichier pronote.json"
                )
                await self.client.close()
                return

        try:
            pronote: pronotepy.Client = pronotepy.Client(
                config_pronote["url"],
                config_pronote["username"],
                config_pronote["password"]
            )

        except pronotepy.CryptoError:
            print(
                "Connexion à Pronote échoué. "
                "Mauvais nom d'utilisateur ou mot de passe."
            )
            await self.client.close()
            return

        except pronotepy.PronoteAPIError:
            print("Connexion à Pronote échoué")
            return

        if not pronote.logged_in:
            print("Connexion à Pronote échoué")
            return

        if not config_pronote.get("channelID"):
            print("Channel non-trouvé ou inexistant")
            await self.client.close()
            return

        fetched_homeworks: List[pronote.homework] = pronote.homework(
            pronote.start_day
        )

        homeworks_file: JsonData = json_wr("devoirs")

        homeworks: DefaultDict[str, List[pronote.homework]] = defaultdict(list)

        for homework in fetched_homeworks:
            homeworks[str(homework.date)].append(
                {
                    "subject": homework.subject.name,
                    "description": homework.description.replace("\n", " ")
                }
            )

        pronote_channel: discord.TextChannel = await self.client.fetch_channel(
            int(config_pronote.get("channelID"))
        )

        if homeworks_file == {} or isinstance(homeworks_file, list):
            json_wr("devoirs", "w", homeworks)
            print("La première connexion aux serveurs de PRONOTE à été un "
                  "succès, les prochains devoirs seront envoyés ici.")
            await pronote_channel.send(
                embed=discord.Embed(
                    title="Première connexion réussie",
                    description=(
                        "La connexion aux serveurs de PRONOTE à été un succès, "
                        "les prochains devoirs seront envoyés ici."
                    ),
                    color=0x1E744F
                )
            )
            return

        if homeworks == homeworks_file:
            print("Aucun nouveau devoir trouvé.")
            return

        json_wr("devoirs", "w", homeworks)

        homeworks_list: list = []
        for key, value in homeworks.items():
            for i in value:
                i["date"] = key
            homeworks_list.extend(value)

        homeworks_old_list: list = []
        for key, value in homeworks_file.items():
            for i in value:
                i["date"] = key
            homeworks_old_list.extend(value)

        new_homework_count = 0

        for homework in homeworks_list:
            if homework in homeworks_old_list:
                continue

            new_homework_count += 1

            time_marker: int = int(
                time.mktime(time.strptime(homework["date"], "%Y-%m-%d"))
            )

            await pronote_channel.send(
                embed=discord.Embed(
                    title=(
                        f"{homework['subject']}\n"
                        f"Pour le <t:{time_marker}:D>"
                    ),
                    description=homework["description"],
                    color=0x1E744F
                )
            )
        print(f'[PRONOTE] {new_homework_count} nouveaux devoirs !')


def setup(client) -> None:
    client.add_cog(Pronote(client))
