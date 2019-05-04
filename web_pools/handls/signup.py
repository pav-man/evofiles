import aiohttp_jinja2
from aiohttp import web
from web_pools.modules import db
from web_pools.modules import utils


@aiohttp_jinja2.template('signup.html')
async def get(request):
    db_conn = request.app['db_conn']
    config = request.app["config"]
    return dict(title=config.project_name)

@aiohttp_jinja2.template('signup.html')
async def post(request):
    db_conn = request.app['db_conn']
    data = await request.post()
    login = data["login"]
    password = data["password"]
    password_hash = await utils.generate_password_hash(password)
    res = await db.add_user(db_conn, login, password_hash)
    if res:
        return {'result' : f'Successfully signup.'}
    else:
        return {'error': f"login '{login}' exists, select another."}


