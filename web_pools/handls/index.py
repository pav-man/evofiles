import aiohttp_jinja2
from aiohttp_security import is_anonymous
from aiohttp_session import get_session


@aiohttp_jinja2.template('index.html')
async def index(request):
    config = request.app["config"]
    # is_logged = not await is_anonymous(request)
    return dict(title=config.project_name)


