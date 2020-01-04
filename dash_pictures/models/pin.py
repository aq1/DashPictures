from django.db import models

from dash_pictures.models import Board


class PinQuerySet(models.QuerySet):
    def filter_user_and_predefined(self, user_id, boards):
        return self.filter(
            models.Q(board__user_id=user_id) | models.Q(board__predefined=True),
            board_id__in=boards,
        )


class Pin(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='pins',
    )
    pinterest_id = models.CharField(
        max_length=255,
        unique=True,
    )

    image_url = models.CharField(
        max_length=255,
    )
    color = models.CharField(
        max_length=255,
    )
    link = models.CharField(
        max_length=255,
    )

    objects = PinQuerySet.as_manager()

    def __str__(self):
        return self.pinterest_id
