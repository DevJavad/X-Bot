import logging
import os
from logging.handlers import TimedRotatingFileHandler

from colorama import Fore, Style, init

from app.settings import Config, BASE_DIR

init(autoreset=True)

PATH: str = BASE_DIR / "logs"
FILENAME: str = "data.log"
TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
FORMAT: str = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"


BOLD = Style.BRIGHT
RESET = Style.RESET_ALL
BLUE = BOLD + Fore.BLUE


class Formatter(logging.Formatter):
    COLORS = {
        "DEBUG": Fore.CYAN + BOLD,
        "INFO": Fore.GREEN + BOLD,
        "WARNING": Fore.YELLOW + BOLD,
        "ERROR": Fore.RED + BOLD,
        "CRITICAL": Fore.MAGENTA + BOLD,
    }

    LEVEL_WIDTH = 9

    def format(self, record):
        level_color = self.COLORS.get(record.levelname, "")

        asctime = self.formatTime(record, self.datefmt)
        level = record.levelname
        name = record.name
        message = record.getMessage()

        return (
            f"{Fore.BLACK}{asctime}{RESET} "
            f"| {BLUE}{name}{RESET} "
            f"| {level_color}{level}{RESET} | "
            f"{message}"
        )

def setup_logger(config: Config) -> None:
    os.makedirs(PATH, exist_ok=True)

    filename = os.path.join(PATH, FILENAME)
    formatter = Formatter(datefmt=TIME_FORMAT)
    file_rotate = TimedRotatingFileHandler(filename, when="midnight", encoding="utf-8")

    root_logger = logging.getLogger()
    root_logger.setLevel(config.logger.level)

    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)
    stream.setFormatter(formatter)

    file_handler = file_rotate
    file_handler.setLevel(config.logger.level)
    file_handler.setFormatter(logging.Formatter(FORMAT, TIME_FORMAT))

    root_logger.addHandler(stream)
    root_logger.addHandler(file_handler)

    aiogram_logger = logging.getLogger("aiogram")
    aiogram_logger.setLevel(logging.DEBUG)
    # aiogram_logger.propagate = False

    aiogram_file = file_rotate
    aiogram_file.setLevel(logging.DEBUG)
    aiogram_file.setFormatter(logging.Formatter(FORMAT, TIME_FORMAT))

    aiogram_logger.addHandler(aiogram_file)

    logging.getLogger("aiosqlite").setLevel(logging.CRITICAL)
    logging.getLogger("tortoise").setLevel(logging.CRITICAL)
