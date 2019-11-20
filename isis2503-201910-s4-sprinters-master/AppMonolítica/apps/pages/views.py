from django.shortcuts import render
from django.http import HttpResponse
from ..login.views import getRole


# Create your views here.
def home_view(request):
    user = request.user
    if user.is_authenticated:
        context = {
            'role': getRole(request),
        }
    else:
        context = {}

    return render(request, 'pages/home_view.html', context)


def ping(request):
    return HttpResponse('True')
