from django.contrib import admin
from kofe.models import Item, Provider


# Register your models here


class ItemInLine(admin.StackedInline):
    model = Item
    extra = 0


class Cafe(admin.ModelAdmin):
    fieldsets = [
        ('Название', {'fields': ['name']}),
    ]
    inlines = [ItemInLine]


admin.site.register(Provider, Cafe)
