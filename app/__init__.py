from app.patterns.behavioral import FileLogger
from app.patterns.creational import FlexLogger
from flex_framework.core import WSGIApplicationFactory
from app.middlewares import middlewares
from config import wsgi_app_type

app = WSGIApplicationFactory.create_app(app_type=wsgi_app_type, middlewares=middlewares)
logger = FlexLogger(logging_strategy=FileLogger())

from app import views
