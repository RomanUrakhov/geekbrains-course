from flex_framework.core import trailing_slash_middleware
from flex_framework.request import BaseRequest

import config


def token_auth_middleware(request: BaseRequest):
    if request.args.get('token') and request.args.get('token') == config.secret_token:
        request.set_header('Custom-Authorized', True)
    else:
        request.set_header('Custom-Authorized', False)
    return request


middlewares = [token_auth_middleware, trailing_slash_middleware]
