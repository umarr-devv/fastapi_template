import logging
from logging import StreamHandler, basicConfig
from logging.handlers import TimedRotatingFileHandler

from core.config import ConfigModel
from core.paths import LOG_DIR

LOG_FILE = LOG_DIR / '.log'


def set_logging(config: ConfigModel):
    basicConfig(
        level=config.logging.level,
        format=config.logging.format,
        handlers=[
            StreamHandler(),
            TimedRotatingFileHandler(
                filename=LOG_FILE,
                when=config.logging.when,
                interval=config.logging.interval,
                encoding='utf-8'
            )
        ]
    )
    logging.getLogger("watchfiles.main").setLevel(logging.CRITICAL)
