from django.contrib import admin

from cards.models import Card, Edition, Color


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['name', 'edition', 'rarity', 'type', 'power', 'toughness']
    list_filter = ['edition', 'rarity', 'type']
    search_fields = ['name', 'edition', 'rarity', 'type', 'text']
    ordering = ['name']

@admin.register(Edition)
class EditionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')