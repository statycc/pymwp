import logging

logger = logging.getLogger(__name__)


class Analysis:

    def __init__(self, file: str):
        logger.info("Starting analysis on file: %s", file)

        print(file)
