import csv
from django.core.management.base import BaseCommand
from phones.models import Phone

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            ph = Phone(name = phone['name'],
                       image = phone['image'],
                       price = float(phone['price']),
                       release_date = phone['release_date'],
                       lte_exists = phone['lte_exists'],
                       slug = phone['name'].strip().lower().replace(' ', '-')
                       )
            ph.save()

