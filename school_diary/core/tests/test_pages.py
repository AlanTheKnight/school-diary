from django.test import TestCase, Client


class TestPages(TestCase):
    def setup(self):
        self.client = Client()

    def test_homepage(self):
        r = self.client.get('')
        self.assertEqual(r.status_code, 200)
