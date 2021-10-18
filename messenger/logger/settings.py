import os

from . import filters

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logger')

LOGGER_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '{levelname} - {asctime} - {message}',
            'style': '{',
        },
    },

    'handlers': {
        'debug_console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format'
        },
        'debug_file': {
            '()': filters.MegaHandler,
            'level': 'DEBUG',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'std_format',
            'filters': ['debug_filter'],
        },
        'error_file': {
            '()': filters.MegaHandler,
            'level': 'ERROR',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),
            'formatter': 'std_format',
            'filters': ['error_filter']
        },
    },

    'loggers': {
        'log': {
            'level': 'DEBUG',
            'handlers': [
                'debug_console', 'debug_file', 'error_file'
            ],
        },
    },

    'filters': {
        'debug_filter': {
            '()': filters.DebugFilter,
        },
        'error_filter': {
            '()': filters.ErrorFilter,
        },
    }
}
