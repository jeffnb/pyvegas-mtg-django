from django.test import TestCase, Client
from django.urls import reverse
from cards.models import Card, Edition, Color
from cards.forms import CardForm

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        
        # Create test data
        self.edition = Edition.objects.create(name='Test Edition', code='TST')
        self.color = Color.objects.create(name='Red', code=Color.RED)
        
        # Create 10 cards to test the random selection
        for i in range(10):
            card = Card.objects.create(
                name=f'Test Card {i}',
                mana_cost='{1}{R}',
                text=f'Test card text {i}',
                type='Creature',
                power='2',
                toughness='2',
                rarity='Common',
                set_name='Test Set',
                image_url=f'https://example.com/image{i}.jpg',
                edition=self.edition
            )
            card.colors.add(self.color)
    
    def test_index_view_get(self):
        """Test that the index view returns a 200 response and uses the correct template"""
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/index.html')
    
    def test_index_view_context(self):
        """Test that the index view provides cards in the context"""
        response = self.client.get(self.index_url)
        self.assertTrue('cards' in response.context)
        self.assertEqual(len(response.context['cards']), 9)  # Should show 9 random cards

class FormCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('cards:create-card')
        self.edition = Edition.objects.create(name='Test Edition', code='TST')
        self.color = Color.objects.create(name='Red', code=Color.RED)
    
    def test_form_create_view_get(self):
        """Test that the form_create view returns a 200 response and uses the correct template"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_create.html')
        self.assertTrue('form' in response.context)
        self.assertIsInstance(response.context['form'], CardForm)
        self.assertEqual(response.context['name'], 'John')  # Check the hardcoded context variable
    
    def test_form_create_view_post_valid(self):
        """Test that a valid POST request creates a card and redirects"""
        card_count_before = Card.objects.count()
        
        # Create valid form data
        form_data = {
            'name': 'New Test Card',
            'mana_cost': '{2}{R}',
            'text': 'New test card text',
            'flavor': 'New test flavor text',
            'type': 'Creature — Beast',
            'power': '3',
            'toughness': '3',
            'rarity': 'Uncommon',
            'set_name': 'Test Set',
            'image_url': 'https://example.com/new_image.jpg',
            'edition': self.edition.id,
            'colors': [self.color.id]
        }
        
        response = self.client.post(self.create_url, form_data)
        
        # Check that the card was created
        self.assertEqual(Card.objects.count(), card_count_before + 1)
        
        # Check that we were redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://www.google.com')
        
        # Check that the card has the correct data
        new_card = Card.objects.latest('id')
        self.assertEqual(new_card.name, 'New Test Card')
        self.assertEqual(new_card.mana_cost, '{2}{R}')
        self.assertEqual(new_card.colors.first(), self.color)
    
    def test_form_create_view_post_invalid(self):
        """Test that an invalid POST request returns the form with errors"""
        card_count_before = Card.objects.count()
        
        # Create invalid form data (missing required fields)
        form_data = {
            'name': '',  # Name is required
            'mana_cost': '{2}{R}',
            'text': 'New test card text',
        }
        
        response = self.client.post(self.create_url, form_data)
        
        # Check that no card was created
        self.assertEqual(Card.objects.count(), card_count_before)
        
        # Check that we're still on the form page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/card_create.html')
        
        # Check that the form has errors
        self.assertTrue(response.context['form'].errors)