import json
import os
import discord
import pronotepy
from discord.ext import commands, tasks
from datetime import datetime, timedelta


class Pronote(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.homeworks_pronote.start()

    @tasks.loop(seconds=300)
    async def homeworks_pronote(self):
        if datetime.now().hour not in [22, 23, 0, 1, 2, 3, 4, 5]:
            files_dir = ''
            config_pronote = open_file(files_dir, 'pronote', 'r')

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
                    devoirs_file = open_file(files_dir, 'devoirs', 'r')
                    devoirs_list = []
                    for i in devoirs:
                        description = i.description.replace('\n', ' ')
                        devoirs_list.append(f'{i.date} : {i.subject.name} {description}')

                    if len(devoirs_list) > len(devoirs_file):
                        open_file(files_dir, 'devoirs', 'w', devoirs_list)
                        devoirs_new_nbr = len(devoirs_list) - len(devoirs_file)
                        print(f'[PRONOTE] {devoirs_new_nbr} nouveaux devoirs !')
                        pronote_channel = self.client.get_channel(int(config_pronote['channelID']))
                        for i in range(devoirs_new_nbr):
                            embed = discord.Embed(title=devoirs[len(devoirs_file) + i].subject.name,
                                                  description=devoirs[len(devoirs_file) + i].description.replace('\n', ' '),
                                                  color=0x1E744F)
                            embed.set_author(name=f'Pour le {devoirs[len(devoirs_file) + i].date}')
                            await pronote_channel.send(embed=embed)


# Fonction principales (fonctions très utiles)
def open_file(repertory, file, action, file_data=None):
    with open(repertory + file + '.json', action) as json_file:
        if action == 'r':
            file_data = json.load(json_file)
        elif action == 'w':
            json.dump(file_data, json_file, indent=4)
        return file_data


def setup(client):
    client.add_cog(Pronote(client))
