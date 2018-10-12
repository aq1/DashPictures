from django.shortcuts import render


def index_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'pinterest'):
        request.session['pins_history'] = []
        return render(
            request,
            'pinterest_drawing_practice/app.html',
        )

    return render(request, 'pinterest_drawing_practice/index.html')
