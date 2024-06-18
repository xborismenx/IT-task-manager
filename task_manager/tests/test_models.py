from django.test import TestCase

from task_manager.models import Position


class TestModels(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="developer")

    def test_model_position_name_field(self):
        position = Position.objects.get(name='developer')
        name = position._meta.get_field("name").verbose_name
        self.assertEqual(name, "name")

    def test_model_position_max_length_and_str(self):
        field_name_len = Position._meta.get_field("name").max_length
        name = Position.objects.get(name='developer')
        self.assertEqual(field_name_len, 100)
        self.assertEqual(name.__str__(), "developer")
