from django.shortcuts import render
from django.http import JsonResponse

from core.tasks import debug_task

# Create your views here.

def hello_world(request):
    response = JsonResponse({'message': 'Hello World!'})
    return response


def home(request):
    response = JsonResponse({'message':'Home Page'})
    return response


def debug_task_view(request):
    debug_task.delay()
    return JsonResponse({'message': 'Task sent to queue.'})
