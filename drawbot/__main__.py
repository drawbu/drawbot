import sys
from typing import List

from drawbot import Bot


def main(argc: int, argv: List[str]):
    """Entry point to run the bot client."""
    bot = Bot(argv[1] if argc > 1 else "vars")
    bot.run()


if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
