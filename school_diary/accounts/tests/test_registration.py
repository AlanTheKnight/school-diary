from django.test import TestCase, Client
from django.urls import reverse, resolve
from accounts import views
from diary import models


EMAIL = "vasya@pupkin.com"
PASSWORD = "Always#KeepGoing321"


DATA = {
    "email": "vasya@pupkin.com",
    "first_name": "Вася",
    "second_name": "Иванов",
    "surname": "Пупкин",
    "password1": "Always#KeepGoing321",
    "password2": "Always#KeepGoing321"
}


DATA_INCORRECT_PASSWORD = {
    "email": "vasya@pupkin.com",
    "first_name": "Вася",
    "second_name": "Иванов",
    "surname": "Пупкин",
    "password1": "Always#KeepGoing321",
    "password2": "Always#KeepGoing"
}

DATA_COMMON_PASSWORD = {
    "email": "vasya@pupkin.com",
    "first_name": "Вася",
    "second_name": "Иванов",
    "surname": "Пупкин",
    "password1": "QWERTY1234",
    "password2": "QWERTY1234"
}


class TestRegistration(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_page(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_page_post(self):
        """Test a registration form with a valid data."""
        response = self.client.post('/register/', DATA, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/login/')
        self.assertEqual(response.redirect_chain[0][1], 302)

    def test_register_url(self):
        """Test the url is correct"""
        self.assertEqual(reverse('register'), '/register/')
        self.assertEqual(resolve('/register/').func, views.user_register)

    def test_passwords_not_match(self):
        """Check that form shows an error for unmatched passwords."""
        response = self.client.post('/register/', DATA_INCORRECT_PASSWORD, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(len(response.context['form'].errors), 1)
        self.assertFalse(response.context['form'].is_valid())

    def test_common_password(self):
        """Check that form shows an error for a common password."""
        response = self.client.post('/register/', DATA_COMMON_PASSWORD, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.redirect_chain)
        self.assertEqual(len(response.context['form'].errors), 1)
        self.assertFalse(response.context['form'].is_valid())

    def test_email_exists(self):
        self.user = models.Users.objects.create_user(
            email=EMAIL, password=PASSWORD)
        self.student = models.Students.objects.create(
            account=self.user, first_name="Вася", surname="Пупкин")

        response = self.client.post('/register/', DATA, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.redirect_chain)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors), 1)

        self.user.delete()

    def tearDown(self):
        pass
