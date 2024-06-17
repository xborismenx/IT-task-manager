from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from task_manager.filters import TaskFilter
from task_manager.forms import SearchTaskForm, TaskForm, WorkerRegistrationForm, SearchWorkerForm
from task_manager.models import Task, Worker


def index(request):
    return render(request, "task_manager/index.html")


class AuthorisationView(generic.View):
    template_name = 'task_manager/authorisation.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'task_manager/authorisation.html')


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"

    def get_ordering(self):
        ordering_deadline = self.request.GET.get('ordering', 'deadline')
        if ordering_deadline not in ['deadline', '-deadline']:
            ordering_deadline = 'deadline'

        ordering_priority = self.request.GET.get('ordering', 'priority')
        if ordering_priority not in ['priority', '-priority']:
            ordering_priority = 'priority'

        return ordering_deadline, ordering_priority

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchTaskForm(initial={"name": name})
        context["filterset"] = self.filterset
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related('task_type').prefetch_related('assignees')
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        self.filterset = TaskFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchTaskForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.all()
        username = self.request.GET.get("name")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset


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


class WorkerRegisterView(generic.View):
    form_class = WorkerRegistrationForm
    template_name = "registration/sign-up.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

        return render(request, self.template_name, {"form": form})
