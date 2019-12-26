import uuid
import datetime
import threading

import requests


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


@background_task
def get_boards(user_id, access_token):
    from dash_pictures.models import Board

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
