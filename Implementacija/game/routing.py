from django.urls import re_path
from . import consumers


websocket_urlpatterns=[
    re_path(r'ws/socket-server/game/(?P<game_id>\w+)/$',consumers.gameConsumer.as_asgi())
]