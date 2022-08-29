# receive/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.enter, name='enter'),
    path('<str:room_name>/<str:user_name>/', views.file_room),
    

]