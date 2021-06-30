from datetime import timedelta, datetime

import os
import json
import pronotepy
import discord
from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

mainFiles = './'

# Configuration des fichiers config.json par défaut
configJson = {'token': '0', 'prefix': ';'}


# Fonction principales (fonctions très utiles)
def open_file(repertory, file, action, file_data=None):
    """Permet de créer ou ouvrir des fichier json. Dans action il faut mettre 'r' pour lire et 'w' pour remplacer le
    contenu du fichier par fileData. Si le fichier n'existe pas, il faut faire 'w'."""
    with open(repertory + file + '.json', action) as jsonFile:
        if action == 'r':
            file_data = json.load(jsonFile)
        elif action == 'w':
            json.dump(file_data, jsonFile, indent=4)
        jsonFile.close()
        return file_data


def verify_file(repertory, file, file_json):
    """Nécessite openFile(). Permet de créer un fichier si il n'existe pas et sinon de vérifier si le contenu du fichier
     correspond bien à au modèle (fileJson)."""
    if (file + '.json') not in os.listdir(repertory):
        open_file(repertory, file, 'w', file_json)
    file_data = open_file(repertory, file, 'r', 0)
    if type({}) == type(file_json):
        for cle, valeur in file_json.items():
            if cle not in file_data.keys():
                file_data[cle] = file_json[cle]
        open_file(repertory, file, 'w', file_data)
    return file_data


# Création/vérification du fichier config
config = verify_file(mainFiles, 'config', configJson)
token = config['token']


@client.event
async def on_ready():
    devoirs_pronote.start()
    print('Connecté en temps que {0.user.name} !'.format(client))


@tasks.loop(seconds=300)
async def devoirs_pronote():
    if datetime.now().hour not in [22, 23, 0, 1, 2, 3, 4, 5]:
        files_dir = './'
        config_pronote = verify_file(files_dir, 'pronote',
                                    {'username': None, 'password': None, 'folderName': None, 'channelID': None,
                                    'url': None})

        if config_pronote['username'] is not None \
                and config_pronote['password'] is not None \
                and config_pronote['url'] is not None:
            pronote = pronotepy.Client(config_pronote['url'], username=config_pronote['username'],
                                       password=config_pronote['password'])

            if config_pronote['folderName'] is not None:
                os.makedirs(config_pronote['folderName'])
                files_dir += f'{config_pronote["folderName"]}/'

            if pronote.logged_in and (config_pronote['channelID'] is not None):
                devoirs = pronote.homework(pronote.start_day,
                                           pronote.start_day + timedelta(days=360))
                devoirs_file = verify_file(files_dir, 'devoirs', [])
                devoirs_list = []
                for i in devoirs:
                    description = i.description.replace('\n', ' ')
                    devoirs_list.append(f'{i.date} : {i.subject.name} {description}')

                if len(devoirs_list) > len(devoirs_file):
                    open_file(files_dir, 'devoirs', 'w', devoirs_list)
                    devoirs_new_nbr = len(devoirs_list) - len(devoirs_file)
                    print(f'[PRONOTE] {devoirs_new_nbr} nouveaux devoirs !')
                    pronote_channel = client.get_channel(int(config_pronote['channelID']))
                    for i in range(devoirs_new_nbr):
                        embed = discord.Embed(title=devoirs[len(devoirs_file) + i].subject.name,
                                              description=devoirs[len(devoirs_file) + i].description.replace('\n', ' '),
                                              color=0x1E744F)
                        embed.set_author(name=f'Pour le {devoirs[len(devoirs_file) + i].date}')
                        await pronote_channel.send(embed=embed)


if token is not None:
    client.run(token)
else:
    print('Pas de token dans le fichier config')
