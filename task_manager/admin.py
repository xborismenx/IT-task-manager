from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Position, Worker, TaskType, Task

admin.site.register(Position)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", )
    fieldsets = UserAdmin.fieldsets + (("Position", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Position", {"fields": ("position", )}),)


admin.site.register(TaskType)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'deadline', "is_completed", "priority", "task_type",)
