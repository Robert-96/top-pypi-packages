from loguru import logger

from .build import build_project


logger.level('INFO')
build_project(develop=True)
