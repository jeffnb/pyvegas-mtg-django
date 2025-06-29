from django.test import TestCase
from cards.models import Color, Edition, Card

class ColorModelTest(TestCase):
    def setUp(self):
        self.color = Color.objects.create(name='Red', code=Color.RED)
    
    def test_color_creation(self):
        """Test that a color can be created with correct attributes"""
        self.assertEqual(self.color.name, 'Red')
        self.assertEqual(self.color.code, 'R')
    
    def test_color_str(self):
        """Test the string representation of a color"""
        self.assertEqual(str(self.color), 'Red')

class EditionModelTest(TestCase):
    def setUp(self):
        self.edition = Edition.objects.create(name='Core Set 2021', code='M21')
    
    def test_edition_creation(self):
        """Test that an edition can be created with correct attributes"""
        self.assertEqual(self.edition.name, 'Core Set 2021')
        self.assertEqual(self.edition.code, 'M21')
    
    def test_edition_str(self):
        """Test the string representation of an edition"""
        self.assertEqual(str(self.edition), 'Core Set 2021(M21)')
    
    def test_edition_ordering(self):
        """Test that editions are ordered by name"""
        Edition.objects.create(name='Zendikar Rising', code='ZNR')
        editions = Edition.objects.all()
        self.assertEqual(editions[0].name, 'Core Set 2021')
        self.assertEqual(editions[1].name, 'Zendikar Rising')

class CardModelTest(TestCase):
    def setUp(self):
        self.edition = Edition.objects.create(name='Core Set 2021', code='M21')
        self.card = Card.objects.create(
            name='Test Card',
            mana_cost='{1}{R}',
            text='Test card text',
            flavor='Test flavor text',
            type='Creature — Human Wizard',
            power='2',
            toughness='1',
            rarity='Rare',
            set_name='Core Set 2021',
            image_url='https://example.com/image.jpg',
            edition=self.edition
        )
        self.red = Color.objects.create(name='Red', code=Color.RED)
        self.blue = Color.objects.create(name='Blue', code=Color.BLUE)
        self.card.colors.add(self.red, self.blue)
    
    def test_card_creation(self):
        """Test that a card can be created with correct attributes"""
        self.assertEqual(self.card.name, 'Test Card')
        self.assertEqual(self.card.mana_cost, '{1}{R}')
        self.assertEqual(self.card.text, 'Test card text')
        self.assertEqual(self.card.flavor, 'Test flavor text')
        self.assertEqual(self.card.type, 'Creature — Human Wizard')
        self.assertEqual(self.card.power, '2')
        self.assertEqual(self.card.toughness, '1')
        self.assertEqual(self.card.rarity, 'Rare')
        self.assertEqual(self.card.set_name, 'Core Set 2021')
        self.assertEqual(self.card.image_url, 'https://example.com/image.jpg')
        self.assertEqual(self.card.edition, self.edition)
    
    def test_card_colors(self):
        """Test that colors can be added to a card"""
        self.assertEqual(self.card.colors.count(), 2)
        self.assertIn(self.red, self.card.colors.all())
        self.assertIn(self.blue, self.card.colors.all())
    
    def test_color_count_property(self):
        """Test the color_count property"""
        self.assertEqual(self.card.color_count, 2)
    
    def test_card_str(self):
        """Test the string representation of a card"""
        self.assertEqual(str(self.card), 'Test Card')