# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from Scrapping.models import IMDbScrapping

class ImdbscraperItem(DjangoItem):
    django_model = IMDbScrapping


