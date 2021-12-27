from urllib.parse import parse_qs


class BaseRequest:
    def __init__(self, environ):
        self._env = environ
        self.url = self._env['PATH_INFO']
        self._cached_body = b''
        self._cached_form = {}
        self._headers = {}

    @property
    def method(self) -> str:
        return self._env['REQUEST_METHOD']

    @property
    def args(self) -> dict:
        raw_arguments = self._env['QUERY_STRING']
        return self._parse_query_string(raw_arguments)

    @property
    def headers(self):
        if self._headers:
            return self._headers
        all_headers = [h for h in self._env if h.startswith('HTTP_')]
        res = {}
        for header in all_headers:
            clear_name = header.replace('HTTP_', '')
            clear_name = clear_name.replace('_', '-')
            clear_name = clear_name.split('-')
            clear_name = map(str.capitalize, clear_name)
            clear_name = '-'.join(clear_name)
            res[clear_name] = self._env[header]
        self._headers = res
        return self._headers

    def body(self) -> bytes:
        if self._cached_body:
            return self._cached_body
        content_length_data = self._env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        body = self._env['wsgi.input'].read(content_length) if content_length > 0 else b''
        self._cached_body = body
        return body

    @staticmethod
    def _parse_query_string(data: str):
        res = {}
        if data:
            parsed_qs = parse_qs(data)
            for key, value in parsed_qs.items():
                res[key] = value[0] if len(value) == 1 else value
        return res

    def _parse_default_form(self, data: bytes):
        result = {}
        if data:
            decoded_data = data.decode('utf-8')
            result = self._parse_query_string(decoded_data)
        return result

    def get_form_data(self):
        if self._cached_form:
            return self._cached_form
        parsers = {
            'application/x-www-form-urlencoded': self._parse_default_form
        }
        content_type = self._env.get('CONTENT_TYPE', '').lower()
        parser_call = parsers.get(content_type)
        raw_data = self.body()
        if raw_data:
            form_data = parser_call(raw_data)
            self._cached_form = form_data
            return form_data
        return {}

    def set_header(self, name, value):
        self._headers[name] = value
