"""Requires running Postgres"""


async def test_health(cli, tables_and_data):
    response = await cli.get('/')
    assert response.status == 200
    assert 'user-service' in await response.text()


async def test_get_users(cli, tables_and_data):
    response = await cli.get('/users')
    assert response.status == 200
    assert 'Bruce Wayne' in await response.text()
