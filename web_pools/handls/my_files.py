import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import authorized_userid
from urllib import parse
from web_pools.modules import db
from web_pools.modules import utils

def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)

@aiohttp_jinja2.template('my_files.html')
async def get(request):
    db_conn = request.app['db_conn']
    config = request.app["config"]
    scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
    username = await authorized_userid(request)
    if not username:
        raise redirect(request.app.router, 'login')
    rows = []
    result = await db.user_files(db_conn, username)
    for row in result:
        id, name, size, path, expiry, insert_dt  = row
        expiry = await utils.get_time(expiry)
        size =  await utils.get_size(size)
        download_link = parse.urlunparse((scheme, config.project_domain, f'/{path}', '', '', ''))
        rows.append((name, expiry, size, download_link))
    return dict(title=config.project_name, rows=rows)

