from django.urls import path

from task_manager import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
    path("tasks/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", views.DeleteTaskView.as_view(), name="task-delete"),
    path("task-type/create/", views.TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-type/<int:pk>/delete/", views.TaskTypeDeleteView.as_view(), name="task-type-delete"),
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", views.WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", views.WorkerUpdateView.as_view(), name="worker-update"),
    path("accounts/register/", views.WorkerRegisterView.as_view(), name="worker-register"),
    path("authorisation/", views.AuthorisationView.as_view(), name="authorisation"),
    path("streamline-workflow/", views.learn_more_1, name="streamline-workflow"),
]

app_name = "task_manager"
