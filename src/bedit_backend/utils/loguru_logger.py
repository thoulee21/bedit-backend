import logging
import sys

from loguru import logger


class InterceptHandler(logging.StreamHandler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # 官方实现中使用record.getMessage()来获取msg，但在sanic中会漏掉它配置过的日志模板，因此要用self.format(record)
        msg = self.format(record)
        logger.opt(depth=depth, exception=record.exc_info).log(level, msg)


logging.basicConfig(handlers=[InterceptHandler()], level=0)
logger.configure(handlers=[{"sink": sys.stderr, "level": 'INFO'}])

logger.add(
    'access.log',
    encoding='utf-8',
    enqueue=True,
    level='INFO',
    compression='zip',
    rotation='10 MB',
    retention="10 days",
    format='{time} {message}'
)
