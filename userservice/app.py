import logging
import sys

from aiohttp import web
from aiohttp_swagger import *

from userservice.db import close_pg, init_pg
from userservice.routes import setup_routes
from userservice.settings import get_config

LOGGER = logging.getLogger(__name__)


def init_app(argv=None):
    app = web.Application()

    setup_routes(app)

    app['config'] = get_config(argv)

    # Create db connection on startup, shutdown on exit
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    setup_swagger(app)

    return app


def main(argv):
    logging.basicConfig(level=logging.INFO)
    LOGGER.info('### Starting user service ###')

    app = init_app(argv)

    config = get_config(argv)
    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
