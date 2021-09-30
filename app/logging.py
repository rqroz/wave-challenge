"""
Application logger configuration.
"""
import json
import structlog
import logging
import logging.config

from flask import Flask, request

from app.config import Config


class RequestContext(logging.Filter):
    """ Enhances log messages with contextual information """
    def filter(self, record):
        try:
            record.request = {
                'remote_ip': request.remote_addr,
                'method': request.method,
                'path': request.path,
                'headers': dict(request.headers),
            }
        except RuntimeError:
            pass
        return True


class HealthFilter(logging.Filter):
    """ Health route filter """
    def filter(self, record):
        request = getattr(record, 'request', None)
        return '/health' not in request.get('path') if request else True


def configure_logging():
    """
    Logging setup.
    """
    timestamper = structlog.processors.TimeStamper(
        fmt='ISO',
        utc=True,
    )
    pre_chain = [
        structlog.stdlib.add_log_level,
        timestamper,
    ]
    filters = ['request_context', 'health_filter']
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.dev.ConsoleRenderer(colors=True),
                'foreign_pre_chain': pre_chain,
            },
        },
        'filters': {
            'health_filter': {
                '()': HealthFilter,
            },
            'request_context': {
                '()': RequestContext,
            },
        },
        'handlers': {
            'console': {
                'level': Config.LOG_LEVEL,
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'filters': filters,
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'werkzeug': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False
            },
        },
    }
    logging.config.dictConfig(config)
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            timestamper,
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def logging_setup(app: Flask):
    configure_logging()

    @app.after_request
    def log_access(response):
        data = '<not printable>'
        if response.headers.get('Content-Type') == 'application/json':
            try:
                data = response.get_data().decode('utf-8')
            except UnicodeDecodeError:
                pass

        try:
            log_message = json.loads(data)
        except json.JSONDecodeError:
            log_message = data
        structlog.get_logger('access').info('RESPONSE', status=response.status_code, data=log_message)
        return response
