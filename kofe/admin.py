from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from kofe.models import Item, Provider, AddressUser, AddressCafe, Account, Order, Basket, Review, ItemsSlotOrder, \
    ItemsSlotBasket

from django.utils.translation import gettext, gettext_lazy as _

# Register your models here


class ItemsSlotOrderInLine(admin.StackedInline):
    model = ItemsSlotOrder
    extra = 0


class ItemsSlotBasketInLine(admin.StackedInline):
    model = ItemsSlotBasket
    extra = 0


class ItemInLine(admin.StackedInline):
    model = Item
    extra = 0


class CafeAddressesInLine(admin.StackedInline):
    model = AddressCafe
    extra = 0


class UserBasketsInLine(admin.StackedInline):
    model = Basket
    extra = 1


class Cafe(admin.ModelAdmin):
    fieldsets = [
        ('Название', {'fields': ['name']}),
    ]
    inlines = [ItemInLine, CafeAddressesInLine]


class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Заказчик', {'fields': ['customer']}),
        ('Выбранное кафе', {'fields': ['chosen_cafe']}),
        ('Тип доставки', {'fields': ['type_of_delivery']}),
        ('Курьер', {'fields': ['courier']}),
        ('Адрес доставки', {'fields': ['chosen_delivery_address']}),
        ('Выбранное время доставки', {'fields': ['time_requested']}),
        ('Закончен ли заказ?', {'fields': ['is_over']}),
    ]
    inlines = [ItemsSlotOrderInLine]


class BasketAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Заказчик', {'fields': ['customer']}),
        ('Выбранное кафе', {'fields': ['chosen_cafe']}),
        ('Адрес доставки', {'fields': ['chosen_delivery_address']}),
    ]
    inlines = [ItemsSlotBasketInLine]


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    inlines = [UserBasketsInLine]


admin.site.register(Account, AccountAdmin)

admin.site.register(AddressUser)
admin.site.register(AddressCafe)
admin.site.register(Review)
admin.site.register(Order, OrderAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Provider, Cafe)
