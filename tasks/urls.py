from django.urls import path, include

from tasks.views import (
    tasks_panel,
    switch_task,
    sync_tasks,
    check_all_feeds,
)

tasks_url = [
    path('', tasks_panel),
    path('sync/', sync_tasks),
    path('switch/', switch_task),
]

urlpatterns = [
    path('tasks/', include(tasks_url)),
    path('feeds/check/', check_all_feeds),
]
