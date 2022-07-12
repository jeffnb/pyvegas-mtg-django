import json

from django.shortcuts import render

# Create your views here.
from cards.models import Color, Card, Edition


def index(request):
    with open('data/all_mtg_cards.json') as f:
        data = json.load(f)

    colors = {}
    for color in Color.objects.all():
        colors[color.name] = color

    editions = {}
    for edition in Edition.objects.all():
        editions[edition.code] = edition


    for card in data:
        edition = editions[card['set']]

        db_card = Card.objects.create(name=card['name'],
                                    mana_cost=card['mana_cost'],
                                    text=card['text'],
                                    flavor=card['flavor'],
                                    type=card['type'],
                                    power=card['power'],
                                    toughness=card['toughness'],
                                    rarity=card['rarity'],
                                    image_url=card['image_url'],
                                    pk=card['id'],
                                    edition=edition)
        try:
            db_card.save()
        except Exception as e:
            continue

        for color in card['colors']:
            db_color = colors[color]
            db_card.colors.add(db_color)
            db_card.save()


    return "Hello, world. You're at the cards index."