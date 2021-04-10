import json

from django.test import TestCase, Client

from apps.timetable import models
from apps.timetable.api import utils


class TestTimeTable(TestCase):
    def setUp(self) -> None:
        klass = models.Klasses.objects.create(number=11, letter="А")
        with open("testData.json", "r") as f:
            data = json.load(f)
        self.lessons = [
            models.Lessons.objects.create(
                klass=klass, day=lesson["day"],
                number=utils.generate_bell(lesson["number"], klass.number)[0],
                subject=lesson['subject'], classroom=lesson['classroom']) for lesson in data
        ]
        self.client = Client()

    def test_timetable_page(self):
        result = self.client.get('/timetable/')
        self.assertEqual(result.status_code, 200)

    def test_timetable_retrieval(self):
        result = self.client.get('/api/timetable/11/А/')
        json_response = json.loads(result.content)
        self.assertEqual(result.status_code, 200)

    def tearDown(self) -> None:
        for lesson in self.lessons:
            lesson.delete()
