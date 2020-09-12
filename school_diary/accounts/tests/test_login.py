from django.test import TestCase, Client
from diary import models
from django.urls import reverse


EMAIL = "vasya.pupkin@gmail.com"
PASSWORD = "RandomPassword1234"


class TestStudentLogin(TestCase):
    """
    Test login system, login page and login url
    for just created user (student).
    """

    def setUp(self):
        self.user = models.Users.objects.create_user(
            email=EMAIL, password=PASSWORD)
        self.student = models.Students.objects.create(
            account=self.user, first_name="Вася", surname="Пупкин")
        self.client = Client()

    def test_login(self):
        login_response = self.client.login(email=EMAIL, password=PASSWORD)
        self.assertTrue(login_response)
        self.client.logout()

    def test_login_url(self):
        self.assertEqual(reverse('login'), '/login/')

    def test_login_page_get(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_post(self):
        response = self.client.post('/login/', {
            "email": EMAIL,
            "password": PASSWORD,
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)

    def tearDown(self):
        self.user.delete()
