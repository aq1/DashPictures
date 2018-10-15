from django.db import models

from dash_pictures.models import Board


class Pin(models.Model):

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='pins')
    pinterest_id = models.CharField(max_length=255, unique=True)

    image_url = models.CharField(max_length=255)
    color = models.CharField(max_length=255)

    def __str__(self):
        return self.pinterest_id
