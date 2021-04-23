from django.test import TestCase, Client
from apps.core import models


class TestHomework(TestCase):
    def SetUp(self) -> None:
        self.client = Client()

    def Test_homework_page(self):
        response = self.client.get('/homework/')
        self.assertEqual(response.status_code, 200)

    def Test_stat_page(self):
        response = self.client.get('/homework-stats/')
        self.assertEqual(response.status_code, 200)

    def Test_homework_list(self):
        response = self.client.get('/homework-list/4')
        self.assertEqual(response.status_code, 200)
