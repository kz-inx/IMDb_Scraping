# IMDB Scrapping

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
* ```

## General Settings 
## Scrapy Settings 
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
```console

```