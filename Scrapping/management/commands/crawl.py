""" Importing Libraries """
from django.core.management.base import BaseCommand
import os
from pathlib import Path


class Command(BaseCommand):
    """
    this class going to extract the data from given website into spider
    """
    help = "Release the spiders"

    # def add_arguments(self, parser):
    #     parser.add_argument('category', type=str, help="Name of the category")

    def handle(self, *args, **options):
        """
        this function will go to handel the request and scraped data from given website
        :return: it will return scraped data from the website
        """
        django_path = Path(__file__).resolve().parent.parent.parent.parent

        os.chdir(str(django_path) + "/Imdbscraper")
        os.system("scrapy crawl imdb_spider")