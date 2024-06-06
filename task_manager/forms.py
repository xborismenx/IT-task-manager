from django import forms
from django.contrib.auth import get_user_model

from task_manager.models import Task, Worker


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={
            "type": "datetime-local"
        }
    ))
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = "__all__"


class SearchTaskForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "search by name"
            }
        )
    )
