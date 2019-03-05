from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def hello_world(request):
    response = JsonResponse({'message': 'Hello World!'})
    return response


def home(request):
    response = JsonResponse({'message':'Home Page'})
    return response
