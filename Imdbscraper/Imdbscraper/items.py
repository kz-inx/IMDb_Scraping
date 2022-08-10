# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
""" Importing Libraries """

import scrapy
from scrapy_djangoitem import DjangoItem
from Scrapping.models import IMDbScrapping

class ImdbscraperItem(DjangoItem):
    """ this class will go to perform save data into your database..."""
    django_model = IMDbScrapping


