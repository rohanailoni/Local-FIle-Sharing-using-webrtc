from django.urls import re_path
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/chat/<str:room_name>/<str:user_name>/', consumers.ChatConsumer.as_asgi()),
]