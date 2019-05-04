import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import remember, forget, authorized_userid
from web_pools.modules import db
from web_pools.modules import utils


def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)


@aiohttp_jinja2.template('login.html')
async def get(request):
    config = request.app["config"]
    username = await authorized_userid(request)
    if username:
        raise redirect(request.app.router, 'index')
    return dict(title=config.project_name)


@aiohttp_jinja2.template('login.html')
async def post(request):
    db_conn = request.app['db_conn']
    data = await request.post()
    error = await validate_login(db_conn, data)
    if error:
        return {'error': error}
    else:
        response = redirect(request.app.router, 'index')
        user, password_hash = await db.get_user_by_login(db_conn, data['login'])
        await remember(request, response, user)
        raise response


async def logout(request):
    response = redirect(request.app.router, 'index')
    await forget(request, response)
    return response


async def validate_login(conn, form):
    username = form['login']
    password = form['password']
    if not username:
        return 'username is required'
    if not password:
        return 'password is required'
    row = await db.get_user_by_login(conn, username)
    if not row:
        return 'Invalid username'
    user, password_hash = row
    if not await utils.check_password_hash(password, password_hash):
        return 'Invalid password'
    else:
        return None
    return 'error'

