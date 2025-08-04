from django.shortcuts import render


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    return render(request, "errors/404.html", status=404)


def privacy_policy(request):
    """ A view to return the privacy policy page """

    return render(request, 'privacy-policy/privacy-policy.html')
