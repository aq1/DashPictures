import uuid
import datetime
import threading

import requests

from django.db import transaction


class BackgroundTask:
    """
    I got tired of Celery.
    """

    tasks = {}

    STARTED = 'STARTED'
    DONE = 'DONE'
    ERROR = 'ERROR'

    def __init__(self, task):
        self.task = task

    def __call__(self, *args, **kwargs):
        return self.task(*args, **kwargs)

    def update_task(self, task_id, status, result):
        self.tasks[task_id] = {
            'name': self.task.__name__,
            'updated': datetime.datetime.now(),
            'status': status,
            'result': result,
        }

    def thread_task(self, task_id, *args, **kwargs):
        self.update_task(task_id, self.STARTED, None)
        try:
            result = self.task(*args, **kwargs)
        except Exception as e:
            self.update_task(task_id, self.ERROR, e)
        else:
            self.update_task(task_id, self.DONE, result)

    def delay(self, *args, **kwargs):
        task_id = str(uuid.uuid4())
        thread = threading.Thread(
            target=self.thread_task,
            args=[task_id] + list(args),
            kwargs=kwargs,
        )
        thread.start()
        return task_id


background_task = BackgroundTask


@background_task
def test(user):
    import time
    time.sleep(5)
    return user.username


@background_task
def get_pins(user_id, access_token):
    from dash_pictures.models import Board, Pin

    pins = {}
    existing_pins = {p.pinterest_id for p in Pin.objects.filter(board__user_id=user_id).only('pinterest_id')}
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
                'fields': 'id,board(id),image,link,color',
                'limit': 100
            })

        if response.status_code != 200:
            raise requests.HTTPError(response.text)

        response = response.json()

        for pin in response['data']:
            pins[pin['id']] = Pin(
                pinterest_id=pin['id'],
                board_id=boards[pin['board']['id']],
                image_url=pin['image']['original']['url'],
                link=pin['link'],
                color=pin['color'],
            )

        cursor = response.get('page', {}).get('cursor')
        if not cursor:
            break

    to_delete = existing_pins - pins.keys()
    to_create = filter(lambda p: p['id'] not in existing_pins, pins)
    with transaction.atomic():
        Pin.objects.filter(pinterest_id__in=to_delete).delete()
        Pin.objects.bulk_create(to_create, batch_size=1000)


@background_task
def get_boards(user_id, access_token):
    from dash_pictures.models import Board

    response = requests.get(
        'https://api.pinterest.com/v1/me/boards/',
        params={
            'access_token': access_token,
            'fields': 'id,name',
            'limit': 100,
        }
    )

    if response.status_code != 200:
        raise requests.HTTPError(response.text)

    existing_boards = {b.pinterest_id for b in Board.objects.filter(user_id=user_id).only('pinterest_id').all()}
    boards = {
        board['id']: Board(
            user_id=user_id,
            pinterest_id=board['id'],
            name=board['name'],
        )
        for board in response.json()['data']
    }

    to_delete = existing_boards - boards.keys()
    to_create = filter(lambda b: b.pinterest_id not in existing_boards, boards.values())
    with transaction.atomic():
        Board.objects.filter(pinterest_id__in=to_delete).update(deleted=True)
        Board.objects.bulk_create(to_create)


@background_task
def get_pinterest(user_id, access_token):
    get_boards(user_id, access_token)
    get_pins(user_id, access_token)
