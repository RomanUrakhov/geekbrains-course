from flex_framework.core import trailing_slash_middleware

import config
from routes import extra_materials, all_courses, advanced_courses, index, my_favourites


def token_auth_middleware(request):
    if request['args'].get('token') and request['args'].get('token') == config.secret_token:
        request['authorized'] = True
    else:
        request['authorized'] = False
    return request


middlewares = [token_auth_middleware, trailing_slash_middleware]

routes = {
    '/': index,
    '/courses/all/': all_courses,
    '/courses/advanced/': advanced_courses,
    '/my-favourites/': my_favourites,
    '/extra_materials/': extra_materials
}
