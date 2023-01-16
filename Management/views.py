from django.shortcuts import render

# Create your views here.


def projectA(request):
    return render(request, 'projectA.html')
