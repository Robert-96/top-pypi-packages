import json
import functools
import os.path

import requests
from loguru import logger
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache


PACKAGE_COUNT = 1000

TOP_30_DAYS_URL = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json'
TOP_365_DAYS_URL = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-365-days.min.json'

PYPI_PROJECT_URL = 'https://pypi.org/pypi/{}/json'
PACKAGE_URL = 'https://pypi.org/project/{}'

CACHE_FILE = 'cache/data.json'

file_cache = FileCache('cache/.web', forever=True)
session = CacheControl(requests.Session(), file_cache)


def cache(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.isfile(filename):
                with open(filename) as fp:
                    return json.load(fp)

            value = func(*args, **kwargs)

            if not os.path.exists(filename):
                with open(filename, 'w') as fp:
                    json.dump(value, fp, indent=2, sort_keys=True)

            return value
        return wrapper
    return decorator


def get_top_packages(file):
    """Download and return a list of most downloaded packages on PyPI."""

    response = session.get(file)
    data = response.json().get('rows')
    return normalize_packages_data(data)


@cache('cache/30-days.json')
def get_top_30_days():
    """Download and return a list of most downloaded packages on PyPI."""

    return get_top_packages(TOP_30_DAYS_URL)


@cache('cache/365-days.json')
def get_top_365_days():
    """Download and return a list of most downloaded packages on PyPI."""

    return get_top_packages(TOP_365_DAYS_URL)


def normalize_packages_data(packages):
    normalized_rows = list()

    for index, package in enumerate(packages[:PACKAGE_COUNT], start=1):
        project = package.get('project')
        downloads = package.get('download_count')

        data = get_pypi_data(project)

        data['index'] = index
        data['download_count'] = downloads

        normalized_rows.append(data)

    return normalized_rows


def get_pypi_data(package):
    """Download PyPi info for the given package.

    Args:
        package (:obj:`str`): The name of the package.

    """

    logger.info('Download: {}'.format(package))

    try:
        response = session.get(PYPI_PROJECT_URL.format(package))
        data = response.json()
        info = data.get('info', {})

        return normalize_pypi_data(info)
    except Exception as error:
        logger.exception(str(error))
        logger.info('Skip: {}'.format(package))

        return {
            'name': package,
            'package_url': PACKAGE_URL.format(package),
            'summary': '',
        }


def normalize_pypi_data(info):
    """Normalize PyPi data from a package.

    Args:
        info (:obj:`dict`): A dict containing the data downloaded from PyPi.

    """

    data = {
        'name': info.get('name'),
        'summary': info.get('summary', ''),
        'version': info.get('version'),
        'url': info.get('project_url'),
    }

    if not info.get('keywords'):
        data['keywords'] = []
    elif ',' in info.get('keywords', ''):
        data['keywords'] = info.get('keywords', '').lower().split(',')
    else:
        data['keywords'] = info.get('keywords', '').lower().split()

    if not info.get('license'):
        data['license'] = None
    else:
        data['license'] = info['license'][:64]

    return data


if __name__ == "__main__":
    import pprint

    top_30_days = get_top_30_days()

    print('Top 30 Days Length: {}'.format(len(top_30_days)))
    pprint.pprint(top_30_days[:5], indent=2)

    top_365_days = get_top_365_days()

    print('Top 365 Days Length: {}'.format(len(top_365_days)))
    pprint.pprint(top_365_days[:5], indent=2)
