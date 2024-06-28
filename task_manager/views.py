from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import View

from task_manager.forms import SearchTaskForm, TaskForm, WorkerRegistrationForm, WorkerCreateForm, WorkerUpdateForm, \
    CommentsForm
from task_manager.models import Task, Worker, TaskType, Commentaries


def index(request):
    return render(request, "task_manager/index.html")


def learn_more_1(request):
    return render(request, "task_manager/learn-more-1.html")


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
        name = self.request.GET.get('name', '')
        context['search_form'] = SearchTaskForm(initial={'name': name})

        current_ordering_deadline, current_ordering_priority = self.get_ordering()
        context['current_ordering_deadline'] = current_ordering_deadline
        context['current_ordering_priority'] = current_ordering_priority
        context['next_ordering'] = {
            'deadline': 'deadline' if current_ordering_deadline == '-deadline' else '-deadline',
            'priority': 'priority' if current_ordering_priority == '-priority' else '-priority'
        }

        task_types = TaskType.objects.annotate(task_count=Count('task'))
        context['task_types'] = [
            {
                'name': task_type.name,
                'task_count': task_type.task_count,
                'task_pk': task_type.pk,
            }
            for task_type in task_types
        ]
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related('task_type')
        name = self.request.GET.get('name')
        task_type = self.request.GET.get('type')
        ordering_deadline, ordering_priority = self.get_ordering()

        if ordering_deadline.startswith("-"):
            queryset = queryset.order_by(ordering_deadline)

        if ordering_priority.startswith("-"):
            queryset = queryset.order_by(ordering_priority)

        if name:
            queryset = queryset.filter(name__icontains=name)
            return queryset
        if task_type:
            queryset = queryset.filter(task_type__name=task_type)
            return queryset
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/task_form.html"


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"

    def get_queryset(self):
        return Task.objects.prefetch_related("assignees", "comments__worker", "comments__worker__position")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments_form"] = CommentsForm()
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        content = request.POST.get("content")
        worker = self.request.user
        Commentaries.objects.create(task=task, content=content, worker=worker)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('task_manager:task-detail', kwargs={'pk': self.get_object().pk})


class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Commentaries, pk=kwargs['pk'], worker=request.user)
        task_pk = comment.task.pk
        comment.delete()
        return redirect('task_manager:task-detail', pk=task_pk)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/task_form.html"


class DeleteTaskView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/task_confirm_delete.html"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/tasktype_confirm_delete.html"


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 4
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
        queryset = Worker.objects.all().select_related("position")
        username = self.request.GET.get("name")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    success_url = reverse_lazy("task_manager:worker-list")
    template_name = "task_manager/worker_form.html"


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")
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
