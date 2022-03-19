"""A simple script that build a webpage with the most downloaded packages from PyPi."""

import os
import json
import datetime
import functools

from rost import Rost
from loguru import logger

from .__version__ import VERSION
from .download import get_top_packages
from .filters import format_number, format_download_count


def create_json_file(searchpath, outputpath, packages=None):
    json_directory = os.path.join(outputpath, 'json')
    json_file = os.path.join(json_directory, 'packages.json')

    os.mkdir(json_directory)

    with open(json_file, 'w') as fp:
        json.dump(packages, fp)


def build_project(develop=False):
    """Build the project.

    Args:
        develop (:obj:`bool`): If set to ``True`` it will start a dev server.
            Defaults to ``False``.

    """

    TIMESTAMP = str(datetime.datetime.now())
    PACKAGES = get_top_packages()

    generator = Rost(
        searchpath='templates',
        staticpaths=['public'],
        context={
            'version': VERSION,
            'timestamp': TIMESTAMP,
        },
        contexts=[
            ('index.html', lambda: {'packages': PACKAGES}),
        ],
        filters={
            'format_number': format_number,
            'format_download_count': format_download_count
        },
        before_callback=functools.partial(create_json_file, packages=PACKAGES)
    )

    if develop:
        logger.info('Start dev server on http://localhost:8080/')
        generator.watch(use_livereload=True)
    else:
        logger.info('Build project...')
        generator.build()


if __name__ == '__main__':
    logger.level('INFO')
    build_project(develop=False)
