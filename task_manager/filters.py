import django_filters
from django_filters import CharFilter

from task_manager.models import Task


class TaskFilter(django_filters.FilterSet):
    priority = django_filters.ChoiceFilter(
        field_name="priority",
        choices=Task.PriorityType.choices,
        label="Priority"
    )

    class Meta:
        model = Task
        fields = ["priority"]
