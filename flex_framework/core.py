from abc import ABC, abstractmethod

from flex_framework.request import BaseRequest


class WSGIApplication(ABC):
    @abstractmethod
    def __call__(self, environ, start_response):
        raise NotImplementedError

    @abstractmethod
    def add_url_rule(self, rule, func):
        raise NotImplementedError

    @abstractmethod
    def route(self, rule):
        raise NotImplementedError


class Flex:
    def __init__(self, middlewares=None):
        self._routes = {}
        self._middlewares = middlewares or []

    def __call__(self, environ, start_response):
        request = BaseRequest(environ)

        for middleware in self._middlewares:
            middleware(request)

        route = self._routes.get(request.url, handle_error)

        status_code, body = route(request)

        start_response(status_code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    def add_url_rule(self, rule, func):
        self._routes[rule] = func

    def route(self, rule):
        def decorator(view_func):
            self.add_url_rule(rule, view_func)
            return view_func

        return decorator


"""
Реализация Logging-Proxy и Fake-Proxy
"""


# TODO: Не могу понять, почему падает, когда вместо Flex юзаю этот класс
class FlexWithLogs(WSGIApplication):
    def __init__(self, middlewares):
        self.source_app = Flex(middlewares=middlewares)

    def __call__(self, environ, start_response):
        request = BaseRequest(environ)
        method_info = f'request method - {request.method}'
        args_info = f'request args - {request.args}'
        data_info = f'request form data - {request.get_form_data()}'
        print(f'[WSGI LOGGER]: {method_info}; {args_info}; {data_info}')
        self.source_app(environ, start_response)

    def add_url_rule(self, rule, func):
        self.source_app.add_url_rule(rule, func)

    def route(self, rule):
        self.source_app.route(rule)


# TODO: TBD
class FlexFake:
    pass


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
