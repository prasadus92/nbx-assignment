import json

from aiohttp import web

from userservice.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST


def json_error(status_code: int, exception: Exception) -> web.Response:
    return web.Response(
        status=status_code,
        body=json.dumps({
            'error': str(exception)
        }).encode('utf-8'),
        content_type='application/json')


async def error_middleware(app, handler):
    async def middleware_handler(request):
        try:
            response = await handler(request)
            if response.status == HTTP_404_NOT_FOUND or response.status == HTTP_400_BAD_REQUEST:
                return json_error(response.status, Exception(response.message))
            return response
        except web.HTTPException as ex:
            return json_error(ex.status, ex)
        except Exception as e:
            return json_error(HTTP_500_INTERNAL_SERVER_ERROR, e)

    return middleware_handler


def setup_middlewares(app):
    app.middlewares.append(error_middleware)
