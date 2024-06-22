from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey
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

    def test_position_name_field(self):
        position = Position.objects.get(name='developer')
        name = position._meta.get_field("name").verbose_name
        self.assertEqual(name, "name")

    def test_task_type_field(self):
        task_type = TaskType.objects.get(id=1)
        name = task_type._meta.get_field("name").verbose_name
        self.assertEqual(name, "name")

    def test_worker_position_field(self):
        position = get_user_model()._meta.get_field("position")
        self.assertEqual(self.worker1.position, self.position_developer)
        self.assertTrue(isinstance(position, ForeignKey))

    def test_worker_absolute_url(self):
        self.assertEqual(self.worker1.get_absolute_url(), "/workers/1/update/")

    def test_worker_str(self):
        self.assertEqual(self.worker1.__str__(), 'ivan bogunov (worker1) - position developer')

    def test_task_model_fields(self):
        self.assertEqual(self.task_1.name, self.task_name)
        self.assertEqual(self.task_1.description, self.task_description)
        self.assertEqual(self.task_1.deadline, self.task_deadline)
        self.assertEqual(self.task_1.is_completed, self.task_is_completed)
        self.assertEqual(self.task_1.priority, self.task_priority)
        self.assertEqual(self.task_1.task_type, self.task_type)
        self.assertEqual(self.task_1.assignees.count(), 2)

    def test_absolute_url(self):
        self.assertEqual(self.task_1.get_absolute_url(), "/tasks/1/")

