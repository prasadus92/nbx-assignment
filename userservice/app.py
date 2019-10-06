import json
import logging

import ujson
from aiohttp import web

from userservice.encoders import UUIDEncoder
from userservice.status import HTTP_200_OK, HTTP_201_CREATED
from . import db

LOGGER = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.get('/')
async def health(request):
    """
        ---
        description: This end-point allow to test that service is up.
        tags:
        - Health check
        produces:
        - application/json
        responses:
            "200":
                description: successful operation. Returns "{'name': 'user-service'}" JSON
    """
    return web.json_response({'name': 'user-service'})


@routes.get('/users')
async def get_users(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.user.select())
        records = await cursor.fetchall()
        users = [dict(u) for u in records]
        return web.json_response(body=json.dumps(users, cls=UUIDEncoder), status=HTTP_200_OK)


@routes.post('/users')
async def create_user(request):
    data = await request.json(loads=ujson.loads)
    async with request.app['db'].acquire() as conn:
        try:
            user = await db.create_user(conn, data['name'], data['email'])
        except Exception as e:
            raise web.HTTPBadRequest(text=str(e))

        return web.json_response(body=json.dumps(user, cls=UUIDEncoder), status=HTTP_201_CREATED)


@routes.get('/users/{user_id}')
async def get_user(request):
    user_id = request.match_info['user_id']
    async with request.app['db'].acquire() as conn:
        try:
            user = await db.get_user(conn, user_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        return web.json_response(body=json.dumps(user, cls=UUIDEncoder), status=HTTP_200_OK)


@routes.put('/users/{user_id}')
async def update_user(request):
    user_id = request.match_info['user_id']
    data = await request.json(loads=ujson.loads)
    async with request.app['db'].acquire() as conn:
        try:
            user = await db.update_user(conn, user_id, data['name'], data['email'])
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        return web.json_response(body=json.dumps(user, cls=UUIDEncoder), status=HTTP_200_OK)


@routes.delete('/users/{user_id}')
async def delete_user(request):
    user_id = request.match_info['user_id']
    async with request.app['db'].acquire() as conn:
        try:
            await db.delete_user(conn, user_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
    return web.json_response(None, status=204)


def create_app():
    app = web.Application()
    app.add_routes(routes)
    return app
