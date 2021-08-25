import datetime

from rost import Rost
from loguru import logger

from .__version__ import VERSION
from .download import get_top_30_days, get_top_365_days


logger.level("INFO")


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
            ('30-days.html', lambda: {'projects': get_top_30_days()}),
            ('365-days.html', lambda: {'projects': get_top_365_days()})
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
    build_project(develop=False)
