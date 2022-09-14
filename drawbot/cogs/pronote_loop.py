import time

import discord
import pronotepy
from discord.ext import commands, tasks

from drawbot.utils import fetch_homeworks, fetch_grades, chunks


class LoopHandler(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.refresh_pronote.start()

    def cog_unload(self):
        self.refresh_pronote.cancel()

    @tasks.loop(minutes=5)
    async def refresh_pronote(self):
        await self.client.wait_until_ready()
        date = time.strftime("%Y-%m-%d %H:%M", time.gmtime())

        try:
            pronote: pronotepy.Client = pronotepy.Client(
                self.client.config["url"],
                self.client.config["username"],
                self.client.config["password"],
            )

        except pronotepy.CryptoError:
            print(
                "Connexion à Pronote échoué. "
                "Mauvais nom d'utilisateur ou mot de passe."
            )
            await self.client.close()
            return

        except pronotepy.PronoteAPIError:
            print(f"{date} - Connexion à Pronote échoué")
            return

        if not pronote.logged_in:
            print(f"{date} - Connexion à Pronote échoué")
            return

        try:
            pronote_channel: discord.TextChannel = await self.client.fetch_channel(
                int(self.client.config.get("channelID"))
            )
        except discord.errors.NotFound:
            print("Channel non-trouvé ou inexistant")
            await self.client.close()
            return

        def discord_timestamp(t_str: str) -> str:
            return f"<t:{int(time.mktime(time.strptime(t_str, '%Y-%m-%d')))}:D>"

        new_homework_count = 0
        for homeworks in chunks(list(fetch_homeworks(pronote)), 10):
            new_homework_count += len(homeworks)
            await pronote_channel.send(
                embeds=[
                    discord.Embed(
                        title=(
                            f"Nouveau devoir de {homework['subject']}\n"
                            f"Pour le {discord_timestamp(homework['date'])}"
                        ),
                        description=homework["description"],
                        color=0x1E744F,
                    )
                    for homework in homeworks
                ]
            )

        new_grades_count = 0
        for grades in chunks(list(fetch_grades(pronote)), 10):
            new_grades_count += len(grades)
            await pronote_channel.send(
                embeds=[
                    discord.Embed(
                        title=(
                            f"Nouvelle note de {grade['subject']}\n"
                            f"Du {discord_timestamp(grade['date'])}"
                        ),
                        description=(
                            f"Note élève : **{grade['grade']}**\n"
                            f"Moy. classe : **{grade['average']}**\n"
                            f"Coefficient : **{grade['coefficient']}**\n"
                            f"Note + : **{grade['max']}**\n"
                            f"Note - : **{grade['min']}**\n"
                        ),
                        color=0x1E744F,
                    )
                    for grade in grades
                ]
            )

        print(
            f"{date} "
            f"- {new_homework_count} nouveaux devoirs "
            f"- {new_grades_count} nouvelles notes !"
        )


async def setup(client: commands.Bot) -> None:
    LoopHandler(client)
