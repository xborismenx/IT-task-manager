from django.urls import path

from task_manager import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),

]

app_name = "task_manager"
