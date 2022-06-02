from django.urls import re_path

from core.consumers import ExposeConsumer

websocket_urlpatterns = [
    re_path(r'ws/expose/(?P<user_id>user_\d+)/$', ExposeConsumer.as_asgi()),
]