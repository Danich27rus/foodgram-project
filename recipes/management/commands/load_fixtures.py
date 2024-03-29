import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Product, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):

        file_path = os.path.join(settings.BASE_DIR,
                                 'recipes/fixtures', 'ingredients.csv')

        with open(file_path) as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Product.objects.get_or_create(
                    title=row[0],
                    dimension=row[1],
                )
            f.close()

        file_path = os.path.join(settings.BASE_DIR,
                                 'recipes/fixtures', 'tags.csv')

        with open(file_path) as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Tag.objects.get_or_create(
                    name=row[0],
                    color=row[1],
                    color_slug=row[2],
                    slug=row[3]
                )
            f.close()
