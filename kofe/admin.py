from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from kofe.models import Item, Provider, AddressUser, AddressCafe, Account, Order

from django.utils.translation import gettext, gettext_lazy as _

# Register your models here


class ItemInLine(admin.StackedInline):
    model = Item
    extra = 0


class CafeAddressesInLine(admin.StackedInline):
    model = AddressCafe
    extra = 0


class Cafe(admin.ModelAdmin):
    fieldsets = [
        ('Название', {'fields': ['name']}),
    ]
    inlines = [ItemInLine, CafeAddressesInLine]


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)

admin.site.register(AddressUser)
admin.site.register(AddressCafe)
admin.site.register(Order)
admin.site.register(Provider, Cafe)
