from django.test import TestCase, Client
from apps.minimum import models

class TestMinimums(TestCase):
    def SetUp(self) -> None:
        self.client = Client()
        models.Documents.objects.create(
            subject="Информатика",
            grade="9",
            term="1",
        )

    def test_minimum_homepage(self):
        response = self.client.get('/minimum/')
        self.assertEqual(response.status_code, 200)

    def test_minimum_requests(self):
        responce=self.client.get('/minimum/')