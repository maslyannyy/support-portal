import os
from typing import Union, Tuple

from django.db import transaction

from tasks.models import Task
from tasks.services import crons

_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def sync_tasks():
    """Обновляет все кроны из базы в файл"""
    crons.clear_all_tasks()

    for cron_task in Task.objects.filter(is_active=True):
        crons.write_task(**cron_task.__dict__)


def get_all_tasks() -> list:
    """Возвращает все кроны из БД"""
    all_tasks = Task.objects.all().values('id', 'sleep', 'param', 'script', 'is_active')
    return list(all_tasks)


@transaction.atomic
def switch_task(task_id: Union[int, str]) -> Tuple[int, bool]:
    """Включает или выключает крон, зависит от текущего состояния"""
    cron_task = Task.objects.get(id=task_id)
    cron_task.is_active = not cron_task.is_active
    cron_task.save()
    return cron_task.id, cron_task.is_active
