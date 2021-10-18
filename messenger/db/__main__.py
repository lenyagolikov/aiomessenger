"""
Утилита для управления состоянием базы данных, обертка над alembic.

Можно вызывать из любой директории, а также указать произвольный DSN для базы
данных, отличный от указанного в файле alembic.ini.
"""
import argparse
import os

from alembic.config import CommandLine

from messenger.utils.db import DB_URL, make_alembic_config


def main():
    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    alembic.parser.add_argument(
        '--db-url', default=os.getenv('DB_URL', 'postgresql' + DB_URL),
    )

    options = alembic.parser.parse_args()

    if 'cmd' not in options:
        alembic.parser.error('too few arguments')
        exit(128)
    else:
        config = make_alembic_config(options)
        exit(alembic.run_cmd(config, options))


if __name__ == '__main__':
    main()
