from abc import ABC, abstractmethod

from flex_framework.request import BaseRequest


class WSGIApplication(ABC):
    @abstractmethod
    def __call__(self, environ, start_response, request=None):
        raise NotImplementedError

    @abstractmethod
    def add_url_rule(self, rule, func):
        raise NotImplementedError

    @abstractmethod
    def route(self, rule):
        raise NotImplementedError


class Flex(WSGIApplication):
    def __init__(self, middlewares=None):
        self._routes = {}
        self._middlewares = middlewares or []

    def __call__(self, environ, start_response, request=None):
        if not request:
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
Реализация Logging WSGI Application
"""


class FlexWithLogs(Flex):
    @staticmethod
    def _additional_logging(request: BaseRequest):
        method_info = f'request method - {request.method}'
        args_info = f'request args - {request.args}'
        data_info = f'request form data - {request.get_form_data()}'
        print(f'[WSGI LOGGER]: {method_info}; {args_info}; {data_info}')

    def __call__(self, environ, start_response, request=None):
        request = BaseRequest(environ)
        self._additional_logging(request)
        return super(FlexWithLogs, self).__call__(environ, start_response, request=request)


"""
Реализация Fake WSGI Application (пример прокси)
"""


class FlexFake(WSGIApplication):
    def __init__(self, middlewares):
        self.source_app = Flex(middlewares)

    def __call__(self, environ, start_response, request=None):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return ['Hello from fake'.encode('utf-8')]

    def add_url_rule(self, rule, func):
        self.source_app(rule, func)

    def route(self, rule):
        return self.source_app.route(rule)


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


class WSGIApplicationFactory:
    app_types = {
        'default': Flex,
        'with_logs': FlexWithLogs,
        'fake': FlexFake
    }

    @classmethod
    def create_app(cls, app_type, middlewares):
        return cls.app_types.get(app_type, Flex)(middlewares)
