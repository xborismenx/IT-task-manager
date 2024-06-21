from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, TaskType, Task


class TestModels(TestCase):
    def setUp(self):
        self.position_developer = Position.objects.create(id=1, name="developer")
        self.position_designer = Position.objects.create(id=2, name="designer")

        self.task_type = TaskType.objects.create(id=1, name="bug")

        self.username1 = "worker1"
        self.first_name1 = "ivan"
        self.last_name1 = "bogunov"
        self.password1 = "qwerty123"

        self.worker1 = get_user_model().objects.create_user(
            username=self.username1,
            first_name=self.first_name1,
            last_name=self.last_name1,
            position=self.position_developer,
            )
        self.worker1.set_password(self.password1)
        self.worker1.is_active = True
        self.worker1.save()
        self.client.force_login(self.worker1)

        self.worker2 = get_user_model().objects.create_user(
            username="worker2",
            first_name="Maxim",
            last_name="Maximov",
            password="qwerty321",
            position=self.position_designer)

        self.task_id = 1
        self.task_name = "fixed navbar buttons"
        self.task_description = "fix navbar buttons because they must been fixed"
        self.task_deadline = datetime.strptime("2024-01-25 23:00:00", "%Y-%m-%d %H:%M:%S")
        self.task_is_completed = True
        self.task_priority = "2"

        self.task_1 = Task.objects.create(
            id=self.task_id,
            name=self.task_name,
            description=self.task_description,
            deadline=self.task_deadline,
            is_completed=self.task_is_completed,
            priority=self.task_priority,
            task_type=self.task_type,
        )
        self.task_1.assignees.set([self.worker1, self.worker2])

    def test_model_position_name_field(self):
        position = Position.objects.get(name='developer')
        name = position._meta.get_field("name").verbose_name
        self.assertEqual(name, "name")

    def test_model_task_type_field(self):
        task_type = TaskType.objects.get(id=1)
        name = task_type._meta.get_field("name").verbose_name
        self.assertEqual(name, "name")

    def test_model_worker_position_field(self):
        self.assertEqual(self.worker1.position, self.position_developer)

    def test_create_worker(self):
        username = "some_username"
        first_name = "some_first_name"
        last_name = "some_last_name"
        password = "PASSWORD"

        worker = get_user_model().objects.create_user(username=username,
                                                      first_name=first_name,
                                                      last_name=last_name)

        worker.set_password(password)
        worker.save()

        self.assertEqual(worker.username, username)
        self.assertEqual(worker.first_name, first_name)
        self.assertEqual(worker.last_name, last_name)

        self.assertTrue(worker.check_password(password))

    def test_update_worker(self):
        update_url = reverse('task_manager:worker-update', kwargs={'pk': self.worker1.id})
        response = self.client.post(update_url, data={
            "username": self.worker1.username,
            "position": self.position_designer.id,
            "password": self.password1,
            "date_joined": self.worker1.date_joined
        })

        self.assertEqual(response.status_code, 302)

    def test_create_task(self):
        task_id = 2
        task_name = "fixed footer buttons"
        task_description = "fix footer buttons because..."
        task_deadline = datetime.strptime("2025-01-25 23:00:00", "%Y-%m-%d %H:%M:%S")
        task_is_completed = False
        task_priority = "1"

        task = Task.objects.create(
            id=task_id,
            name=task_name,
            description=task_description,
            deadline=task_deadline,
            is_completed=task_is_completed,
            priority=task_priority,
            task_type=self.task_type,
        )
        task.assignees.set([self.worker1, self.worker2])
        self.assertEqual(task.name, task_name)
        self.assertEqual(task.description, task_description)
        self.assertEqual(task.deadline, task_deadline)
        self.assertEqual(task.priority, task_priority)
        self.assertEqual(task.task_type, self.task_type)
        self.assertEqual(list(task.assignees.get_queryset()), [self.worker1, self.worker2])

    def test_update_task(self):
        test_name = "test name task"
        update_url = reverse("task_manager:task-update", kwargs={"pk": self.task_1.pk})
        response = self.client.post(update_url,
                                    {"name": test_name,
                                     "priority":self.task_priority,
                                     "description": self.task_description,
                                     "deadline": self.task_deadline,
                                     "assignees": [self.worker1.id, self.worker2.id]})

        self.assertEqual(response.status_code, 302)

    def test_delete_task(self):
        print(self.worker1.is_authenticated)
        delete_url = reverse("task_manager:task-delete", kwargs={"pk": self.task_1.id})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task_1.id).exists())
