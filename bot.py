from datetime import timedelta, datetime

import discord
import json
import os
import pronotepy
from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

mainFiles = './'

# Configuration des fichiers config.json par défaut
configJson = {'token': '0', 'prefix': ';'}


# Fonction principales (fonctions très utiles)
def open_file(repertory, file, action, fileData=None):
    """Permet de créer ou ouvrir des fichier json. Dans action il faut mettre 'r' pour lire et 'w' pour remplacer le
    contenu du fichier par fileData. Si le fichier n'existe pas, il faut faire 'w'."""
    with open(repertory + file + '.json', action) as jsonFile:
        if action == 'r':
            fileData = json.load(jsonFile)
        elif action == 'w':
            json.dump(fileData, jsonFile, indent=4)
        jsonFile.close()
        return fileData


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


# Création/vérifcation du fichier config
config = verify_file(mainFiles, 'config', configJson)
token = config['token']


@client.event
async def on_ready():
    devoirs_pronote.start()
    print('Connecté en temps que {0.user.name} !'.format(client))


@tasks.loop(seconds=300)
async def devoirs_pronote():
    if datetime.now().hour not in [22, 23, 0, 1, 2, 3, 4, 5]:
        filesDir = './'
        configPronote = verify_file(filesDir, 'pronote',
                                    {'username': None, 'password': None, 'folderName': None, 'channelID': None,
                                    'url': None})

        if configPronote['username'] != None and configPronote['password'] != None and configPronote['url'] != None:
            pronote = pronotepy.Client(configPronote['url'], username=configPronote['username'],
                                       password=configPronote['password'])

            if configPronote['folderName'] != None:
                os.makedirs(configPronote['folderName'])
                filesDir += f'{configPronote["folderName"]}/'

            if (pronote.logged_in and (configPronote['channelID'] != None)):
                devoirs = pronote.homework(pronote.start_day,
                                           pronote.start_day + timedelta(days=360))
                devoirsFile = verify_file(filesDir, 'devoirs', [])
                devoirsList = []
                for i in devoirs:
                    description = i.description.replace('\n', ' ')
                    devoirsList.append(f'{i.date} : {i.subject.name} {description}')

                if len(devoirsList) > len(devoirsFile):
                    open_file(filesDir, 'devoirs', 'w', devoirsList)
                    devoirsNewNbr = len(devoirsList) - len(devoirsFile)
                    print(f'[PRONOTE] {devoirsNewNbr} nouveaux devoirs !')
                    pronoteChannel = client.get_channel(int(configPronote['channelID']))
                    for i in range(devoirsNewNbr):
                        embed = discord.Embed(title=devoirs[len(devoirsFile) + i].subject.name,
                                              description=devoirs[len(devoirsFile) + i].description.replace('\n', ' '),
                                              color=0x1E744F)
                        embed.set_author(name=f'Pour le {devoirs[len(devoirsFile) + i].date}')
                        await pronoteChannel.send(embed=embed)


if token != None:
    client.run(token)
else:
    print('Pas de token dans le fichier config')
