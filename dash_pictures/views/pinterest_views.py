from django.http import JsonResponse
from django.db import models
from django.contrib.auth.decorators import login_required

from dash_pictures.models import Board, Pin


@login_required(login_url='/')
def get_boards(request):
    boards = Board.objects.filter_user_and_predefined(request.user).values()

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
            return JsonResponse({'status': 'No pin found'}, status=400)

    pins_history.append(pin['id'])
    request.session['pins_history'] = pins_history

    return JsonResponse(pin)
