from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from kofeFast import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Item(models.Model):
    price = models.IntegerField('Цена', default=300)
    preview = models.ImageField('Внешка', default=None, upload_to='item_picture')
    provided = models.ForeignKey('Provider', on_delete=models.CASCADE)
    name = models.CharField('Продукт', max_length=50, default='coffee')

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
