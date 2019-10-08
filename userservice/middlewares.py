import json

from aiohttp import web


def json_error(status_code: int, exception: Exception) -> web.Response:
    return web.Response(
        status=status_code,
        body=json.dumps({
            'error': str(exception)
        }).encode('utf-8'),
        content_type='application/json')


async def error_middleware(app: web.Application, handler):
    async def middleware_handler(request):
        try:
            response = await handler(request)
            if response.status == 404 or response.status == 400:
                return json_error(response.status, Exception(response.message))
            return response
        except web.HTTPException as ex:
            return json_error(ex.status, ex)
        except Exception as e:
            return json_error(500, e)

    return middleware_handler


def setup_middlewares(app):
    app.middlewares.append(error_middleware)
