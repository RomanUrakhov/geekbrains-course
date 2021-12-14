from flex_framework.request import BaseRequest


class Flex:
    def __init__(self, routes, middlewares=None):
        self._routes = routes
        self._middlewares = middlewares

    def __call__(self, environ, start_response):
        request = BaseRequest(environ)

        for middleware in self._middlewares:
            middleware(request)

        route = self._routes.get(request.url, handle_error)

        status_code, body = route(request)

        start_response(status_code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


def trailing_slash_middleware(request: BaseRequest):
    """
    Опциональный Middleware, добавляющий в конец URL слеш
    """
    raw_url = request.url
    if not raw_url.endswith('/'):
        request.url = f'{raw_url}/'
    return request


def handle_error(request):
    """
    Роут по-умолчанию, если не нашли совпадения по URL в self._routes
    """
    return '404 NOT FOUND', 'Page not found'
