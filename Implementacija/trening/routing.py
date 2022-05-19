from django.urls import re_path
from . import consumers


websocket_urlpatterns=[
    re_path(r'ws/socket-server/(?P<trening_id>\w+)/$',consumers.treningConsumer.as_asgi())
]