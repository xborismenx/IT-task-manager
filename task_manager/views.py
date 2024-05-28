from django.shortcuts import render
from django.urls import reverse, reverse_lazy
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
    queryset = Task.objects.select_related('task_type').prefetch_related('assignees')
    paginate_by = 2
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"


class TaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/task_form.html"


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/task_form.html"


class DeleteTaskView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/task_confirm_delete.html"


class WorkerListView(generic.ListView):
    model = Worker
    template_name = "task_manager/worker_list.html"
    context_object_name = "worker_list"


class WorkerCreateView(generic.CreateView):
    model = Worker
    fields = "__all__"
    success_url = reverse_lazy("task_manager:worker-list")
    template_name = "task_manager/worker_form.html"


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    fields = "__all__"
    success_url = reverse_lazy("task_manager:worker")
    template_name = "task_manager/worker_form.html"
