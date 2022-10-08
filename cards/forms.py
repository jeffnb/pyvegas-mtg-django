from django import forms

from cards.models import Card


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ['id']