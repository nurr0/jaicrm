from django.shortcuts import render
from django.template import RequestContext

#

def custom_handler404(request, exception):
    return render(request, 'core/error404.html', {'path': request.path}, status=404)

def custom_handler403(request, exception):
    return render(request, 'core/error403.html', {'path': request.path}, status=403)

def custom_handler500(request, *args, **kwargs):
    return render(request, 'core/error500.html', status=500)
