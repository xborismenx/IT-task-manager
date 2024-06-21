from django.test import TestCase
from django.urls import reverse

TASK_URL = reverse("task_manager:task-list")
WORKER_URL = reverse("task_manager:worker-list")


class PublicAccessTest(TestCase):
    def test_login_task_required(self):
        response = self.client.get(TASK_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_worker_required(self):
        response = self.client.get(WORKER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_type_create_login_required(self):
        response = self.client.get(reverse("task_manager:task-type-create"))
        self.assertNotEqual(response.status_code, 200)


