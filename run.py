from wsgiref.simple_server import make_server
from flex_framework.core import Flex

from urls import routes, middlewares


app = Flex(routes=routes, middlewares=middlewares)

if __name__ == '__main__':
    with make_server('', 8080, app) as httpd:
        sa = httpd.socket.getsockname()
        print(f"Running at: http://{sa[0]}:{sa[1]}")
        httpd.serve_forever()
