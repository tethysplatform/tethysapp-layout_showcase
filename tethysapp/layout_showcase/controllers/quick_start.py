from django.shortcuts import render


def quick_start(request):
    context = {}
    return render(request, 'layout_showcase/quick_start.html', context)
