from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from kofe.models import Item, Provider, Address


# Register your models here


class ItemInLine(admin.StackedInline):
    model = Item
    extra = 0


class Cafe(admin.ModelAdmin):
    fieldsets = [
        ('Название', {'fields': ['name']}),
    ]
    inlines = [ItemInLine]


admin.site.register(Address)
admin.site.register(Provider, Cafe)
