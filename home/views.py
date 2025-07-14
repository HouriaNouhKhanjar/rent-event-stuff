from django.shortcuts import render


def index(request):
    """ A view to return the Home page """

    context = {
        'search_term': ''
    }
    return render(request, 'home/index.html', context)
