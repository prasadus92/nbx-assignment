from userservice.views import health, get_users, get_user, create_user, update_user, delete_user


def setup_routes(app):
    app.router.add_get('/', health, name='health')
    app.router.add_get('/users', get_users, name='get-users')
    app.router.add_post('/users', create_user, name='create-user')
    app.router.add_get('/users/{id:[0-9a-fA-F]+}', get_user, name='get-user')
    app.router.add_put('/users/{id:[0-9a-fA-F]+}', update_user, name='update-user')
    app.router.add_delete('/users/{id:[0-9a-fA-F]+}', delete_user, name='delete-user')
