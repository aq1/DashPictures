from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from dash_pictures.models import Board, Pin


@login_required(login_url='/')
def get_boards(request):

    boards = Board.objects.filter(user=request.user).values()

    return JsonResponse({'data': list(boards)})


def _get_random_pin(boards_ids, pins_history):
    return Pin.objects.filter(
        board_id__in=boards_ids,
    ).exclude(
        id__in=pins_history
    ).values().order_by('?').first()


@login_required(login_url='/')
def get_pin(request):
    pins_history = request.session.get('pins_history', [])
    boards_ids = request.GET.getlist('boards_ids')
    pin = _get_random_pin(boards_ids, pins_history)

    if not pin:
        pins_history = []
        pin = _get_random_pin(boards_ids, pins_history)
        if not pin:
            return JsonResponse({'status': 'No pin found'}, status=400)

    pins_history.append(pin['id'])
    request.session['pins_history'] = pins_history

    return JsonResponse(pin)
