import time

import discord
import pronotepy
from discord.ext.commands import Context
from discord.ext import commands, tasks

from ..json_types import JsonDict
from ..utils import json_wr, fetch_homeworks, fetch_grades


class Pronote(commands.Cog):
    def __init__(self, client):
        """Initialize the search for new homeworks."""
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.refresh_pronote.start()

    @tasks.loop(seconds=300)
    async def refresh_pronote(self):

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

        auths = {"homeworks": True, "grades": True}

        if auths["homeworks"]:
            new_homework_count = 0
            for homework in fetch_homeworks(pronote):
                new_homework_count += 1
                await pronote_channel.send(
                    embed=discord.Embed(
                        title=(
                            f"Nouveau devoir de {homework['subject']}\n"
                            f"Pour le {discord_timestamp(homework['date'])}"
                        ),
                        description=homework["description"],
                        color=0x1E744F,
                    )
                )

        if auths["grades"]:
            new_grades_count = 0
            for grade in fetch_grades(pronote):
                new_grades_count += 1
                await pronote_channel.send(
                    embed=discord.Embed(
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
                )

        print(
            (date if any(auths) else "")
            + (
                ""
                if not auths["homeworks"]
                else f" - {new_homework_count} nouveaux devoirs"
            )
            + ("" if not auths["grades"] else f" - {new_grades_count} nouveaux notes")
            + (" !" if any(auths) else "")
        )

    @commands.command(name="homeworks", aliases=("devoirs",))
    async def change_channel(self, ctx: Context) -> None:
        homeworks: JsonDict = json_wr("devoirs")

        embed = discord.Embed(title="Prochains devoirs", color=self.client.embed_color)

        today = time.time()
        homeworks_dict = {}
        for date, homeworks_list in homeworks.items():

            date_timestamp = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
            if date_timestamp >= today:
                homeworks_dict[date_timestamp] = homeworks_list

        homeworks_dict = {key: homeworks_dict[key] for key in sorted(homeworks_dict)}

        for date, homeworks_list in homeworks_dict.items():
            embed.add_field(
                name=f"Pour le <t:{date}:D>",
                value="\n".join(
                    [
                        f"**- {h['subject']} :** {h['description']}"
                        for h in homeworks_list
                    ]
                ),
                inline=False,
            )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Pronote(client))
