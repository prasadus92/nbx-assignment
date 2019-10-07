from userservice.views import health, get_users, get_user, create_user, update_user, delete_user


def setup_routes(app):
    app.router.add_get('/', health)
    app.router.add_get('/users', get_users)
    app.router.add_post('/users', create_user)
    app.router.add_get('/users/{user_id:[0-9a-fA-F]+}', get_user)
    app.router.add_put('/users/{user_id:[0-9a-fA-F]+}', update_user)
    app.router.add_delete('/users/{user_id:[0-9a-fA-F]+}', delete_user)
