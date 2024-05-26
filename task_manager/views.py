from django.shortcuts import render
from django.views import generic

from task_manager.models import Task, Worker


def index(request):
    workers = Worker.objects.all().count()
    tasks = Task.objects.all().count()
    context = {
        'workers': workers,
        'tasks': tasks
    }
    return render(request, "task_manager/index.html", context=context)


class TaskListView(generic.ListView):
    model = Task
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"


class WorkerListView(generic.ListView):
    model = Worker
    template_name = "task_manager/worker_list.html"
    context_object_name = "worker_list"
