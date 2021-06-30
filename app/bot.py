import json
from discord.ext import commands


class Bot(commands.Bot):

    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)

        super().__init__(config.get('prefix'))
        self._token = config.get('token')

    def run(self):
        if not self._token:
            return

        super().run(self._token)


def main():
    bot = Bot()
    bot.run()


if __name__ == '__main__':
    main()
