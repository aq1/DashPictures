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

    def add_arguments(self, parser):
        parser.add_argument(
            'user',
            nargs='?',
            help='User Id',
        )

    def handle(self, *args, **options):
        users = PinterestUser.objects.all()
        if options['user']:
            users = users.filter(user_id=options['user'])

        for user in tqdm.tqdm(users):
            get_pinterest(user.user_id, user.access_token)
