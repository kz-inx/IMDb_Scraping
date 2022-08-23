# IMDB Scrapping <img src="https://github.com/kz-inx/IMDb_Scraping/blob/main/imdb.jpg" width="45">

Scrapping the IMDB website using the scrapy, creating the endpoint for run this scrapping using the DRF(Django Rest Farmework)
<br/>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
## Requirements 
* Python 
* pycharm 
* PostgresSql 
* Postman

## Installation 
```python
pip install djangorestframework
pip install scrapy
```
See the install of Scrapy  section in the documentation at
https://docs.scrapy.org/en/latest/intro/install.html for more details.

See the install of Django Restframework section in the documentation at
https://www.django-rest-framework.org/ for more details.

## Start your Project 
* Use this following commands to start the DRF and Scrapy 
``` python
django-admin startproject Project name 
# create a new app in the django 
python manage.py startapp App name 
scrapy startproject Project name 
# create spider in the scrapy 
scrapy genspider spider_name specify url 
```

## General Settings 
### Scrapy Settings 
* ### Install Libraries Proxy settings 
```python
pip install scrapy_proxy_pool
pip install scrapy-user-agents
```
```console
# Add this in settings.py of scrapy 
PROXY_POOL_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
    'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,

}

# uncomment this pipline code. It help save your data into the database 

ITEM_PIPELINES = {
   'Imdbscraper.pipelines.ImdbscraperPipeline': 300,
}

# Django Integration with the scrapy 


# Django project root level path
django_path = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(django_path)+"/")

os.environ['DJANGO_SETTINGS_MODULE'] = 'ImdbScrapping.settings'
django.setup()
```

## Django Settings 
### Install Libraries
```python
pip install celery
sudo apt install redis-server
```
See the install of redis  section in the documentation at
https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04 for more details.

```console
----------------------------------------------------------------------------------------------
# Add rest faremwork the into your installled apps in the settings,py file 
----------------------------------------------------------------------------------------------
INSTALLED_APPS = [
   '''
    'rest_framework',
    'Add App name you create',
   '''
], 
----------------------------------------------------------------------------------------------
# give your creadnitals for this database integration 
----------------------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'PORT': os.environ.get('DB_PORT'),
        'HOST': os.environ.get('DB_HOST')
    }
},
----------------------------------------------------------------------------------------------
#celery settings add 
----------------------------------------------------------------------------------------------
# Integration celery filed with django
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

```
## Creating the crawl  file
```python
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
```

## Custom command to run Scrapy 
` python manage.py crawl `
* Creating task.py for schedule task in the system 
```python
""" Import Libraries """
from celery import shared_task
import os

@shared_task()
def bakcgroung_scrapping():
    """ this function will run your task into the background process """
    os.system('python manage.py crawl')
```
## Development 

#### Migrations changes 
```python
$ python manage.py makemigrations 
$ python maange.py migrate 
```

#### Running Server 
```python
$ redis-server
$ celery -A ImdbScrapping worker -l INFO 
$ python manage.py runserver 
```
