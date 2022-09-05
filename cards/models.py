import uuid

from django.db import models

class Color(models.Model):
    RED = 'R'
    GREEN = 'G'
    BLUE = 'U'
    WHITE = 'W'
    BLACK = 'B'
    COLOR_CHOICES = [(RED, 'Red'), (GREEN, 'Green'), (BLUE, 'Blue'), (WHITE, 'White'), (BLACK, 'Black')]

    name = models.CharField(max_length=20)
    code = models.CharField(max_length=3, choices=COLOR_CHOICES)

    def __str__(self):
        return self.name

class Edition(models.Model):
    """
    These are constantly added to so we won't lock them into choice fields
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.name}({self.code})"

    class Meta:
        ordering = ['name']


class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    mana_cost = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    flavor = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100)
    power = models.CharField(max_length=5)
    toughness = models.CharField(max_length=5)
    rarity = models.CharField(max_length=20)
    set_name = models.CharField(max_length=50)
    image_url = models.URLField(max_length=300)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    colors = models.ManyToManyField(Color)

    @property
    def color_count(self):
        return self.colors.count()


    def __str__(self):
        return self.name