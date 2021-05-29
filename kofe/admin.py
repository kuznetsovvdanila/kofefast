"""Инициализация страничек в админ панели"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from kofe.models import Item, Provider, AddressUser, AddressCafe, Account, Order, Basket, Review, \
    ItemsSlotOrder, ItemsSlotBasket, Volumes, Addons


# Register your models here


class ItemsSlotOrderInLine(admin.StackedInline):
    """Создание структуры для предметов заказа"""
    model = ItemsSlotOrder
    extra = 0


class ItemsSlotBasketInLine(admin.StackedInline):
    """Создание структуры для предметов в корзине"""
    model = ItemsSlotBasket
    extra = 0


class ItemsAddsInLine(admin.StackedInline):
    """Создание структуры для добавок к предмету"""
    model = Addons
    extra = 1


class ItemsVolumesInLine(admin.StackedInline):
    """Создание структуры для объемов предмета"""
    model = Volumes
    extra = 1


class ItemInLine(admin.StackedInline):
    """Создание структуры для продукции кофейни"""
    model = Item
    extra = 0


class CafeAddressesInLine(admin.StackedInline):
    """Создание структуры для адресов кофейни"""
    model = AddressCafe
    extra = 0


class UserBasketsInLine(admin.StackedInline):
    """Создание структуры для отображения корзин(она всегда одна) пользователя"""
    model = Basket
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    """Отображение продукта в админ панели"""
    fieldsets = [
        ('Название', {'fields': ['name']}),
        ('Описание', {'fields': ['description']}),
        ('Цена', {'fields': ['price']}),
        ('Внешка', {'fields': ['preview']}),
        ('Из', {'fields': ['provided']}),
        ('Просчитан цвет', {'fields': ['not_has_color']}),
    ]


class Cafe(admin.ModelAdmin):
    """Отображение кофейни в админ панели"""
    fieldsets = [
        ('Название', {'fields': ['name']}),
        ('Владелец', {'fields': ['owner']}),
        ('Открытие в', {'fields': ['open_time']}),
        ('Закрытие в', {'fields': ['close_time']}),
    ]
    inlines = [ItemInLine, CafeAddressesInLine]


class OrderAdmin(admin.ModelAdmin):
    """Отображение заказа в админ панели"""
    fieldsets = [
        ('Заказчик', {'fields': ['customer']}),
        ('Выбранное кафе', {'fields': ['chosen_cafe']}),
        ('Тип доставки', {'fields': ['type_of_delivery']}),
        # ('Курьер', {'fields': ['courier']}),
        ('Адрес доставки', {'fields': ['chosen_delivery_address']}),
        ('Выбранное время доставки', {'fields': ['time_requested']}),
        ('Закончен ли заказ?', {'fields': ['is_over']}),
        ('Комментарий к заказу', {'fields': ['comment']}),
    ]
    inlines = [ItemsSlotOrderInLine]


class BasketAdmin(admin.ModelAdmin):
    """Отображение корзины в админ панели"""
    fieldsets = [
        ('Заказчик', {'fields': ['customer']}),
    ]
    inlines = [ItemsSlotBasketInLine]


class AccountAdmin(UserAdmin):
    """Отображение аккаунта пользователя в админ панели"""
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    inlines = [UserBasketsInLine]


admin.site.register(Account, AccountAdmin)


admin.site.register(Item, ItemAdmin)
admin.site.register(AddressUser)
admin.site.register(AddressCafe)
admin.site.register(Review)
admin.site.register(Order, OrderAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Provider, Cafe)
