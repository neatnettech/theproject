# logging_setup.py
import structlog
import logging
import sys
from structlog.stdlib import LoggerFactory
from structlog.processors import JSONRenderer, TimeStamper, add_log_level, format_exc_info
from structlog.contextvars import merge_contextvars

def setup_logger():
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            merge_contextvars,
            add_log_level,
            TimeStamper(fmt="iso"),
            format_exc_info,
            JSONRenderer()
        ],
        logger_factory=LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()