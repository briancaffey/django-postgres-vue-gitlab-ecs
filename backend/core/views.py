import os

from django.http import JsonResponse

from core.tasks import debug_task


def hello_world(request):
    response = JsonResponse(
        {
            'message': 'Hello, World!',
            'git_sha': os.environ.get('GIT_SHA', '<git sha>')
        }
    )
    return response


def home(request):
    response = JsonResponse({'message': 'Root'})
    return response


def debug_task_view(request):
    debug_task.delay()
    return JsonResponse({'message': 'Task sent to queue.'})


def verify_domain(request):
    valid_subdomains = ['test', 'sub', 'localhost']
    subdomain = request.META['HTTP_HOST'].split('.')[0]
    if subdomain in valid_subdomains:
        return JsonResponse(
            {
                "message": "OK",
                "subdomain": subdomain,
            },
            status=200
        )
    else:
        return JsonResponse(
            {
                "message": "Subdomain does not exist"
            },
            status=404
        )
