""" Importing the libraries """
from django.urls import path,include
from .views import IMDbscrapping

""" Url patterns for redirect and perform the particular operation in the our system """
urlpatterns = [
    path('IMDb/', IMDbscrapping.as_view()),
]