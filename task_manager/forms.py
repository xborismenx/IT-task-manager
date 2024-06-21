from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Task, Worker


class WorkerRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', "placeholder": "username"}
        )
    )
    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-lg', "placeholder": "email"}
        )
    )
    password1 = forms.CharField(
        label="password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', "placeholder": "password"}
        )
    )

    password2 = forms.CharField(
        label="password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', "placeholder": "password confirmation"}
        )
    )

    class Meta:
        model = Worker
        fields = ("username", "email", "password1", "password2")


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
                "placeholder": "search by name",
                "class": "form-control form__input",
                "style": "width: 150px;"
            }
        )
    )


class SearchWorkerForm(forms.Form):
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


class WorkerCreateUpdateForm(UserCreationForm):
    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Worker
        fields = ('username', 'first_name', 'last_name', "position")

