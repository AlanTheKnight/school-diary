from django.test import TestCase, Client

from apps.timetable import views


class TestViews(TestCase):
    def SetUp(self) -> None:
        self.client = Client()

    def test_timetable_page(self):
        response = self.client.get("/timetable/")
        self.assertEqual(response.status_code, 200)
