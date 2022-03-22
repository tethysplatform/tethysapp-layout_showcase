from django.shortcuts import render
from tethys_sdk.routing import controller


@controller
def quick_start(request):
    context = {}
    return render(request, 'layout_showcase/quick_start.html', context)
