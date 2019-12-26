from django.core.management.base import BaseCommand

import tqdm

from dash_pictures.tasks.pinterest_tasks import (
    get_pinterest,
)
from dash_pictures.models import (
    PinterestUser,
)


class Command(BaseCommand):
    help = 'Update users boards and pins'

    def handle(self, *args, **options):
        for user in tqdm.tqdm(PinterestUser.objects.all()):
            get_pinterest(user.user_id, user.access_token)
