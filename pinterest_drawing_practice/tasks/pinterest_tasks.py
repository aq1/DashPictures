import os

import requests

from celery import Celery, shared_task


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
app = Celery('pinterest')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@shared_task()
def get_pins(user_id, access_token):
    from pinterest_drawing_practice.models import Board, Pin

    pins = []
    pins_ids = set()
    boards = {
        board.pinterest_id: board.id
        for board in Board.objects.filter(user_id=user_id)
    }

    cursor = None
    while True:
        response = requests.get(
            'https://api.pinterest.com/v1/me/pins/',
            params={
                'cursor': cursor,
                'access_token': access_token,
                'fields': 'id,board(id),image,color',
                'limit': 100
            })

        if response.status_code != 200:
            return

        response = response.json()

        for pin in response['data']:
            if Pin.objects.filter(pinterest_id=pin['id']).exists() or pin['id'] in pins_ids:
                continue

            pins_ids.add(pin['id'])

            pins.append(
                Pin(
                    pinterest_id=pin['id'],
                    board_id=boards[pin['board']['id']],
                    image_url=pin['image']['original']['url'],
                    color=pin['color'],
                )
            )

        cursor = response.get('page', {}).get('cursor')
        if not cursor:
            break

    Pin.objects.bulk_create(pins)


@shared_task()
def get_boards(user_id, access_token):
    from pinterest_drawing_practice.models import Board

    r = requests.get(
        'https://api.pinterest.com/v1/me/boards/',
        params={
            'access_token': access_token,
            'fields': 'id,name',
            'limit': 100,
        }
    )

    if r.status_code != 200:
        return

    boards = []
    for board in r.json()['data']:
        if Board.objects.filter(pinterest_id=board['id']).exists():
            continue

        boards.append(Board(
            user_id=user_id,
            pinterest_id=board['id'],
            name=board['name'],
        ))

    Board.objects.bulk_create(boards)
    get_pins.delay(user_id, access_token)
