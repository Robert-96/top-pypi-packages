from loguru import logger

from .build import build_project


logger.level("INFO")
logger.info("Start dev server on localhost:8080/")

build_project(develop=True)
