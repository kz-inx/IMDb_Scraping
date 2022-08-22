""" Import libraries """
from .task import bakcgroung_scrapping
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import Complex_IMDb,bulk_update
from .models import IMDbScrapping
from django.db.models import Q, Avg, Max, Min, F
from rest_framework.views import APIView


class IMDbscrapping(ListAPIView):
    """
    to call this class from urls and hit API
    """

    def get(self, request):
        """
        This function will when api hit it will go task file call that function
        :param request: it will go the request task function for scrapping the data
        :return: it will return the msg of success in the form the json to end user
        """
        bakcgroung_scrapping.delay()
        return Response({'status': 'pass', 'msg': 'Scrapping InProgress '}, status=status.HTTP_200_OK)

class movie_recommendation(ListAPIView):
    """
    Field lookups in django orm it provide us check particular data into the database
    we can use many function like startswith, endswith, extract, gt, gte,lt,lte, etc....
    """
    serializer_class = Complex_IMDb

    def get_queryset(self):
        # queryset = IMDbScrapping.objects.filter(name__startswith='Top Gun: Maverick')
        # queryset = IMDbScrapping.objects.filter(vote__gt=90000)
        # queryset = IMDbScrapping.objects.filter(runtime__lte=140)
        queryset = IMDbScrapping.objects.filter(runtime__gte=90)
        # queryset = IMDbScrapping.objects.filter(name__endswith='Top Gun: Maverick')
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
    """
    Reterving the objects of particular id from the given into the parameter
    """
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
    """
    Deleting the objects by taking the manual id of which object we need remove from our database
    """
    serializer_class = Complex_IMDb
    # queryset = IMDbScrapping.objects.all()
    def delete(self, request):
        try:
            IMDbScrapping.objects.get(id=12005).delete()
            return Response({'msg': "Done"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'msg': "data not found"}, status=status.HTTP_404_NOT_FOUND)

class select_objects(APIView):
    """
    Select is the query booster in the orm, It will convert multiple query into the single query using the join
    """
    serializer_class = Complex_IMDb
    def get(self,request):
        queryset = IMDbScrapping.objects.select_related().all()
        serializer = Complex_IMDb(instance=queryset, many=True)
        return Response(serializer.data)

class prefetch_objects(APIView):
    """
    Prefetch is also the query booster in the orm
    """
    serializer_class = Complex_IMDb
    def get(self,request):
        queryset = IMDbScrapping.objects.prefetch_related().all()
        serializer = Complex_IMDb(instance=queryset, many=True)
        return Response(serializer.data)

class field_compare_models(APIView):
    """

    """
    serializer_class = Complex_IMDb
    def get(self,request):
        queryset = IMDbScrapping.objects.filter(runtime__gte=F('rating'))
        serializer = Complex_IMDb(instance=queryset, many=True)
        return Response(serializer.data)

class bulk_update_view(APIView):
    def put(self,request):
        data = request.data

        if data:
            if not isinstance(data, list):
                raise ValidationError('Expected list of dict.')

            try:
                id_count = {}
                for i in data:
                    id_count[i['id']] = id_count.get(i['id'], 0) + 1
            except KeyError:
                raise ValidationError('id or name is not present in data.')

            context = {
                'request': request,
                'id_count': id_count
            }

            serializer = bulk_update(data=data, context=context, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': "SuccessFully Update into the database"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('No Data to process', status=status.HTTP_400_BAD_REQUEST)






