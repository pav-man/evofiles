#!/home/python/evo_files/venv/bin/python3.6
import argparse
import aiohttp_jinja2
import jinja2
import logging.config
import os
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import authorized_userid
from aiohttp_security import setup as setup_security
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_session import session_middleware
from web_pools.handls import *
from web_pools.modules.db_auth import DBAuthorizationPolicy
from web_pools.modules.db import init_db, close_db
from web_pools.modules import config
from web_pools.modules.deleter import files_deleter

logging.config.dictConfig(config.LOGGING)
logs = logging.getLogger("aioserver")

async def current_user_ctx_processor(request):
    userid = await authorized_userid(request)
    is_anonymous = not bool(userid)
    return {'current_user': {'is_anonymous': is_anonymous, 'userid': userid}}

async def init_app():
    middleware = session_middleware(EncryptedCookieStorage(config.cookie_secret))
    app = web.Application(middlewares=[middleware, files_deleter])
    app['config'] = config
    app.router.add_get('/', index.index, name='index')
    app.router.add_post('/', upload.upload)
    app.router.add_get('/search/', search.index)
    app.router.add_get('/search/{FILENAME:.*}/', search.file)
    app.router.add_post('/search/', search.search)
    app.router.add_get('/{HASHNAME:\w+}', download.index)
    app.router.add_get('/login/', login.get, name='login')
    app.router.add_post('/login/', login.post)
    app.router.add_get('/logout/', login.logout)
    app.router.add_get('/signup/', signup.get)
    app.router.add_post('/signup/', signup.post)
    app.router.add_get('/my_files/', my_files.get)
    templates =  os.path.join(config.project_root,'web_pools','templates')
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(templates),
                         autoescape=jinja2.select_autoescape(['html', 'xml']),
                         context_processors=[current_user_ctx_processor]
                         )
    db_conn = await init_db(app)
    # app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    setup_security(app,
                   SessionIdentityPolicy(),
                   DBAuthorizationPolicy(db_conn)
                   )
    return app


def main(path):
    app = init_app()
    web.run_app(app, path=path)

if __name__ == '__main__':
    #sypervisor start num process
    parser = argparse.ArgumentParser(description="evofiles aioserver")
    parser.add_argument('--path')
    args = parser.parse_args()
    path = args.path
    # path = "/tmp/evo_files_0.sock"
    main(path=path)

