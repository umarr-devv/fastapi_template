import logging
from logging import StreamHandler, basicConfig
from logging.handlers import TimedRotatingFileHandler

from core.config import config
from core.paths import LOG_DIR

LOG_FILE = LOG_DIR / '.log'


class Logging:
    handlers: list[logging.Handler] = [
        StreamHandler(),
        TimedRotatingFileHandler(
            filename=LOG_FILE,
            when=config.logging.when,
            interval=config.logging.interval,
            encoding='utf-8'
        )
    ]

    @classmethod
    def exclude_watch_files(cls):
        logging.getLogger("watchfiles.main").setLevel(logging.CRITICAL)

    @classmethod
    def set(cls):
        basicConfig(
            level=config.logging.level,
            format=config.logging.format,
            handlers=cls.handlers
        )
        cls.exclude_watch_files()
