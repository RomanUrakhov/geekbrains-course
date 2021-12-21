from flex_framework.core import trailing_slash_middleware
from flex_framework.request import BaseRequest

import config
from routes import all_courses, advanced_courses, index, feedback, articles, tags, add_material, copy_material, \
    material_list


def token_auth_middleware(request: BaseRequest):
    if request.args.get('token') and request.args.get('token') == config.secret_token:
        request.set_header('Custom-Authorized', True)
    else:
        request.set_header('Custom-Authorized', False)
    return request


middlewares = [token_auth_middleware, trailing_slash_middleware]

routes = {
    '/': index,
    '/courses/': all_courses,
    '/courses/all/': all_courses,
    '/courses/advanced/': advanced_courses,
    '/articles/': articles,
    '/feedback/': feedback,
    '/tags/': tags,
    '/add-material/': add_material,
    '/copy-material/': copy_material,
    '/materials/': material_list
}
