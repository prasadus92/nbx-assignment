from aiohttp import web
from app import create_app
import logging


LOGGER = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    LOGGER.info('### Starting user service ###')
    app = create_app()
    web.run_app(app)