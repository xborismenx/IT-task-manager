from django.shortcuts import render

from task_manager.models import Task, Worker


def index(request):
    workers = Worker.objects.all().count()
    tasks = Task.objects.all().count()
    context = {
        'workers': workers,
        'tasks': tasks
    }
    return render(request, "task_manager/index.html", context=context)
