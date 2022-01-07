"""A simple script that build a webpage with the most downloaded packages from PyPi."""

import datetime

from rost import Rost
from loguru import logger

from .__version__ import VERSION
from .download import get_top_packages


def format_number(number):
    return "{:,}".format(number)


def format_download_count(number):
    B = 1_000_000_000
    M = 1_000_000
    K = 1_000

    if number > B:
        return "{:.2f}B".format(number / B)
    if number > M:
        return "{:.2f}M".format(number / M)
    elif number > K:
        return "{:.2f}K".format(number / K)
    else:
        return str(number)


def build_project(develop=False):
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
        generator.watch(monitorpaths=['public'])
    else:
        generator.build()


if __name__ == "__main__":
    logger.level("INFO")
    logger.info("Build project...")

    build_project(develop=False)
