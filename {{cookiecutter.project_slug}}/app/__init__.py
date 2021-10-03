import logging

from app.core.config import Config

__version__ = "{{cookiecutter.project_version}}"

logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(Config.LOGGING_LEVEL)
logger.info("Version %s", __version__)
