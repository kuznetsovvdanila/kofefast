from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from kofeFast import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Address(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    city = models.CharField('Город', max_length=30, default='Москва')
    street = models.CharField('Улица', max_length=30, default='Арбат')
    house = models.IntegerField('Дом', default=1)
    entrance = models.IntegerField('Подъезд', default=None)

    def __str__(self):
        return str(self.owner)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"


class Item(models.Model):
    price = models.IntegerField('Цена', default=300)
    preview = models.ImageField('Внешка', default=None, upload_to='item_picture')
    provided = models.ForeignKey('Provider', on_delete=models.CASCADE)
    name = models.CharField('Продукт', max_length=50, default='coffee')
    description = models.CharField('Описание',
                                   max_length=250,
                                   default='Съешь ещё этих мягких французских булок, да выпей же чаю')
    not_has_color = models.BooleanField('Не просчитан цвет', default=True)
    primary_color = models.CharField('Главный цвет превью', max_length=50, default="0, 0, 0, 255")

    FoodTypes = [
        ('e', 'Eatable'),
        ('d', 'Drinkable'),
    ]

    type = models.CharField(max_length=1, choices=FoodTypes, default='e')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Итем"
        verbose_name_plural = "Айтемы"


class Provider(models.Model):
    name = models.CharField('Название', max_length=50)
    production = models.ManyToManyField('Item', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кафе"
        verbose_name_plural = "Кофейни"
