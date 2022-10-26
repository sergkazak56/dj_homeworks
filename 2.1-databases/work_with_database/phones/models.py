from django.db import models
from datetime import date

class Phone(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.URLField(max_length=200)
    price = models.FloatField()
    release_date = models.DateField(default=date.today())
    lte_exists = models.BooleanField(default=True)
    slug = models.SlugField(max_length=50, db_index=True)
