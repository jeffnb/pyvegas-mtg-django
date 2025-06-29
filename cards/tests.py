import uuid
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.admin.sites import AdminSite
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from cards.models import Color, Edition, Card
from cards.forms import CardForm
from cards.views import form_create, index
from cards.admin import ColorAdmin, EditionsAdmin, CardAdmin


class ColorModelTest(TestCase):
    """Test cases for Color model"""
    
    def setUp(self):
        self.color = Color.objects.create(name='Red', code='R')
    
    def test_color_creation(self):
        """Test creating a color instance"""
        self.assertEqual(self.color.name, 'Red')
        self.assertEqual(self.color.code, 'R')
        self.assertIsInstance(self.color.id, int)
    
    def test_color_string_representation(self):
        """Test the string representation of color"""
        self.assertEqual(str(self.color), 'Red')
    
    def test_color_choices(self):
        """Test color choices are properly defined"""
        choices = Color.COLOR_CHOICES
        expected_choices = [('R', 'Red'), ('G', 'Green'), ('U', 'Blue'), ('W', 'White'), ('B', 'Black')]
        self.assertEqual(choices, expected_choices)
    
    def test_color_constants(self):
        """Test color constants are properly defined"""
        self.assertEqual(Color.RED, 'R')
        self.assertEqual(Color.GREEN, 'G')
        self.assertEqual(Color.BLUE, 'U')
        self.assertEqual(Color.WHITE, 'W')
        self.assertEqual(Color.BLACK, 'B')
    
    def test_color_code_validation(self):
        """Test color code field validation"""
        color = Color(name='Test', code='R')
        color.full_clean()  # Should not raise ValidationError
        
        # Test invalid choice
        color.code = 'X'
        with self.assertRaises(ValidationError):
            color.full_clean()


class EditionModelTest(TestCase):
    """Test cases for Edition model"""
    
    def setUp(self):
        self.edition1 = Edition.objects.create(name='Alpha', code='LEA')
        self.edition2 = Edition.objects.create(name='Beta', code='LEB')
    
    def test_edition_creation(self):
        """Test creating an edition instance"""
        self.assertEqual(self.edition1.name, 'Alpha')
        self.assertEqual(self.edition1.code, 'LEA')
        self.assertIsInstance(self.edition1.id, int)
    
    def test_edition_string_representation(self):
        """Test the string representation of edition"""
        self.assertEqual(str(self.edition1), 'Alpha(LEA)')
    
    def test_edition_ordering(self):
        """Test that editions are ordered by name"""
        editions = list(Edition.objects.all())
        self.assertEqual(editions[0].name, 'Alpha')
        self.assertEqual(editions[1].name, 'Beta')
    
    def test_edition_fields_max_length(self):
        """Test field max length constraints"""
        # Test name max length
        long_name = 'x' * 101
        edition = Edition(name=long_name, code='TST')
        with self.assertRaises(ValidationError):
            edition.full_clean()
        
        # Test code max length
        long_code = 'xxxx'
        edition = Edition(name='Test', code=long_code)
        with self.assertRaises(ValidationError):
            edition.full_clean()


