from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from dash_pictures.tasks.pinterest_tasks import background_task


@user_passes_test(lambda u: u.is_superuser)
def background_task_view(request):
    tasks = sorted(
        [{
            'id': task_id,
            'updated': task['updated'],
            'status': task['status'],
            'result': task['result'],
            'name': task['name'],
        } for task_id, task in background_task.tasks.items()],
        key=lambda i: i['updated'],
        reverse=True,
    )
    return render(
        request,
        'dash_pictures/background_task.html', {
            'tasks': tasks,
        },
    )
