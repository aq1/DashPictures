from django.contrib import admin

from dash_pictures.models import (
    PinterestUser,
    Board,
    Pin,
)


@admin.register(PinterestUser)
class PinterestUserAdmin(admin.ModelAdmin):

    list_display = '__str__', 'pinterest_id', 'access_token'


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):

    list_display = '__str__', 'user'


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):

    list_display = '__str__', 'board', 'color'
