import aiohttp_jinja2
from aiohttp import web
from urllib import parse
from web_pools.modules import db
from web_pools.modules import utils

@aiohttp_jinja2.template('search.html')
async def index(request):
    db_conn = request.app['db_conn']
    config = request.app["config"]
    return dict(title=config.project_name)

@aiohttp_jinja2.template('search.html')
async def file(request):
    db_conn = request.app['db_conn']
    config = request.app["config"]
    scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
    filename = request.match_info['FILENAME']
    rows = []
    if filename:
        result = await db.select_files(db_conn, filename)
        for row in result:
            id, name, size, path, expiry, insert_dt  = row
            expiry = await utils.get_time(expiry)
            size =  await utils.get_size(size)
            download_link = parse.urlunparse((scheme, config.project_domain, f'/{path}', '', '', ''))
            rows.append((expiry, size, download_link))
    return dict(title=config.project_name, filename=filename, rows=rows)


async def search(request):
    data = await request.post()
    filename = data["filename"]
    redirect_url = "/search/" + parse.quote(filename, safe='') + '/'
    raise web.HTTPFound(redirect_url)
