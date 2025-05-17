from django.http import HttpResponse
import os
from django.shortcuts import render

ENV = os.environ.get('env', 'dev')

def hello_world(request):
    return HttpResponse(f"<h1>Hello, World!</h1><p>Środowisko: {ENV}</p><p>test aplikacyji </p>")