from fastapi import Request

from .config import cfg
from .errors import HTTPabort


class CurrentUser:
    is_auth = False

    def __init__(self, auth_headers=None):
        if auth_headers:
            self.is_auth = True
            for attr, data in auth_headers:
                setattr(self, attr, data)


async def get_current_user(request: Request):
    auth_headers = []
    for attr, header in cfg.AUTH_HEADERS.items():
        try:
            data = request.headers[f'{cfg.AUTH_HEADER_PREFIX}_{header}']
        except KeyError:
            return CurrentUser()
        if attr == 'account_id':
            try:
                data = int(data)
            except ValueError:
                return CurrentUser()
        if not data:
            return CurrentUser()
        auth_headers.append((attr, data))

    return CurrentUser(auth_headers)


async def auth_required(request: Request):
    current_user = await get_current_user(request)
    if not current_user.is_auth:
        HTTPabort(401, 'Missing auth HEADER(S)')
    return current_user


async def auth_forbidden(request: Request):
    current_user = await get_current_user(request)
    if current_user.is_auth:
        HTTPabort(409, 'User must be unauthorized')
