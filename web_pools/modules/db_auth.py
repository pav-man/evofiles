from aiohttp_security.abc import AbstractAuthorizationPolicy
from web_pools.modules import db

class DBAuthorizationPolicy(AbstractAuthorizationPolicy):

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def authorized_userid(self, identity):
        row = await db.get_user_by_login(self.db_pool, identity)
        if row:
            return identity
        return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        return True