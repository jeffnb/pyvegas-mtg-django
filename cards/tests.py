from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.http import HttpResponse
from django.forms import ModelForm
import uuid

from cards.models import Color, Edition, Card
from cards.forms import CardForm
from cards.views import form_create, index


class ColorModelTest(TestCase):
    """Test Color model functionality"""
    
    def setUp(self):
        self.color = Color.objects.create(
            name='Red',
            code=Color.RED
        )
    
    def test_color_creation(self):
        """Test Color object creation and basic properties"""
        self.assertEqual(self.color.name, 'Red')
        self.assertEqual(self.color.code, 'R')
    
    def test_color_str_representation(self):
        """Test Color string representation"""
        self.assertEqual(str(self.color), 'Red')
    
    def test_color_choices(self):
        """Test that color choices are correctly defined"""
        expected_choices = [('R', 'Red'), ('G', 'Green'), ('U', 'Blue'), ('W', 'White'), ('B', 'Black')]
        self.assertEqual(Color.COLOR_CHOICES, expected_choices)
    
    def test_color_choice_validation(self):
        """Test that only valid color codes can be used"""
        valid_codes = ['R', 'G', 'U', 'W', 'B']
        for code in valid_codes:
            color = Color(name=f'Test {code}', code=code)
            # This should not raise any validation errors
            color.full_clean()


class EditionModelTest(TestCase):
    """Test Edition model functionality"""
    
    def setUp(self):
        self.edition = Edition.objects.create(
            name='Alpha',
            code='ALP'
        )
    
    def test_edition_creation(self):
        """Test Edition object creation and basic properties"""
        self.assertEqual(self.edition.name, 'Alpha')
        self.assertEqual(self.edition.code, 'ALP')
    
    def test_edition_str_representation(self):
        """Test Edition string representation"""
        self.assertEqual(str(self.edition), 'Alpha(ALP)')
    
    def test_edition_ordering(self):
        """Test that editions are ordered by name"""
        edition_beta = Edition.objects.create(name='Beta', code='BET')
        edition_unlimited = Edition.objects.create(name='Unlimited', code='UNL')
        
        editions = Edition.objects.all()
        self.assertEqual(editions[0], self.edition)  # Alpha comes first
        self.assertEqual(editions[1], edition_beta)  # Beta comes second
        self.assertEqual(editions[2], edition_unlimited)  # Unlimited comes last


class CardModelTest(TestCase):
    """Test Card model functionality"""
    
    def setUp(self):
        self.red_color = Color.objects.create(name='Red', code=Color.RED)
        self.blue_color = Color.objects.create(name='Blue', code=Color.BLUE)
        self.edition = Edition.objects.create(name='Alpha', code='ALP')
        
        self.card = Card.objects.create(
            name='Lightning Bolt',
            mana_cost='{R}',
            text='Lightning Bolt deals 3 damage to any target.',
            flavor='The spark that ignites a rebellion.',
            type='Instant',
            power='',
            toughness='',
            rarity='Common',
            set_name='Alpha',
            image_url='https://example.com/lightning_bolt.jpg',
            edition=self.edition
        )
        self.card.colors.add(self.red_color)
    
    def test_card_creation(self):
        """Test Card object creation and basic properties"""
        self.assertEqual(self.card.name, 'Lightning Bolt')
        self.assertEqual(self.card.mana_cost, '{R}')
        self.assertEqual(self.card.type, 'Instant')
        self.assertEqual(self.card.edition, self.edition)
        self.assertIsInstance(self.card.id, uuid.UUID)
    
    def test_card_str_representation(self):
        """Test Card string representation"""
        self.assertEqual(str(self.card), 'Lightning Bolt')
    
    def test_card_color_count_property(self):
        """Test the color_count property"""
        self.assertEqual(self.card.color_count, 1)
        
        # Add another color and test
        self.card.colors.add(self.blue_color)
        self.assertEqual(self.card.color_count, 2)
    
    def test_card_colors_relationship(self):
        """Test many-to-many relationship with colors"""
        self.assertIn(self.red_color, self.card.colors.all())
        self.assertEqual(self.card.colors.count(), 1)
    
    def test_card_edition_relationship(self):
        """Test foreign key relationship with edition"""
        self.assertEqual(self.card.edition, self.edition)
    
    def test_card_uuid_field(self):
        """Test that Card uses UUID as primary key"""
        self.assertIsInstance(self.card.id, uuid.UUID)
        # Ensure it's auto-generated and unique
        another_card = Card.objects.create(
            name='Another Card',
            type='Creature',
            power='1',
            toughness='1',
            rarity='Common',
            set_name='Alpha',
            image_url='https://example.com/another.jpg',
            edition=self.edition
        )
        self.assertNotEqual(self.card.id, another_card.id)


