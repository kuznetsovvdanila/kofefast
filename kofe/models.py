from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from kofeFast import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models

from kofeFast.settings import AUTH_USER_MODEL


class AddressUser(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')
    name = models.CharField('Имя', max_length=30, default='Дом')
    city = models.CharField('Город', max_length=30, default='Москва')
    street = models.CharField('Улица', max_length=30, default='Арбат')
    house = models.CharField('Дом', max_length=30, default='-1')
    building = models.CharField('Корпус', max_length=30, default='-1')
    entrance = models.IntegerField('Подъезд', default=-1)
    floor = models.IntegerField('Этаж', default=-1)
    flat = models.IntegerField('Квартира', default=-1)

    def __str__(self):
        return str(self.city) + ' ' + str(self.street) + ' ' + str(self.house)

    class Meta:
        verbose_name = "Адрес Пользователя"
        verbose_name_plural = "Адреса Пользователя"


class AddressCafe(models.Model):
    owner = models.ForeignKey('Provider', on_delete=models.CASCADE, verbose_name='Владелец')
    city = models.CharField('Город', max_length=30, default='Москва')
    street = models.CharField('Улица', max_length=30, default='Арбат')
    house = models.CharField('Дом', max_length=30, default='-1')
    building = models.CharField('Корпус', max_length=30, default='-1')
    entrance = models.IntegerField('Подъезд', default=-1)

    def __str__(self):
        return str(self.owner)

    class Meta:
        verbose_name = "Адрес Кофейни"
        verbose_name_plural = "Адреса Кофейни"


class Volumes(models.Model):
    volume = models.CharField('Объем', max_length=4, default='0.')
    source = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name='Чей??')

    def __str__(self):
        return str(self.volume)

    class Meta:
        verbose_name = "Объем"
        verbose_name_plural = "Объемы"


class Addons(models.Model):
    addth = models.CharField('Добавка', max_length=15, default='ниче')
    sourceItem = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name='К чему??')

    def __str__(self):
        return str(self.addth)

    class Meta:
        verbose_name = "Добавка"
        verbose_name_plural = "Добавки"


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

    other_volumes = models.ManyToManyField('Volumes', blank=True)
    additions = models.ManyToManyField('Addons', blank=True)

    FoodTypes = [
        ('e', 'Eatable'),
        ('d', 'Drinkable'),
    ]

    type = models.CharField(max_length=1, choices=FoodTypes, default='d')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукция"


class ItemsSlotOrder(models.Model):
    count = models.IntegerField('Количество', default=1)
    good = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name='Продукт')
    order_connection = models.ForeignKey('Order', on_delete=models.CASCADE,
                                         verbose_name='К какому заказу привязан', default=None)

    def __str__(self):
        return str(self.good.name) + ' в количестве ' + str(self.count)

    class Meta:
        verbose_name = "Слот в корзине"
        verbose_name_plural = "Слоты в корзине"


class ItemsSlotBasket(models.Model):
    count = models.IntegerField('Количество', default=1)
    good = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name='Продукт')
    basket_connection = models.ForeignKey('Basket', on_delete=models.CASCADE,
                                          verbose_name='К какой корзине привязан', default=None)

    def __str__(self):
        return str(self.good.name) + ' в количестве ' + str(self.count)

    class Meta:
        verbose_name = "Слот в корзине"
        verbose_name_plural = "Слоты в корзине"


class Provider(models.Model):
    name = models.CharField('Название', max_length=50)
    cafe_addresses = models.ManyToManyField('AddressCafe', blank=True)
    production = models.ManyToManyField('Item', blank=True)
    owner = models.ManyToManyField(AUTH_USER_MODEL, blank=True, verbose_name='Владелец')

    open_time = models.CharField('Открытие в', max_length=10, default='9')
    close_time = models.CharField('Закрытие в', max_length=10, default='23')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кафе"
        verbose_name_plural = "Кофейни"


class Review(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', unique=True)
    content = models.CharField('Содержание', max_length=500, default='Мы лучшие')
    time_created = models.TimeField('Время создания отзыва', auto_now_add=False, auto_now=False)

    def __str__(self):
        return 'Отзыв от ' + str(self.author)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Order(models.Model):
    customer = models.ForeignKey(AUTH_USER_MODEL, related_name='customer', on_delete=models.CASCADE,
                                 verbose_name='Заказчик')
    chosen_items = models.ManyToManyField(ItemsSlotOrder, blank=True, verbose_name="Выбранные продукты")
    chosen_cafe = models.ForeignKey('AddressCafe', on_delete=models.CASCADE, verbose_name='Выбранное кафе')
    type_of_delivery = models.CharField('Тип доставки', max_length=10, default='Самовывоз')
    #courier = models.ForeignKey(AUTH_USER_MODEL, related_name='courier', on_delete=models.CASCADE,
    #                            verbose_name='Курьер', unique=True, default=None)
    chosen_delivery_address = models.ManyToManyField('AddressUser', blank=True, verbose_name='Выбранный адрес доставки')
    time_created = models.TimeField('Время создания заказа', auto_now_add=True, auto_now=False)
    time_requested = models.TimeField('Время на выполнение заказа', default=datetime.now()+timedelta(minutes=20))
    time_over = models.DateTimeField('Время завершения заказа', auto_now=True)
    is_over = models.BooleanField('Окончен ли заказ?', default=False)

    comment = models.CharField('Комментарий к заказу', max_length=500, default='лучший сервис')

    def __str__(self):
        return "Заказ от " + str(self.customer) + " из " + str(self.chosen_cafe) + " время: " + str(self.time_created)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Basket(models.Model):
    customer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Заказчик', unique=True)
    chosen_items = models.ManyToManyField(ItemsSlotBasket, blank=True, verbose_name="Выбранные продукты")

    def all_cost(self):
        cost = 0

        for i in self.chosen_items.all():
            cost += i.good.price * i.count

        return cost

    def __str__(self):
        return "Корзина " + str(self.customer)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have an name')
        if not last_name:
            raise ValueError('Users must have an surname')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name="Антон",
            last_name="Крутой",
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=60, default='username')
    email 					= models.EmailField(verbose_name="Почта", max_length=60, unique=True)
    date_joined				= models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='Последний вход', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_cafe_owner		    = models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    y                       = models.IntegerField('Прокрутка', default=0)

    profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures", default=None)

    first_name = models.CharField('Имя', max_length=60, default='first_name')
    last_name = models.CharField('Фамилия', max_length=60, default='last_name')

    user_basket = models.ManyToManyField(Basket, blank=True, verbose_name="Пользовательские корзины корзина")
    chosen_address = models.ManyToManyField(AddressUser, blank=True, verbose_name="Выбранный адрес")
    phone_number = models.CharField('Номер телефона', max_length=13, default="89142185648")

    owned_cafe = models.ManyToManyField(Provider, blank=True, verbose_name="Владеет кофейней")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
