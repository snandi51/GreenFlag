from django.shortcuts import render
import django

# Create your views here.


def projectA(request):
    return render(request, 'projectA.html')


def test_graph(request):
    return render(request, 'temp.html')


def error_400(request, exception):
    return render(request, '400.html')


def error_403(request, exception):
    return render(request, '403.html')


def error_404(request, exception):
    return render(request, '404.html')


def error_500(request):
    return render(request, '500.html')


