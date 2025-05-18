import logging
from logging import StreamHandler, basicConfig
from logging.handlers import TimedRotatingFileHandler

from core.config import ConfigModel
from core.paths import LOG_DIR

LOG_FILE = LOG_DIR / '.log'
LOG_FORMAT = '%(name)s | %(asctime)s | %(funcName)s | %(filename)s | %(levelname)s | %(message)s'
LOG_INTERVAl = 7


def set_logging(config: ConfigModel):
    basicConfig(
        level=config.log_level,
        format=LOG_FORMAT,
        handlers=[
            StreamHandler(),
            TimedRotatingFileHandler(
                filename=LOG_FILE,
                when='D',
                interval=LOG_INTERVAl,
                encoding='utf-8'
            )
        ]
    )
    logging.getLogger("watchfiles.main").setLevel(logging.WARNING)
