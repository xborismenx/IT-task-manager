from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from django.contrib.auth import get_user_model
from task_manager.forms import (
    WorkerRegistrationForm,
    TaskForm,
    SearchTaskForm,
    SearchWorkerForm,
    WorkerCreateUpdateForm
)
from task_manager.models import Position


class FormsTest(TestCase):
    def test_worker_registration_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = WorkerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data['password2'] = 'wrongpassword123'
        form = WorkerRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_task_form(self):
        position = Position.objects.create(name='Developer')
        worker1 = get_user_model().objects.create_user(username='worker1', password='password', position=position)
        worker2 = get_user_model().objects.create_user(username='worker2', password='password', position=position)

        form_data = {
            'name': 'Test Task',
            "description": "description about task",
            "priority": "1",
            'deadline': '2024-12-31T23:59',
            'assignees': [worker1.id, worker2.id]
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data.pop('deadline')
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('deadline', form.errors)

    def test_search_task_form(self):
        form_data = {'name': 'Test Task'}
        form = SearchTaskForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {}
        form = SearchTaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_worker_form(self):
        form_data = {'name': 'Test Worker'}
        form = SearchWorkerForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {}
        form = SearchWorkerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_create_update_form(self):
        position = Position.objects.create(name='Developer')

        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'position': position.id
        }
        form = WorkerCreateUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data.pop('last_name')
        form = WorkerCreateUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

        form_data['last_name'] = 'User'
        form_data['password2'] = 'wrongpassword123'
        form = WorkerCreateUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
