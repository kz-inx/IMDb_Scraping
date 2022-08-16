""" Importing the libraries """
from django.urls import path,include
from .views import IMDbscrapping,movie_recommendation, movie_search, aggreate_rating, limit_records, \
    retrving_records,delte_objects, comparing_objects, prefetch_objects

""" Url patterns for redirect and perform the particular operation in the our system """
urlpatterns = [
    path('IMDb/', IMDbscrapping.as_view()),
    path('watch/', movie_recommendation.as_view()),
    path('search/',movie_search.as_view()),
    path('avg/',aggreate_rating.as_view()),
    path('limit/',limit_records.as_view()),
    path('ret/', retrving_records.as_view()),
    path('delete/', delte_objects.as_view()),
    path('select/',comparing_objects.as_view()),
    path('prefetch/', prefetch_objects.as_view())

]