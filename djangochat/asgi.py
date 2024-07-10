# Run redis server:  docker run --rm -p 6379:6379 redis:7

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangochat.settings')

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from channels.routing import ProtocolTypeRouter, URLRouter
import room.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(room.routing.websocket_urlpatterns))
        )
})
