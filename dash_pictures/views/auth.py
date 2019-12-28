from urllib.parse import urlencode

from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods

import requests

from dash_pictures.models import PinterestUser
from dash_pictures.views import index_view
from dash_pictures.tasks import pinterest_tasks
from dash_pictures.models import Board


def oauth_view(request):
    try:
        code, state = request.GET['code'], request.GET['state']
    except KeyError:
        return HttpResponse('Bad parameters', status=400)

    if state != 'state':
        return HttpResponse('Bad parameters', status=400)

    response = requests.post(
        'https://api.pinterest.com/v1/oauth/token',
        data={
            'grant_type': 'authorization_code',
            'client_id': settings.PINTEREST_APP_ID,
            'client_secret': settings.PINTEREST_APP_SECRET,
            'code': code,
        }
    )

    if response.status_code != 200:
        return JsonResponse(response.json(), status=400)

    access_token = response.json()['access_token']
    response = requests.get(
        'https://api.pinterest.com/v1/me',
        params={'access_token': access_token},
    )

    if response.status_code != 200:
        return JsonResponse(response.json(), status=400)

    data = response.json()['data']
    pinterest_user, _ = PinterestUser.create_or_update(
        pinterest_id=data['id'],
        access_token=access_token,
        first_name=data['first_name'],
        last_name=data['last_name'],
    )

    user = authenticate(request, username=data['id'], password=access_token)
    if user is not None:
        login(request, user)
    else:
        return JsonResponse({'error': 'Could not log in'}, status=400)

    if not Board.objects.filter(user_id=user.id).exists():
        request.session['get_boards_task_id'] = pinterest_tasks.get_pinterest.delay(request.user.id, access_token)

    return redirect(index_view)


@require_http_methods(['POST'])
def login_view(request):
    params = {
        'response_type': 'code',
        'client_id': '4993212126788084668',
        'state': 'state',
        'scope': 'read_public',
        'redirect_uri': settings.PINTEREST_REDIRECT_URL,
    }
    url = 'https://api.pinterest.com/oauth?{}'.format(urlencode(params))
    return redirect(url)
