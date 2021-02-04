from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import AnonymousUser
from accounts import views
from core import models


# Email & password for test user
EMAIL = "vasya@pupkin.com"
PASSWORD = "Always#KeepGoing321"

# Correct data for submitting a registration form
DATA = {
    "email": "vasya@pupkin.com",
    "first_name": "Вася",
    "second_name": "Иванов",
    "surname": "Пупкин",
    "password1": "Always#KeepGoing321",
    "password2": "Always#KeepGoing321"
}

# Incorrect data (invalid password confirmation)
DATA_INVALID_CONFIRMATION = {
    "email": "vasya@pupkin.com",
    "first_name": "Вася",
    "second_name": "Иванов",
    "surname": "Пупкин",
    "password1": "Always#KeepGoing321",
    "password2": "Always#KeepGoing"
}

# Incorrect data (common password)
DATA_COMMON_PASSWORD = {
    "email": "vasya@pupkin.com",
    "first_name": "Вася",
    "second_name": "Иванов",
    "surname": "Пупкин",
    "password1": "QWERTY1234",
    "password2": "QWERTY1234"
}


class TestStudentsRegistration(TestCase):
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
        """
        Test the url reverse is correct and it's binded
        with right view function.
        """
        self.assertEqual(reverse('register'), '/register/')
        self.assertEqual(resolve('/register/').func, views.user_register)

    def test_passwords_not_match(self):
        """
        Check that form shows an error for invalid password confirmation.
        """
        response = self.client.post('/register/', DATA_INVALID_CONFIRMATION, follow=True)
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
        """
        Check that form is invalid if user's data
        includes email that is already taken.
        """
        self.user = models.Users.objects.create_user(
            email=EMAIL, password=PASSWORD, first_name="Вася", surname="Пупкин")
        self.student = self.user.create_account()
        response = self.client.post('/register/', DATA, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.redirect_chain)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors), 1)
        self.user.delete()

    def tearDown(self):
        pass


class TestStudentLoginLogout(TestCase):
    """
    Test login/logout systems, pages and urls
    for user with student `account_type`.
    """
    def setUp(self):
        self.user = models.Users.objects.create_user(
            email=EMAIL, password=PASSWORD, first_name="Вася", surname="Пупкин")
        self.student = self.user.create_account()
        self.client = Client()

    def test_logout(self):
        login_response = self.client.login(email=EMAIL, password=PASSWORD)
        self.assertTrue(login_response)
        response = self.client.get("/logout/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0], ('/login/', 302))
        self.assertEqual(response.context['user'], AnonymousUser())

    def test_login_url(self):
        self.assertEqual(reverse('login'), '/login/')

    def test_logout_url(self):
        self.assertEqual(reverse('logout'), '/logout/')

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
