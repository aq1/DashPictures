import time

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from dash_pictures.models import Board, Pin
from dash_pictures.tasks.pinterest_tasks import background_task


@login_required(login_url='/')
def get_boards(request):
    if request.session.get('get_boards_task_id') and background_task.tasks.get(request.session['get_boards_task_id']):
        # this is fine
        while True:
            task = background_task.tasks[request.session['get_boards_task_id']]
            if task['status'] == background_task.STARTED:
                time.sleep(1)
                continue
            if task['status'] == background_task.ERROR:
                return JsonResponse({'data': []})
            break

    boards = Board.objects.filter_user_and_predefined(request.user.id).values()

    return JsonResponse({'data': list(boards)})


def _get_random_pin(user_id, boards, pins_history):
    return Pin.objects.filter_user_and_predefined(
        user_id,
        boards,
    ).exclude(
        id__in=pins_history
    ).values().order_by('?').first()


@login_required(login_url='/')
def get_pin(request):
    pins_history = request.session.get('pins_history', [])
    boards = request.GET.getlist('boards[]')
    pin = _get_random_pin(request.user.id, boards, pins_history)

    if not pin:
        pins_history = []
        pin = _get_random_pin(request.user.id, boards, pins_history)
        if not pin:
            return JsonResponse(
                {'status': 'No pin found'}, status=400)

    pins_history.append(pin['id'])
    request.session['pins_history'] = pins_history

    return JsonResponse(pin)
