from django.shortcuts import render

# Create your views here.


def projectA(request):
    return render(request, 'projectA.html')


def test_graph(request):
    return render(request, 'temp.html')
