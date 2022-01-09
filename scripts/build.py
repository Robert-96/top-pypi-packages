"""A simple script that build a webpage with the most downloaded packages from PyPi."""

import datetime

from rost import Rost
from loguru import logger

from .__version__ import VERSION
from .download import get_top_packages
from .filters import format_number, format_download_count


def build_project(develop=False):
    """Build the project.

    Args:
        develop (:obj:`bool`): If set to ``True`` it will start a dev server.
            Defaults to ``False``.

    """

    generator = Rost(
        searchpath='templates',
        staticpaths=['public'],
        context={
            'version': VERSION,
            'timestamp': str(datetime.datetime.now()),
        },
        contexts=[
            ('index.html', lambda: {'packages': get_top_packages()}),
        ],
        filters={
            'format_number': format_number,
            'format_download_count': format_download_count
        },
    )

    if develop:
        logger.info('Start dev server on http://localhost:8080/')
        generator.watch(monitorpaths=['public'])
    else:
        logger.info('Build project...')
        generator.build()


if __name__ == '__main__':
    logger.level('INFO')
    build_project(develop=False)