class CardModelTest(TestCase):
    """Test cases for Card model"""
    
    def setUp(self):
        self.color = Color.objects.create(name='Red', code='R')
        self.edition = Edition.objects.create(name='Alpha', code='LEA')
        self.card = Card.objects.create(
            name='Lightning Bolt',
            mana_cost='{R}',
            text='Lightning Bolt deals 3 damage to any target.',
            flavor='The spark of an idea, the power of a storm.',
            type='Instant',
            power='',
            toughness='',
            rarity='Common',
            set_name='Alpha',
            image_url='https://example.com/lightning_bolt.jpg',
            edition=self.edition
        )
        self.card.colors.add(self.color)
    
    def test_card_creation(self):
        """Test creating a card instance"""
        self.assertEqual(self.card.name, 'Lightning Bolt')
        self.assertEqual(self.card.mana_cost, '{R}')
        self.assertEqual(self.card.type, 'Instant')
        self.assertEqual(self.card.edition, self.edition)
        self.assertIsInstance(self.card.id, uuid.UUID)
    
    def test_card_string_representation(self):
        """Test the string representation of card"""
        self.assertEqual(str(self.card), 'Lightning Bolt')
    
    def test_card_uuid_primary_key(self):
        """Test that card uses UUID as primary key"""
        self.assertIsInstance(self.card.id, uuid.UUID)
        self.assertIsNotNone(self.card.id)
    
    def test_card_color_count_property(self):
        """Test the color_count property"""
        self.assertEqual(self.card.color_count, 1)
        
        # Add another color
        blue_color = Color.objects.create(name='Blue', code='U')
        self.card.colors.add(blue_color)
        self.assertEqual(self.card.color_count, 2)
    
    def test_card_foreign_key_relationship(self):
        """Test foreign key relationship with Edition"""
        self.assertEqual(self.card.edition, self.edition)
        self.assertIn(self.card, self.edition.card_set.all())
    
    def test_card_many_to_many_relationship(self):
        """Test many-to-many relationship with Color"""
        self.assertIn(self.color, self.card.colors.all())
        self.assertIn(self.card, self.color.card_set.all())
    
    def test_card_optional_fields(self):
        """Test that optional fields can be null/blank"""
        card = Card.objects.create(
            name='Test Card',
            type='Creature',
            power='1',
            toughness='1',
            rarity='Common',
            set_name='Test Set',
            image_url='https://example.com/test.jpg',
            edition=self.edition
        )
        self.assertIsNone(card.mana_cost)
        self.assertIsNone(card.text)
        self.assertIsNone(card.flavor)
    
    def test_card_field_max_lengths(self):
        """Test field max length constraints"""
        # Test name max length
        card = Card(
            name='x' * 101,
            type='Creature',
            power='1',
            toughness='1',
            rarity='Common',
            set_name='Test',
            image_url='https://example.com/test.jpg',
            edition=self.edition
        )
        with self.assertRaises(ValidationError):
            card.full_clean()


class CardFormTest(TestCase):
    """Test cases for CardForm"""
    
    def setUp(self):
        self.color = Color.objects.create(name='Red', code='R')
        self.edition = Edition.objects.create(name='Alpha', code='LEA')
    
    def test_form_is_model_form(self):
        """Test that CardForm is a ModelForm"""
        form = CardForm()
        self.assertIsInstance(form, ModelForm)
    
    def test_form_excludes_id_field(self):
        """Test that form excludes id field"""
        form = CardForm()
        self.assertNotIn('id', form.fields)
    
    def test_form_includes_required_fields(self):
        """Test that form includes all required fields except id"""
        form = CardForm()
        expected_fields = [
            'name', 'mana_cost', 'text', 'flavor', 'type', 
            'power', 'toughness', 'rarity', 'set_name', 
            'image_url', 'edition', 'colors'
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)
    
    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'name': 'Test Card',
            'mana_cost': '{1}{R}',
            'text': 'Test card text',
            'type': 'Creature',
            'power': '2',
            'toughness': '1',
            'rarity': 'Common',
            'set_name': 'Test Set',
            'image_url': 'https://example.com/test.jpg',
            'edition': self.edition.id,
            'colors': [self.color.id]
        }
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_data(self):
        """Test form with invalid data"""
        form_data = {
            'name': '',  # Required field is empty
            'type': 'Creature',
            'power': '2',
            'toughness': '1',
            'rarity': 'Common',
            'set_name': 'Test Set',
            'image_url': 'invalid-url',  # Invalid URL
            'edition': self.edition.id
        }
        form = CardForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('image_url', form.errors)
    
    def test_form_save(self):
        """Test form save functionality"""
        form_data = {
            'name': 'Test Card',
            'type': 'Creature',
            'power': '2',
            'toughness': '1',
            'rarity': 'Common',
            'set_name': 'Test Set',
            'image_url': 'https://example.com/test.jpg',
            'edition': self.edition.id,
            'colors': [self.color.id]
        }
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        card = form.save()
        self.assertEqual(card.name, 'Test Card')
        self.assertEqual(card.edition, self.edition)
        self.assertTrue(Card.objects.filter(name='Test Card').exists())


