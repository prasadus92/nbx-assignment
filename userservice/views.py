import json
import logging

from aiohttp import web
from aiohttp_validate import validate

from userservice.encoders import CustomEncoder
from userservice.schema import USER_CREATE_REQUEST_SCHEMA, USER_CREATE_RESPONSE_SCHEMA, USER_UPDATE_REQUEST_SCHEMA, \
    USER_UPDATE_RESPONSE_SCHEMA
from userservice.status import HTTP_200_OK, HTTP_201_CREATED
from . import db

LOGGER = logging.getLogger(__name__)


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
            description: Successful operation. Returns the name of the service
    """
    return web.json_response({'name': 'user-service'})


# ToDo: Pagination
async def get_users(request):
    """
    ---
    description: This end-point allows to fetch all the users.
    tags:
    - Get all users
    produces:
    - application/json
    responses:
        "200":
            description: Successful operation. Returns a list of users
    """
    LOGGER.info("### Received a new GET users request ###")
    async with request.app['db'].acquire() as conn:
        users = await db.get_all_users(conn)
        return web.json_response(body=json.dumps(users, cls=CustomEncoder), status=HTTP_200_OK)


@validate(
    request_schema=USER_CREATE_REQUEST_SCHEMA,
    response_schema=USER_CREATE_RESPONSE_SCHEMA,
)
async def create_user(self, request):
    """
    ---
    description: This end-point allows to create a new user.
    tags:
    - Create user
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      description: User object
      required: true
      schema:
        type: object
        properties:
          name:
            type: string
          email:
            type: string
    responses:
        "201":
            description: Successful operation. Returns the created user
    """
    data = await request.json(loads=json.loads)
    LOGGER.info("### Received a new CREATE user request with payload - %s ###", data)
    async with request.app['db'].acquire() as conn:
        try:
            user = await db.create_user(conn, data['name'], data['email'])
        except Exception as e:
            raise web.HTTPBadRequest(text=str(e))

        return web.json_response(body=json.dumps(user, cls=CustomEncoder), status=HTTP_201_CREATED)


async def get_user(request):
    """
    ---
    description: This end-point allows to fetch an existing user.
    tags:
    - Create user
    produces:
    - application/json
    parameters:
    - in: path
      name: user_id
      type: string
    responses:
        "200":
            description: Successful operation. Returns the found user
        "404":
            description: Unsuccessful operation or user not found
    """
    user_id = request.match_info['user_id']
    LOGGER.info("### Received a new GET user request for User ID - %s ###", user_id)
    async with request.app['db'].acquire() as conn:
        try:
            user = await db.get_user(conn, user_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        return web.json_response(body=json.dumps(user, cls=CustomEncoder), status=HTTP_200_OK)


@validate(
    request_schema=USER_UPDATE_REQUEST_SCHEMA,
    response_schema=USER_UPDATE_RESPONSE_SCHEMA,
)
async def update_user(self, request):
    """
    ---
    description: This end-point allows to update the details of an existing user.
    tags:
    - Update user
    produces:
    - application/json
    parameters:
    - in: path
      name: user_id
      type: string
    - in: body
      name: body
      description: User object
      required: true
      schema:
        type: object
        properties:
          name:
            type: string
          email:
            type: string
    responses:
        "200":
            description: Successful operation. Returns the updated user
        "404":
            description: Unsuccessful operation or user not found
    """
    user_id = request.match_info['user_id']
    LOGGER.info("### Received a new UPDATE user request for User ID - %s ###", user_id)
    data = await request.json(loads=json.loads)
    async with request.app['db'].acquire() as conn:
        try:
            user = await db.update_user(conn, user_id, data['name'], data['email'])
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        return web.json_response(body=json.dumps(user, cls=CustomEncoder), status=HTTP_200_OK)


async def delete_user(request):
    """
    ---
    description: This end-point allows to delete an existing user.
    tags:
    - Delete user
    produces:
    - application/json
    parameters:
    - in: path
      name: user_id
      type: string
    responses:
        "204":
            description: Successful operation. Returns no content
        "404":
            description: Unsuccessful operation or user not found
    """
    user_id = request.match_info['user_id']
    LOGGER.info("### Received a new DELETE user request for User ID - %s ###", user_id)
    async with request.app['db'].acquire() as conn:
        try:
            await db.delete_user(conn, user_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
    return web.json_response(None, status=204)
