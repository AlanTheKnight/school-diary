from django.test import TestCase, Client

class TestKlasses(TestCase):
    def SetUp(self) -> None:
        self.client = Client()

    def test_klass_home_page(self):
        response = self.client.get('klasses/my-klass/')
        self.assertEqual(response.status_code, 200)
