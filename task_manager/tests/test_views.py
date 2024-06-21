from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.models import TaskType, Task, Position, Worker


class ViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.task_type = TaskType.objects.create(name="Bug")
        self.position_developer = Position.objects.create(id=1, name="Developer")
        self.position_designer = Position.objects.create(name="Designer")
        self.worker1 = get_user_model().objects.create_user(
            username="worker1",
            first_name="Ivan",
            last_name="Bogunov",
            position=self.position_developer
        )
        self.worker2 = get_user_model().objects.create_user(
            username="worker2",
            first_name="Maxim",
            last_name="Maximov",
            position=self.position_designer
        )
        self.task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            deadline="2024-12-31 23:59:59",
            priority="1",
            task_type=self.task_type
        )
        self.worker1.active = True
        self.client.force_login(self.worker1)

    def test_index_view(self):
        response = self.client.get(reverse('task_manager:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/index.html')

    def test_authorisation_view(self):
        response = self.client.get(reverse('task_manager:authorisation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/authorisation.html')

    def test_task_list_view(self):
        response = self.client.get(reverse('task_manager:task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task_list.html')

    def test_task_create_view(self):
        response = self.client.post(reverse('task_manager:task-create'), {
            'name': 'New Task',
            'description': 'Task description',
            'deadline': '2024-12-31 23:59:59',
            'priority': '1',
            'task_type': self.task_type.id,
            'assignees': [self.worker1.id, self.worker2.id]
        })
        self.assertEqual(response.status_code, 302)

    def test_task_detail_view(self):
        response = self.client.get(reverse('task_manager:task-detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task_detail.html')

    def test_task_update_view(self):
        response = self.client.post(reverse('task_manager:task-update', kwargs={'pk': self.task.pk}), {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'deadline': '2024-12-31 23:59:59',
            'priority': '1',
            'task_type': self.task_type.id,
            'assignees': [self.worker1.id, self.worker2.id]
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_task_view(self):
        response = self.client.post(reverse('task_manager:task-delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_type_create_view(self):
        response = self.client.post(reverse('task_manager:task-type-create'), {'name': 'New Type'})
        self.assertEqual(response.status_code, 302)

    def test_task_type_delete_view(self):
        task_type = TaskType.objects.create(name="Feature")
        response = self.client.post(reverse('task_manager:task-type-delete', kwargs={'pk': task_type.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TaskType.objects.filter(pk=task_type.pk).exists())

    def test_worker_list_view(self):
        response = self.client.get(reverse('task_manager:worker-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/worker_list.html')

    def test_worker_create_view(self):
        response = self.client.post(reverse('task_manager:worker-create'), {
            'username': 'newworker',
            'first_name': 'First',
            'last_name': 'Last',
            'position': self.position_developer.id,
            "password1": "password321",
            "password2": "password321"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Worker.objects.filter(username='newworker').exists())

    def test_worker_update_view(self):
        response = self.client.post(reverse('task_manager:worker-update', kwargs={'pk': self.worker1.pk}), {
            'username': 'updatedworker',
            'first_name': 'Updated',
            'last_name': 'Worker',
            'position': self.position_developer.id,
            "password1": "qwert123QWERT",
            "password2": "qwert123QWERT"
        })
        self.assertEqual(response.status_code, 302)
        self.worker1.refresh_from_db()
        self.assertEqual(self.worker1.username, 'updatedworker')

    def test_worker_register_view_get(self):
        response = self.client.get(reverse('task_manager:worker-register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/sign-up.html')

    def test_worker_register_view_post(self):
        response = self.client.post(reverse('task_manager:worker-register'), {
            'username': 'newuser',
            'first_name': 'First',
            'last_name': 'Last',
            "email": "f@mail.com",
            'password1': 'password123PASS',
            'password2': 'password123PASS'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())
