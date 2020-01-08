from django.contrib import admin

from dash_pictures.models import (
    PinterestUser,
    Board,
    Pin,
)


class PinInline(admin.StackedInline):
    model = Pin
    extra = 0


@admin.register(PinterestUser)
class PinterestUserAdmin(admin.ModelAdmin):
    list_display = '__str__', 'pinterest_id',


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = '__str__', 'user', 'predefined'
    inlines = [PinInline]


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = '__str__', 'board', 'color'
