import os
import time
from datetime import datetime

import discord
import pronotepy
from discord.ext import commands, tasks

from app.utils import json_wr


class Pronote(commands.Cog):

    def __init__(self, client):
        """Initialize the search for new homeworks."""
        self.default_pronote_config = {
            "username": None,
            "password": None,
            "channelID": None, "url": None
        }

        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.homeworks_pronote.start()

    @tasks.loop(seconds=300)
    async def homeworks_pronote(self):
        hour = datetime.now().hour

        if hour > 22 or hour < 5:
            return

        files_dir = 'app/'

        if not os.path.isfile('app/pronote.json'):
            json_wr('pronote', self.default_pronote_config)

        config_pronote = json_wr('pronote')

        for key, name in {
            'username': "nom d'utilisateur",
            'password': 'mot de passe',
            'url': 'url'
        }.items():
            if config_pronote.get(key) is None:
                print(
                    f"veuillez indiquer un {name} Pronote  dans le fichier"
                    "pronote.json"
                )
                return

        try:
            pronote = pronotepy.Client(
                config_pronote['url'],
                username=config_pronote['username'],
                password=config_pronote['password']
            )

        except pronotepy.CryptoError:
            print(
                'Connexion à Pronote échoué. '
                'Mauvais nom d\'utilisateur ou mot de passe.'
            )
            return

        except pronotepy.PronoteAPIError:
            print("Connexion à Pronote échoué")
            return

        if config_pronote['folderName'] is not None:
            os.makedirs(config_pronote['folderName'])
            files_dir += f'{config_pronote["folderName"]}/'

        if not pronote.logged_in:
            print("Connexion à Pronote échoué")
            return

        if not config_pronote.get('channelID'):
            print("Channel non-trouvé ou non-existant")
            return

        current_homeworks = pronote.homework(pronote.start_day)

        homeworks_file = json_wr('devoirs')
        homeworks_list = []

        for homework in current_homeworks:
            description = homework.description.replace('\n', ' ')
            homeworks_list.append(
                f'{homework.date} : {homework.subject.name} {description}'
            )

        if homeworks_list == homeworks_file:
            print("Aucun nouveau devoir trouvé.")
            return

        json_wr('devoirs', data=homeworks_list)
        pronote_channel = self.client.get_channel(
            int(config_pronote['channelID'])
        )

        new_homework_num = 0

        for homework_num, homework in enumerate(homeworks_list):
            if homework in homeworks_file:
                continue

            new_homework_num += 1

            time_marker = int(
                time.mktime(
                    time.strptime(
                        str(current_homeworks[homework_num].date),
                        "%Y-%m-%d"
                    )
                )
            )

            await pronote_channel.send(
                embed=discord.Embed(
                    title=(
                        f'{current_homeworks[homework_num].subject.name} pour'
                        f'le <t:{time_marker}:D>'
                    ),
                    # now you can use timestamps in discord like:
                    # <t:timestamp:D>

                    description=(
                        current_homeworks[
                            homework_num
                        ].description.replace('\n', ' ')
                    ),
                    color=0x1E744F
                )
            )
        print(f'[PRONOTE] {new_homework_num} nouveaux devoirs !')


def setup(client):
    client.add_cog(Pronote(client))
