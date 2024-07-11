# Run redis server:  docker run --rm -p 6379:6379 redis:7

import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangochat.settings')

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from channels.routing import ProtocolTypeRouter, URLRouter
from room.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        )
})
