"""Описание тестов для проверки работоспособности приложения"""
from django.test import TestCase, Client
from django.urls import reverse

from kofeFast.settings import AUTH_USER_MODEL


class IndexPageTestCase(TestCase):
    """Тесты view 'index.html' """
    def setUp(self) -> None:
        """Сетап для тестов view 'index.html' """
        self.client = Client()
        self.response = self.client.get(reverse('index'))

    def test_index_response(self):
        """Тест на ответ страницы"""
        self.assertEqual(self.response.status_code, 200)


class PersonalAreaPageTestCase(TestCase):
    """Тесты view 'personal_area.html' """
    fixtures = ['test_database.json']

    def setUp(self) -> None:
        """Сетап для тестов view 'personal_area.html' """
        self.client = Client()
        self.user = AUTH_USER_MODEL.objects.get(email='1@gmail.com')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('personal_area'))

    def test_index_response(self):
        """Тест на ответ страницы"""
        self.assertEqual(self.response.status_code, 200)
