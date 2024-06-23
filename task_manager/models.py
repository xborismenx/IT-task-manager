from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username}) - position {self.position}"

    def get_absolute_url(self):
        return reverse("task_manager:worker-update", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Task(models.Model):
    class PriorityType(models.TextChoices):
        URGENT = "1", "Urgent"
        HIGH = "2", "High"
        MEDIUM = "3", "Medium"
        LOW = "4", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=1,
        choices=PriorityType.choices,
        default=PriorityType.MEDIUM
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True, blank=True)
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    def get_absolute_url(self):
        return reverse("task_manager:task-detail", kwargs={"pk": self.pk})
