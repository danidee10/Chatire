import os

import django

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter

from notifications import consumers
from notifications import routing as notifications_routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatire.settings')
django.setup()

application = ProtocolTypeRouter({
  'http': AsgiHandler(),
  'websocket': URLRouter(notifications_routing.websocket_urlpatterns)
})
