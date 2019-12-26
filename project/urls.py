from django.contrib import admin
from django.urls import path, include

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
    path('tasks/', background_task_view, name='task'),
    path('oauth/', oauth_view, name='oauth'),
    path('login/', login_view, name='login'),
    path('api/get_boards/', get_boards, name='get_boards'),
    path('api/get_pin/', get_pin, name='get_pin'),
    path('', index_view, name='index'),
]


urlpatterns = [
    path('dash_pictures/', include(urlpatterns)),
]
