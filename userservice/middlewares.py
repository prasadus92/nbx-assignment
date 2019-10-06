import logging

logger = logging.getLogger(__name__)


async def request_logging_middleware(app, handler):
    async def middleware_handler(request):
        logger.info(request)
        return await handler(request)

    return middleware_handler


def setup_middlewares(app):
    app.middlewares.append(request_logging_middleware)
