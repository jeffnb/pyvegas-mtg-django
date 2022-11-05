import json

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from cards.forms import CardForm
from cards.models import Card


def form_create(request):

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('https://www.google.com')

    else:
        form = CardForm()

    return render(request, 'cards/card_create.html', {'name': 'John', 'form': form})

def index(request):
    cards = Card.objects.order_by('?')[:9]

    return render(request, 'cards/index.html', {'cards': cards})