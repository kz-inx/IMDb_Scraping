""" Import libraries """
from .task import bakcgroung_scrapping
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import Complex_IMDb
from .models import IMDbScrapping
from django.db.models import Q, Avg, Max, Min, Count
from rest_framework.views import APIView


class IMDbscrapping(ListAPIView):
    """
    to call this class from urls and hit API
    """

    def get(self, request):
        """
        This function will when api hit it will go task file call that function
        :param request: it will going the request task function for scrapping the data
        :return: it will return the msg of success in the form the json to end user
        """
        bakcgroung_scrapping.delay()
        return Response({'status': 'pass', 'msg': 'successfully data scraped'}, status=status.HTTP_200_OK)


class movie_recommendation(ListAPIView):
    """
    Field lookups in django orm it provide us check particular data into the database
    we can use many function like startswith, endswith, extract, gt, gte,lt,lte, etc....
    """
    serializer_class = Complex_IMDb

    def get_queryset(self):
        queryset = IMDbScrapping.objects.filter(name__endswith='Top Gun: Maverick')
        return queryset


class movie_search(ListAPIView):
    """
    In Django orm it provides us complex lookups with Q. Where we can or condition in the filter for the data,
    take out the that data from the database. As you can see below exg in which we have applied the Q for OR Condition.
    """
    serializer_class = Complex_IMDb

    def get_queryset(self):
        queryset = IMDbScrapping.objects.filter(Q(rating__gt=8.5) | Q(runtime__lte=110))
        return queryset


class aggreate_rating(APIView):
    """
    Aggregate provide us take out the min, max, avg, count with the database. We can also implement the Aggreate with the using with filtet
    As you show the below examples are given the calculate the different fields
    """
    serializer_class = Complex_IMDb

    def get(self, request):
        # queryset = IMDbScrapping.objects.aggregate(Min('rating'), Max('rating'))
        # queryset = IMDbScrapping.objects.aggregate(Min('vote'), Max('vote'))
        queryset = IMDbScrapping.objects.filter(runtime__lte=120).aggregate(Min('vote'), Max('vote'))
        # queryset = IMDbScrapping.objects.annotate(Count('vote'))
        # s = Complex_IMDb(instance=queryset, many=True)
        return Response(queryset)


class limit_records(ListAPIView):
    """
    the limit records we are going to show the user sometimes. There lacks of records are available into the our the system,
    but we need show limit numbers of records to the user we can do this using the slicing after query
    In this only positive integer values should given, it will not work for the negative value
    """
    serializer_class = Complex_IMDb
    def get_queryset(self):
        # entry object will not support the negative index , it required only positive integer
        queryset = IMDbScrapping.objects.filter(rating__gt=7.9, runtime__gte=90)[:15]
        return queryset


class retrving_records(APIView):
    serializer_class = Complex_IMDb

    # queryset = IMDbScrapping.objects.all()
    def get(self, request):
        try:
            queryset = IMDbScrapping.objects.get(id=12005)
            serialzier = Complex_IMDb(instance=queryset)
            return Response(serialzier.data)
        except:
            return Response({'msg': "data not found"}, status=status.HTTP_404_NOT_FOUND)


class delte_objects(APIView):
    serializer_class = Complex_IMDb
    # queryset = IMDbScrapping.objects.all()
    def delete(self, request):
        try:
            IMDbScrapping.objects.get(id=12005).delete()
            return Response({'msg': "Done"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'msg': "data not found"}, status=status.HTTP_404_NOT_FOUND)

class comparing_objects(APIView):
    serializer_class = Complex_IMDb
    def get(self,request):
        queryset = IMDbScrapping.objects.select_related().all()
        serializer = Complex_IMDb(instance=queryset, many=True)
        return Response(serializer.data)

class prefetch_objects(APIView):
    serializer_class = Complex_IMDb
    def get(self,request):
        queryset = IMDbScrapping.objects.prefetch_related().all()
        serializer = Complex_IMDb(instance=queryset, many=True)
        return Response(serializer.data)


