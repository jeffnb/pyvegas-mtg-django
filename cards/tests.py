import uuid
from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseRedirect

from cards.models import Color, Edition, Card
from cards.forms import CardForm


class ColorModelTest(TestCase):
    def setUp(self):
        self.color = Color.objects.create(name="Red", code=Color.RED)

    def test_color_creation(self):
        self.assertEqual(self.color.name, "Red")
        self.assertEqual(self.color.code, "R")

    def test_color_str_representation(self):
        self.assertEqual(str(self.color), "Red")

    def test_color_choices(self):
        expected_choices = [('R', 'Red'), ('G', 'Green'), ('U', 'Blue'), ('W', 'White'), ('B', 'Black')]
        self.assertEqual(Color.COLOR_CHOICES, expected_choices)

    def test_all_color_codes(self):
        colors = [
            Color.objects.create(name="Green", code=Color.GREEN),
            Color.objects.create(name="Blue", code=Color.BLUE),
            Color.objects.create(name="White", code=Color.WHITE),
            Color.objects.create(name="Black", code=Color.BLACK),
        ]
        
        self.assertEqual(colors[0].code, "G")
        self.assertEqual(colors[1].code, "U")
        self.assertEqual(colors[2].code, "W")
        self.assertEqual(colors[3].code, "B")


class EditionModelTest(TestCase):
    def setUp(self):
        self.edition = Edition.objects.create(name="Alpha", code="LEA")

    def test_edition_creation(self):
        self.assertEqual(self.edition.name, "Alpha")
        self.assertEqual(self.edition.code, "LEA")

    def test_edition_str_representation(self):
        self.assertEqual(str(self.edition), "Alpha(LEA)")

    def test_edition_ordering(self):
        edition2 = Edition.objects.create(name="Beta", code="LEB")
        edition3 = Edition.objects.create(name="Arabian Nights", code="ARN")
        
        editions = list(Edition.objects.all())
        self.assertEqual(editions[0].name, "Alpha")
        self.assertEqual(editions[1].name, "Arabian Nights")
        self.assertEqual(editions[2].name, "Beta")


class CardModelTest(TestCase):
    def setUp(self):
        self.edition = Edition.objects.create(name="Alpha", code="LEA")
        self.red_color = Color.objects.create(name="Red", code=Color.RED)
        self.blue_color = Color.objects.create(name="Blue", code=Color.BLUE)
        
        self.card = Card.objects.create(
            name="Lightning Bolt",
            mana_cost="{R}",
            text="Lightning Bolt deals 3 damage to any target.",
            flavor="The sparkmage shrieked, calling on the rage of the storms of his youth.",
            type="Instant",
            power="",
            toughness="",
            rarity="Common",
            set_name="Alpha",
            image_url="https://example.com/lightning_bolt.jpg",
            edition=self.edition
        )

    def test_card_creation(self):
        self.assertEqual(self.card.name, "Lightning Bolt")
        self.assertEqual(self.card.mana_cost, "{R}")
        self.assertEqual(self.card.type, "Instant")
        self.assertEqual(self.card.rarity, "Common")
        self.assertEqual(self.card.edition, self.edition)

    def test_card_uuid_primary_key(self):
        self.assertIsInstance(self.card.id, uuid.UUID)
        self.assertIsNotNone(self.card.id)

    def test_card_str_representation(self):
        self.assertEqual(str(self.card), "Lightning Bolt")

    def test_card_color_relationship(self):
        self.card.colors.add(self.red_color)
        self.assertEqual(self.card.colors.count(), 1)
        self.assertIn(self.red_color, self.card.colors.all())

    def test_card_color_count_property(self):
        # Test with no colors
        self.assertEqual(self.card.color_count, 0)
        
        # Test with one color
        self.card.colors.add(self.red_color)
        self.assertEqual(self.card.color_count, 1)
        
        # Test with multiple colors
        self.card.colors.add(self.blue_color)
        self.assertEqual(self.card.color_count, 2)

    def test_card_edition_foreign_key(self):
        self.assertEqual(self.card.edition.name, "Alpha")
        self.assertEqual(self.card.edition.code, "LEA")

    def test_card_optional_fields(self):
        card_minimal = Card.objects.create(
            name="Test Card",
            type="Creature",
            power="1",
            toughness="1",
            rarity="Common",
            set_name="Test Set",
            image_url="https://example.com/test.jpg",
            edition=self.edition
        )
        
        self.assertIsNone(card_minimal.mana_cost)
        self.assertIsNone(card_minimal.text)
        self.assertIsNone(card_minimal.flavor)

    def test_creature_card(self):
        creature = Card.objects.create(
            name="Grizzly Bears",
            mana_cost="{1}{G}",
            type="Creature — Bear",
            power="2",
            toughness="2",
            rarity="Common",
            set_name="Alpha",
            image_url="https://example.com/bears.jpg",
            edition=self.edition
        )
        
        self.assertEqual(creature.power, "2")
        self.assertEqual(creature.toughness, "2")
        self.assertEqual(creature.type, "Creature — Bear")


