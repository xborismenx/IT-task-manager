from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=100)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)


class TaskType(models.Model):
    name = models.CharField(max_length=255)


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
