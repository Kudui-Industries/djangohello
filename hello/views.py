from django.http import HttpResponse
from django.shortcuts import render


def hello_world(request):
    return HttpResponse("<h1>Hello, World! :test1 </h1>")