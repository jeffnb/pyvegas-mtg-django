from django.test import TestCase
from cards.forms import CardForm
from cards.models import Edition, Color

class CardFormTest(TestCase):
    def setUp(self):
        self.edition = Edition.objects.create(name='Test Edition', code='TST')
        self.color = Color.objects.create(name='Red', code=Color.RED)

    def test_card_form_valid(self):
        """Test that the form is valid with all required fields"""
        form_data = {
            'name': 'Test Card',
            'mana_cost': '{1}{R}',
            'text': 'Test card text',
            'flavor': 'Test flavor text',
            'type': 'Creature — Human Wizard',
            'power': '2',
            'toughness': '1',
            'rarity': 'Rare',
            'set_name': 'Test Set',
            'image_url': 'https://example.com/image.jpg',
            'edition': self.edition.id,
            'colors': [self.color.id]
        }
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_card_form_invalid_missing_required(self):
        """Test that the form is invalid when required fields are missing"""
        # Missing name, type, power, toughness, rarity, set_name, image_url, edition
        form_data = {
            'mana_cost': '{1}{R}',
            'text': 'Test card text',
            'flavor': 'Test flavor text',
            'colors': [self.color.id]
        }
        form = CardForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('type', form.errors)
        self.assertIn('power', form.errors)
        self.assertIn('toughness', form.errors)
        self.assertIn('rarity', form.errors)
        self.assertIn('set_name', form.errors)
        self.assertIn('image_url', form.errors)
        self.assertIn('edition', form.errors)

    def test_card_form_optional_fields(self):
        """Test that the form is valid when optional fields are missing"""
        # mana_cost, text, and flavor are optional
        form_data = {
            'name': 'Test Card',
            'type': 'Creature — Human Wizard',
            'power': '2',
            'toughness': '1',
            'rarity': 'Rare',
            'set_name': 'Test Set',
            'image_url': 'https://example.com/image.jpg',
            'edition': self.edition.id,
            'colors': [self.color.id]  # Colors is required
        }
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_card_form_invalid_url(self):
        """Test that the form is invalid with an invalid URL"""
        form_data = {
            'name': 'Test Card',
            'type': 'Creature — Human Wizard',
            'power': '2',
            'toughness': '1',
            'rarity': 'Rare',
            'set_name': 'Test Set',
            'image_url': 'not-a-url',  # Invalid URL
            'edition': self.edition.id
        }
        form = CardForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('image_url', form.errors)
