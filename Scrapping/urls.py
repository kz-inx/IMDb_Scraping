""" Importing the libraries """
from django.urls import path,include
from .views import IMDbScrap,MovieRecommendation, MovieSearch, AggreateRating, LimitRecords, \
    ReturnRecords,DeleteObjects, SelectObjects, PrefetchObjects, FieldCompareModels, BulkUpdateView

""" Url patterns for redirect and perform the particular operation in the our system """
urlpatterns = [
    path('IMDb/', IMDbScrap.as_view()),
    path('watch/', MovieRecommendation.as_view()),
    path('search/', MovieSearch.as_view()),
    path('avg/', AggreateRating.as_view()),
    path('limit/', LimitRecords.as_view()),
    path('ret/', ReturnRecords.as_view()),
    path('delete/', DeleteObjects.as_view()),
    path('select/', SelectObjects.as_view()),
    path('prefetch/', PrefetchObjects.as_view()),
    path('fields/', FieldCompareModels.as_view()),
    path('update/', BulkUpdateView.as_view())

]