class ViewTest(TestCase):
    """Test cases for views"""
    
    def setUp(self):
        self.client = Client()
        self.color = Color.objects.create(name='Red', code='R')
        self.edition = Edition.objects.create(name='Alpha', code='LEA')
    
    def test_form_create_get_request(self):
        """Test GET request to form_create view"""
        response = self.client.get(reverse('cards:create-card'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')
        self.assertContains(response, 'form')
        self.assertIsInstance(response.context['form'], CardForm)
        self.assertEqual(response.context['name'], 'John')
        self.assertTemplateUsed(response, 'cards/card_create.html')
    
    def test_form_create_post_valid_data(self):
        """Test POST request to form_create view with valid data"""
        form_data = {
            'name': 'Test Card',
            'type': 'Creature',
            'power': '2',
            'toughness': '1',
            'rarity': 'Common',
            'set_name': 'Test Set',
            'image_url': 'https://example.com/test.jpg',
            'edition': self.edition.id,
            'colors': [self.color.id]
        }
        response = self.client.post(reverse('cards:create-card'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://www.google.com')
        self.assertTrue(Card.objects.filter(name='Test Card').exists())
    
    def test_form_create_post_invalid_data(self):
        """Test POST request to form_create view with invalid data"""
        form_data = {
            'name': '',  # Required field is empty
            'type': 'Creature'
        }
        response = self.client.post(reverse('cards:create-card'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertFalse(response.context['form'].is_valid())
        self.assertTemplateUsed(response, 'cards/card_create.html')
    
    def test_index_view(self):
        """Test index view"""
        # Create some test cards
        for i in range(15):
            Card.objects.create(
                name=f'Card {i}',
                type='Creature',
                power='1',
                toughness='1',
                rarity='Common',
                set_name='Test Set',
                image_url=f'https://example.com/card{i}.jpg',
                edition=self.edition
            )
        
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/index.html')
        
        # Should return 9 random cards
        cards = response.context['cards']
        self.assertEqual(len(cards), 9)
        
        # All cards should be Card instances
        for card in cards:
            self.assertIsInstance(card, Card)
        
        # Check that the response contains card names in the rendered content
        response_content = response.content.decode()
        # At least one card name should be in the response
        card_names_in_response = [f'Card {i}' for i in range(15) if f'Card {i}' in response_content]
        self.assertGreater(len(card_names_in_response), 0)
    
    def test_index_view_with_no_cards(self):
        """Test index view when no cards exist"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cards']), 0)


class URLTest(TestCase):
    """Test cases for URL routing"""
    
    def test_cards_create_url_resolves(self):
        """Test that cards create URL resolves to correct view"""
        url = reverse('cards:create-card')
        self.assertEqual(resolve(url).func, form_create)
    
    def test_index_url_resolves(self):
        """Test that index URL resolves to correct view"""
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)
    
    def test_cards_create_url_pattern(self):
        """Test cards create URL pattern"""
        url = reverse('cards:create-card')
        self.assertEqual(url, '/cards/')
    
    def test_index_url_pattern(self):
        """Test index URL pattern"""
        url = reverse('index')
        self.assertEqual(url, '/')


class AdminTest(TestCase):
    """Test cases for admin configuration"""
    
    def setUp(self):
        self.site = AdminSite()
        self.color = Color.objects.create(name='Red', code='R')
        self.edition = Edition.objects.create(name='Alpha', code='LEA')
        self.card = Card.objects.create(
            name='Test Card',
            type='Creature',
            power='2',
            toughness='1',
            rarity='Common',
            set_name='Test Set',
            image_url='https://example.com/test.jpg',
            edition=self.edition
        )
    
    def test_color_admin_configuration(self):
        """Test ColorAdmin configuration"""
        admin = ColorAdmin(Color, self.site)
        self.assertEqual(admin.list_display, ('name', 'code'))
    
    def test_edition_admin_configuration(self):
        """Test EditionsAdmin configuration"""
        admin = EditionsAdmin(Edition, self.site)
        self.assertEqual(admin.list_display, ('name', 'code'))
    
    def test_card_admin_configuration(self):
        """Test CardAdmin configuration"""
        admin = CardAdmin(Card, self.site)
        expected_list_display = ['name', 'edition', 'rarity', 'type', 'power', 'toughness']
        expected_list_filter = ['edition', 'rarity', 'type']
        expected_search_fields = ['name', 'edition', 'rarity', 'type', 'text']
        expected_ordering = ['name']
        
        self.assertEqual(admin.list_display, expected_list_display)
        self.assertEqual(admin.list_filter, expected_list_filter)
        self.assertEqual(admin.search_fields, expected_search_fields)
        self.assertEqual(admin.ordering, expected_ordering)