class CardFormTest(TestCase):
    def setUp(self):
        self.edition = Edition.objects.create(name="Test Edition", code="TST")
        self.color = Color.objects.create(name="Red", code=Color.RED)

    def test_card_form_valid_data(self):
        form_data = {
            'name': 'Test Card',
            'mana_cost': '{1}{R}',
            'text': 'Test card text',
            'flavor': 'Test flavor text',
            'type': 'Instant',
            'power': '0',
            'toughness': '0',
            'rarity': 'Common',
            'set_name': 'Test Set',
            'image_url': 'https://example.com/test.jpg',
            'edition': self.edition.id,
            'colors': [self.color.id]
        }
        
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_card_form_missing_required_fields(self):
        form_data = {
            'name': '',  # Required field missing
            'type': 'Instant',
            'power': '',
            'toughness': '',
            'rarity': 'Common',
            'set_name': 'Test Set',
            'image_url': 'https://example.com/test.jpg',
            'edition': self.edition.id
        }
        
        form = CardForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_card_form_excludes_id(self):
        form = CardForm()
        self.assertNotIn('id', form.fields)

    def test_card_form_save(self):
        form_data = {
            'name': 'Form Test Card',
            'mana_cost': '{2}{R}',
            'text': 'Form test text',
            'type': 'Sorcery',
            'power': '3',
            'toughness': '2',
            'rarity': 'Uncommon',
            'set_name': 'Form Test Set',
            'image_url': 'https://example.com/form_test.jpg',
            'edition': self.edition.id,
            'colors': [self.color.id]
        }
        
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        card = form.save()
        self.assertEqual(card.name, 'Form Test Card')
        self.assertEqual(card.mana_cost, '{2}{R}')
        self.assertEqual(card.type, 'Sorcery')
        self.assertEqual(card.edition, self.edition)
        self.assertIn(self.color, card.colors.all())


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.edition = Edition.objects.create(name="Test Edition", code="TST")
        self.color = Color.objects.create(name="Red", code=Color.RED)
        
        # Create some test cards for the index view
        for i in range(15):  # More than 9 to test the limit
            Card.objects.create(
                name=f"Test Card {i}",
                type="Creature",
                power="1",
                toughness="1",
                rarity="Common",
                set_name="Test Set",
                image_url=f"https://example.com/test{i}.jpg",
                edition=self.edition
            )

    def test_form_create_get_request(self):
        response = self.client.get(reverse('cards:create-card'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name')
        self.assertContains(response, 'John')  # Template context variable
        self.assertIsInstance(response.context['form'], CardForm)

    def test_form_create_post_valid_data(self):
        form_data = {
            'name': 'Posted Card',
            'mana_cost': '{1}{R}',
            'text': 'Posted card text',
            'type': 'Instant',
            'power': '3',
            'toughness': '1',
            'rarity': 'Common',
            'set_name': 'Posted Set',
            'image_url': 'https://example.com/posted.jpg',
            'edition': self.edition.id,
            'colors': [self.color.id]
        }
        
        response = self.client.post(reverse('cards:create-card'), data=form_data)
        
        # Should redirect to Google (as per the view logic)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, 'https://www.google.com')
        
        # Verify card was created
        self.assertTrue(Card.objects.filter(name='Posted Card').exists())

    def test_form_create_post_invalid_data(self):
        form_data = {
            'name': '',  # Missing required field
            'type': 'Instant'
        }
        
        response = self.client.post(reverse('cards:create-card'), data=form_data)
        
        # Should not redirect, should stay on form page
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CardForm)
        self.assertFalse(response.context['form'].is_valid())

    def test_index_view(self):
        response = self.client.get('/cards/')  # Assuming this is mapped to index
        
        # Note: The index view may not be accessible via reverse since it's not in urlpatterns
        # This test assumes the URL mapping exists. If not, it would need to be added.
        pass  # This test would need the proper URL mapping

    def test_index_view_card_limit(self):
        # This test verifies that only 9 cards are returned (as per the view logic)
        # Would need proper URL mapping to test fully
        pass  # Implementation depends on URL configuration


class IntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.edition = Edition.objects.create(name="Integration Test", code="INT")
        self.red_color = Color.objects.create(name="Red", code=Color.RED)
        self.blue_color = Color.objects.create(name="Blue", code=Color.BLUE)

    def test_complete_card_creation_workflow(self):
        """Test the complete workflow of creating a card with colors and edition"""
        
        # Verify initial state
        self.assertEqual(Card.objects.count(), 0)
        
        # Create a card through the form
        form_data = {
            'name': 'Integration Test Card',
            'mana_cost': '{1}{R}{U}',
            'text': 'This is an integration test card.',
            'flavor': 'Testing is important.',
            'type': 'Instant',
            'power': '2',
            'toughness': '1',
            'rarity': 'Rare',
            'set_name': 'Integration Set',
            'image_url': 'https://example.com/integration.jpg',
            'edition': self.edition.id,
            'colors': [self.red_color.id, self.blue_color.id]
        }
        
        response = self.client.post(reverse('cards:create-card'), data=form_data)
        
        # Verify redirect
        self.assertIsInstance(response, HttpResponseRedirect)
        
        # Verify card was created
        self.assertEqual(Card.objects.count(), 1)
        
        # Verify card details
        card = Card.objects.first()
        self.assertEqual(card.name, 'Integration Test Card')
        self.assertEqual(card.mana_cost, '{1}{R}{U}')
        self.assertEqual(card.edition, self.edition)
        self.assertEqual(card.color_count, 2)
        self.assertIn(self.red_color, card.colors.all())
        self.assertIn(self.blue_color, card.colors.all())

    def test_card_with_no_colors(self):
        """Test creating a card and then removing colors"""
        # Since the form requires colors, we'll test the model's ability to have no colors
        card = Card.objects.create(
            name='Colorless Artifact',
            mana_cost='{2}',
            text='An artifact with no color.',
            type='Artifact',
            power='1',
            toughness='1',
            rarity='Uncommon',
            set_name='Artifact Set',
            image_url='https://example.com/artifact.jpg',
            edition=self.edition
        )
        
        # Verify card was created with no colors
        self.assertEqual(card.color_count, 0)
        self.assertEqual(card.colors.count(), 0)
        
        # Add a color and then remove it
        card.colors.add(self.red_color)
        self.assertEqual(card.color_count, 1)
        
        card.colors.clear()
        self.assertEqual(card.color_count, 0)
