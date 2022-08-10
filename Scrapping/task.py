""" Import Libraries """
from celery import shared_task
import os

@shared_task()
def bakcgroung_scrapping():
    """ this function will run your task into the background process """
    os.system('python manage.py crawl')