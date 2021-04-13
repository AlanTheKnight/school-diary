from django.test import TestCase, Client
from apps.news import models


class TestNews(TestCase):
    def SetUp(self) -> None:
        self.client = Client()

    def test_news_home_page(self):
        response = self.client.get('/news/page/1')
        self.assertEqual(response.status_code, 200)

    def test_news_post_page(self):
        models.Publications.objects.create(title="asqwde",
                                           author="Kaedone",
                                           content="asdfghjkl",
                                           slug="new-post")
        r = self.client.get('/news/post/new-post')
        self.assertEqual(r.status_code, 200)

    def test_creating_news(self):
        res = self.client.post('/news/create/', {
            "title": "asqwd",
            "author": "Kaedone",
            "content": "ugydf",
            "slug": "old-post"
        })
        self.assertEqual(res.status_code, 302)

    def test_searching_news(self):
        models.Publications.objects.create(title="asqwde",
                                           author="Kaedone",
                                           content="asdfghjkl",
                                           slug="new-post")
        response = self.client.get('/news/page/1?search=asqwde')
        self.assertEqual(len(response.context["news"]), 1)
