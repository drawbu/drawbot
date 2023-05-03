import sys
from typing import List, Final

from drawbot import Bot

DEFAULT_CONFIG_PATH: Final[str] = "vars"

EXIT_OK: Final[int] = 0
EXIT_FAILURE: Final[int] = 1


def main(argc: int, argv: List[str]) -> int:
    """Entry point to run the bot client."""
    bot = Bot(argv[1] if argc > 1 else DEFAULT_CONFIG_PATH)

    if not bot.is_configured:
        return EXIT_FAILURE

    if not bot.run():
        return EXIT_FAILURE

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
