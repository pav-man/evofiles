import os
import shutil
from aiohttp import web
from web_pools.modules import db

@web.middleware
async def files_deleter(request, handler):
    db_conn = request.app['db_conn']
    config = request.app["config"]
    rows = await db.select_expire_files(db_conn)
    if rows:
        for row in rows:
            id, filename, hash_dir = row
            path = os.path.join(config.project_files, hash_dir)
            shutil.rmtree(path, ignore_errors=True)
        await db.delete_expire_files(db_conn, ",".join((str(r[0]) for r in rows)))

    response = await handler(request)
    return response