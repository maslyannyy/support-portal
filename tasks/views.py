from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pydantic import BaseModel

from helpers.decorators import staff_or_404
from tasks.management.commands import feed_checker
from tasks.services import tasks


class SwitchTaskRequest(BaseModel):
    id: int


class SwitchTaskResponse(BaseModel):
    id: int
    is_active: bool
    success: bool


@staff_or_404
@require_http_methods("GET")
def tasks_panel(request):
    all_tasks = tasks.get_all_tasks()
    return render(request, 'panel.html', {'all_tasks': all_tasks})


@staff_or_404
@csrf_exempt
@require_http_methods("PUT")
def switch_task(request):
    task = SwitchTaskRequest.parse_raw(request.read().decode())

    if not task.id:
        return JsonResponse({'success': False})

    task_id, task_status = tasks.switch_task(task.id)
    response = SwitchTaskResponse(id=task_id, is_active=task_status, success=True)

    return JsonResponse(response.dict())


@staff_or_404
@csrf_exempt
@require_http_methods("POST")
def sync_tasks(request):
    tasks.sync_tasks()
    return JsonResponse({'success': True})


@staff_or_404
@csrf_exempt
@require_http_methods("POST")
def check_all_feeds(request):
    feed_checker.check_feeds()
    return JsonResponse({'success': True})
