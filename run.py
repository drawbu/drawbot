from app.bot import Bot


def main() -> None:
    """Entry point to run the bot client."""
    bot: Bot = Bot()
    bot.run()


if __name__ == '__main__':
    main()
