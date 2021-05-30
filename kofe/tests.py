"""Описание тестов для проверки работоспособности приложения"""
from django.test import TestCase, Client
from django.urls import reverse

from kofeFast.settings import AUTH_USER_MODEL


class IndexPageTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get(reverse('index'))

    def test_index_response(self):
        self.assertEqual(self.response.status_code, 200)


class PersonalAreaPageTestCase(TestCase):
    fixtures = ['test_database.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = AUTH_USER_MODEL.objects.get(email='1@gmail.com')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('personal_area'))

    def test_index_response(self):
        self.assertEqual(self.response.status_code, 200)
