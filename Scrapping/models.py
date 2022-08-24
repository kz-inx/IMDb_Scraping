import os
import uuid
from urllib.parse import urlparse


import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.utils.text import slugify


# Create your models here.

class IMDbScrapping(models.Model):
    """
    Creating the filed for store data into our database
    """
    name = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    rating = models.CharField(max_length=300)
    description = models.TextField()
    amount = models.CharField(max_length=100, null=True)
    year = models.CharField(max_length=200)
    runtime = models.CharField(max_length=100)
    categories = models.CharField(max_length=300)
    vote = models.CharField(max_length=300)
    image_file = models.ImageField(upload_to='images', null=True)
    image_urls = models.URLField(default=None, null=True)

    def __str__(self):
        return str(self.name)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.image_urls and not self.image_file:
            # print('>>>>>', self.image_urls)
            r = requests.get(self.image_urls)

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(r.content)
            img_temp.flush()
            name = urlparse(self.image_urls)
            extension = os.path.basename(name.path).split('.')[-1]
            # self.image_file.save(f"{os.path.basename(name.path)}", File(img_temp)
            self.image_file.save(f"{self.id}.{extension}", File(img_temp))

        super(IMDbScrapping, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

