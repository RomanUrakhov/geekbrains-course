from urllib.parse import parse_qs


class Flex:
    def __init__(self, routes, middlewares=None):
        self._routes = routes
        self._middlewares = [default_argparse_middleware]
        middlewares and self._middlewares.extend(middlewares)  # extend if not empty

    def __call__(self, environ, start_response):
        request = {'url': environ['PATH_INFO'], 'args': environ['QUERY_STRING']}
        for middleware in self._middlewares:
            middleware(request)

        route = self._routes.get(request['url'], handle_error)

        status_code, body = route(request)

        start_response(status_code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


def default_argparse_middleware(request):
    """
    Предопределенный Middleware, парсящий строку аргументов запроса
    """
    raw_arguments = request['args']
    request['args'] = {}
    parsed_qs = parse_qs(raw_arguments)
    for key, value in parsed_qs.items():
        request['args'][key] = value[0]
    return request


def trailing_slash_middleware(request):
    """
    Опциональный Middleware, добавляющий в конец URL слеш
    """
    raw_url = request['url']
    if not raw_url.endswith('/'):
        request['url'] = f'{raw_url}/'
    return request


def handle_error(request):
    """
    Роут по-умолчанию, если не нашли совпадения по URL в self._routes
    """
    return '404 NOT FOUND', 'Page not found'
