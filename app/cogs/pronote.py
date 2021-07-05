import json
import os
import discord
import pronotepy
from discord.ext import commands, tasks
from datetime import datetime, timedelta


class Pronote(commands.Cog):

    def __init__(self, client):
        """Initialize the search for new homeworks."""
        self.default_pronote_config = {
            "username": None, "password": None,  "channelID": None, "url": None
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
            json_file('pronote', 'w', self.default_pronote_config)

        config_pronote = json_file('pronote')

        for key, name in {
            'username': "nom d'utilisateur",
            'password': 'mot de passe',
            'url': 'url'
        }.items():
            if config_pronote.get(key) is None:
                print(f"veuillez indiquer un {name} Pronote dans le fichier pronote.json")
                return

        try:
            pronote = pronotepy.Client(
                config_pronote['url'],
                username=config_pronote['username'],
                password=config_pronote['password']
            )
        except pronotepy.CryptoError:
            print("Connexion à Pronote échoué. Mauvais nom d'utilisateur ou mot de passe.")
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

        homeworks_file = json_file('devoirs')
        homeworks_list = []

        for i in current_homeworks:
            description = i.description.replace('\n', ' ')
            homeworks_list.append(f'{i.date} : {i.subject.name} {description}')

        if len(homeworks_list) < len(homeworks_file):
            return

        json_file('devoirs', 'w', homeworks_list)
        devoirs_new_nbr = len(homeworks_list) - len(homeworks_file)
        print(f'[PRONOTE] {devoirs_new_nbr} nouveaux devoirs !')
        pronote_channel = self.client.get_channel(int(config_pronote['channelID']))

        for i in range(devoirs_new_nbr):
            await pronote_channel.send(
                embed=discord.Embed(
                    title=current_homeworks[len(homeworks_file) + i].subject.name,
                    description=current_homeworks[len(homeworks_file) + i].description.replace('\n', ' '),
                    color=0x1E744F
                ).set_author(
                    name=f'Pour le {current_homeworks[len(homeworks_file) + i].date}'
                )
            )


def json_file(file, action='r', file_data=None):
    with open(f"app/{file}.json", action) as f:
        if action == 'r':
            return json.load(f)

        if action == 'w':
            json.dump(file_data, f, indent=4)


def setup(client):
    client.add_cog(Pronote(client))
