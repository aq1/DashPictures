from django.db import models
from django.contrib.auth.models import User


class BoardQuerySet(models.QuerySet):
    def filter_user_and_predefined(self, user):
        return self.filter(
            models.Q(user=user) |
            models.Q(predefined=True),
        )


class Board(models.Model):

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='boards',
    )
    predefined = models.BooleanField(
        default=False,
    )
    pinterest_id = models.CharField(
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
    )

    objects = BoardQuerySet.as_manager()

    def __str__(self):
        return self.name
