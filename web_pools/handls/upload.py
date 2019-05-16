import os
import time
import aiohttp_jinja2
import aiofiles
from aiohttp import web
from aiohttp_security import authorized_userid
from urllib.parse import urlunparse
from web_pools.modules import db
from web_pools.modules import utils

@aiohttp_jinja2.template('upload_post.html')
async def upload(request):
    db_conn = request.app['db_conn']
    config = request.app["config"]
    scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
    username = await authorized_userid(request)
    reader = await request.multipart()
    field = await reader.next()
    assert field.name == 'file'
    filename = field.filename
    if not filename:
        return dict(error='not select file')
    size = 0
    hash_dir = await utils.hash_path(str(time.time()))
    if not os.path.exists(os.path.join(config.project_files, hash_dir)):
        os.makedirs(os.path.join(config.project_files, hash_dir))
    async with aiofiles.open(os.path.join(config.project_files, hash_dir, filename), 'wb') as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            await f.write(chunk)
        await f.flush()

    field = await reader.next()
    assert field.name == 'expiry'
    expiry = await field.text()
    error = await validate_expiry(config, expiry)
    if error:
        expiry = config.default_expiry
    file_id = await db.insert_file(db_conn, filename, size, hash_dir, expiry)
    url = urlunparse((scheme,config.project_domain, f'/{hash_dir}','','',''))
    if username:
        await db.add_file_to_user(db_conn, username, file_id)
    return dict(filename=filename, size=size, expiry=expiry, url=url)


async def validate_expiry(config, expiry):
    if not expiry:
        return 'Not set expiry time'
    elif not expiry.isdigit():
        return 'Not digit'
    elif int(expiry) > config.max_expiry:
        return 'expiry time not correct'
