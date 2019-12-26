from django.contrib import admin
from django.urls import path

from dash_pictures.views import (

    index_view,
    oauth_view,
    login_view,
    get_boards,
    get_pin,
    background_task_view,
)

urlpatterns = [
    path('a/', admin.site.urls),
    path('tasks/', background_task_view),
    path('oauth/', oauth_view),
    path('login/', login_view),
    path('api/get_boards/', get_boards),
    path('api/get_pin/', get_pin),
    path('', index_view),
]
