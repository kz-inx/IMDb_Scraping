from django.db import models

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
