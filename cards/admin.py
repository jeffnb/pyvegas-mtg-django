from django.contrib import admin

from cards.models import Card, Color, Edition


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Edition)
class EditionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'mana_cost', 'type', 'rarity', 'set_name')
    list_filter = ('type', 'rarity', 'set_name')



