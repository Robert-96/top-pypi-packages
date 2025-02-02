"""A simple script that downloads a list for the most downloaded packages for PyPI."""

import os
import json
import functools

import requests
from loguru import logger
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache


PACKAGE_COUNT = 5000
TOP_PACKAGES_URL = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json'

PYPI_PROJECT_URL = 'https://pypi.org/pypi/{}/json'
PACKAGE_URL = 'https://pypi.org/project/{}'

file_cache = FileCache('cache/.web', forever=True)
session = CacheControl(requests.Session(), file_cache)


def cache(filename=None):
    """Cache function return value."""

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


@cache('cache/data.json')
def get_top_packages():
    """Download and return a list of most downloaded packages on PyPI."""

    response = session.get(TOP_PACKAGES_URL)
    data = response.json().get('rows')
    return normalize_packages_data(data)


def normalize_packages_data(packages):
    """Given a list of packages download data form PyPI for each package.

    Args:
        package (:obj:`list`): A list of package names.

    """

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
    """Download PyPI info for the given package.

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
    """Normalize PyPI data from a package.

    Args:
        info (:obj:`dict`): A dict containing the data downloaded from PyPI.

    """

    data = {
        'name': info.get('name'),
        'version': info.get('version'),
        'url': info.get('project_url'),
        'summary': info.get('summary') or '',
    }

    if not info.get('keywords'):
        data['keywords'] = []
    elif ',' in info.get('keywords', ''):
        data['keywords'] = info.get('keywords', '').lower().split(',')
    else:
        data['keywords'] = info.get('keywords', '').lower().split()

    data['keywords'] = list(set(keyword for keyword in data['keywords'] if keyword))

    if not info.get('license'):
        data['license'] = None
    else:
        data['license'] = info['license'][:64]

    return data


if __name__ == "__main__":
    import pprint

    pprint('Download the list of the top packages from PyPI...')
    top_packages = get_top_packages()

    print('Length: {}'.format(len(top_packages)))
    pprint.pprint(top_packages[:5], indent=2)
