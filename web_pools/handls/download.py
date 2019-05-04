import aiohttp_jinja2
from aiohttp import web
from urllib.parse import urlunparse
from web_pools.modules import db
from web_pools.modules import utils


@aiohttp_jinja2.template('download.html')
async def index(request):
    db_conn = request.app['db_conn']
    config = request.app["config"]
    scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
    hashname = request.match_info.get('HASHNAME', None)
    row = await db.select_file(db_conn, path=hashname)
    if row:
        id, name, size, path, expiry, insert_dt  = row
        expiry = await utils.get_time(expiry)
        size =  await utils.get_size(size)
        download_link = urlunparse((scheme, config.project_domain, f'/files/{hashname}/{name}', '', '', ''))
        return dict(title=config.project_name, filename=name, size=size, expiry = expiry,  download_link=download_link)
    else:
        raise web.HTTPNotFound()