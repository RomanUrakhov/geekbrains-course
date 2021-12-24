from flex_framework.core import Flex
from app.middlewares import middlewares

app = Flex(middlewares=middlewares)

from app import views
