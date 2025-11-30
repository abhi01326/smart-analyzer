from django.urls import path
from .views import (
    create_task, list_tasks, get_task,
    update_task, delete_task,
    analyze_tasks, suggest_tasks
)

urlpatterns = [
    path('create/', create_task),
    path('list/', list_tasks),
    path('<int:task_id>/', get_task),
    path('<int:task_id>/update/', update_task),
    path('<int:task_id>/delete/', delete_task),
    path('analyze/', analyze_tasks),
    path('suggest/', suggest_tasks),
]
