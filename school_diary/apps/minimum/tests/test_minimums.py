from django.test import TestCase, Client


class TestMinimums(TestCase):
    def SetUp(self) -> None:
        self.client = Client()

    def test_minimum_homepage(self):
        response = self.client.get('/minimum/')
        self.assertEqual(response.status_code, 200)