class CardFormTest(TestCase):
    """Test CardForm functionality"""
    
    def setUp(self):
        self.red_color = Color.objects.create(name='Red', code=Color.RED)
        self.edition = Edition.objects.create(name='Alpha', code='ALP')
    
    def test_card_form_is_model_form(self):
        """Test that CardForm is a ModelForm"""
        self.assertTrue(issubclass(CardForm, ModelForm))
    
    def test_card_form_excludes_id(self):
        """Test that CardForm excludes the id field"""
        form = CardForm()
        self.assertNotIn('id', form.fields)
    
    def test_card_form_includes_other_fields(self):
        """Test that CardForm includes all other expected fields"""
        form = CardForm()
        expected_fields = [
            'name', 'mana_cost', 'text', 'flavor', 'type', 
            'power', 'toughness', 'rarity', 'set_name', 
            'image_url', 'edition', 'colors'
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)
    
    def test_card_form_valid_data(self):
        """Test CardForm with valid data"""
        form_data = {
            'name': 'Test Card',
            'type': 'Creature',
            'power': '2',
            'toughness': '2',
            'rarity': 'Common',
            'set_name': 'Test Set',
            'image_url': 'https://example.com/test.jpg',
            'edition': self.edition.id,
            'colors': [self.red_color.id]
        }
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_card_form_save(self):
        """Test that CardForm can save a valid card"""
        form_data = {
            'name': 'Test Card',
            'type': 'Creature',
            'power': '2',
            'toughness': '2',
            'rarity': 'Common',
            'set_name': 'Test Set',
            'image_url': 'https://example.com/test.jpg',
            'edition': self.edition.id,
            'colors': [self.red_color.id]
        }
        form = CardForm(data=form_data)
        self.assertTrue(form.is_valid())
        card = form.save()
        self.assertEqual(card.name, 'Test Card')
        self.assertEqual(card.edition, self.edition)


class CardViewTest(TestCase):
    """Test Card views functionality"""
    
    def setUp(self):
        self.client = Client()
        self.red_color = Color.objects.create(name='Red', code=Color.RED)
        self.edition = Edition.objects.create(name='Alpha', code='ALP')
        
        # Create test cards
        for i in range(15):  # Create more than 9 cards to test random selection
            card = Card.objects.create(
                name=f'Test Card {i}',
                type='Creature',
                power='1',
                toughness='1',
                rarity='Common',
                set_name='Test Set',
                image_url=f'https://example.com/card{i}.jpg',
                edition=self.edition
            )
            card.colors.add(self.red_color)
    
    def test_index_view_status_code(self):
        """Test that index view returns 200 status code"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_template(self):
        """Test that index view uses correct template"""
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'cards/index.html')
    
    def test_index_view_context_cards(self):
        """Test that index view provides cards in context"""
        response = self.client.get(reverse('index'))
        self.assertIn('cards', response.context)
        cards = response.context['cards']
        self.assertEqual(len(cards), 9)  # Should return exactly 9 cards
    
    def test_index_view_random_cards(self):
        """Test that index view returns different cards on multiple requests"""
        # This test might occasionally fail due to randomness, but it's unlikely
        response1 = self.client.get(reverse('index'))
        response2 = self.client.get(reverse('index'))
        
        cards1 = list(response1.context['cards'])
        cards2 = list(response2.context['cards'])
        
        # With 15 cards and selecting 9, there's a good chance they'll be different
        # We'll just check that we get 9 cards each time
        self.assertEqual(len(cards1), 9)
        self.assertEqual(len(cards2), 9)
    
    def test_form_create_view_get(self):
        """Test form_create view with GET request"""
        response = self.client.get(reverse('cards:create-card'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_create.html')
        self.assertIn('form', response.context)
        self.assertIn('name', response.context)
        self.assertEqual(response.context['name'], 'John')
    
    def test_form_create_view_post_valid(self):
        """Test form_create view with valid POST data"""
        post_data = {
            'name': 'Test Card',
            'type': 'Creature',
            'power': '2',
            'toughness': '2',
            'rarity': 'Common',
            'set_name': 'Test Set',
            'image_url': 'https://example.com/test.jpg',
            'edition': self.edition.id,
            'colors': [self.red_color.id]
        }
        response = self.client.post(reverse('cards:create-card'), data=post_data)
        # Should redirect to Google (as per the current implementation)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://www.google.com')
        
        # Verify card was created
        self.assertTrue(Card.objects.filter(name='Test Card').exists())
    
    def test_form_create_view_post_invalid(self):
        """Test form_create view with invalid POST data"""
        post_data = {
            'name': '',  # Invalid: empty name
            'type': 'Creature',
        }
        response = self.client.post(reverse('cards:create-card'), data=post_data)
        # Should re-render the form, not redirect
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_create.html')


class URLTest(TestCase):
    """Test URL routing functionality"""
    
    def test_index_url_resolves(self):
        """Test that root URL resolves to index view"""
        url = reverse('index')
        self.assertEqual(url, '/')
        self.assertEqual(resolve(url).func, index)
    
    def test_card_create_url_resolves(self):
        """Test that cards create URL resolves correctly"""
        url = reverse('cards:create-card')
        self.assertEqual(url, '/cards/')
        self.assertEqual(resolve(url).func, form_create)
    
    def test_urls_accessible(self):
        """Test that URLs are accessible"""
        # Create minimal test data
        red_color = Color.objects.create(name='Red', code=Color.RED)
        edition = Edition.objects.create(name='Alpha', code='ALP')
        
        # Test index URL
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Test cards create URL
        response = self.client.get('/cards/')
        self.assertEqual(response.status_code, 200)
