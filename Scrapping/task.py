""" Import Libraries """
from celery import shared_task
import os
from .models import IMDbScrapping

@shared_task()
def bakcgroung_scrapping():
    """ this function will run your task into the background process """
    os.system('python manage.py crawl')

@shared_task()
def download_image(obj_id):
    obj = IMDbScrapping.objects.get(id=obj_id)
    obj.save()