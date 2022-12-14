""" Import libraries """
import logging
from .task import background_scrap
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ComplexImdbSerializers,BulkUpdateSerializers
from .models import IMDbScrapping
from django.db.models import Q, Avg, Max, Min, F
from rest_framework.views import APIView


logger = logging.getLogger('django')
class IMDbScrap(ListAPIView):
    """
    to call this class from urls and hit API
    """


    def get(self, request):
        """
        This function will when api hit it will go task file call that function
        :param request: it will go the request task function for scrapping the data
        :return: it will return the msg of success in the form the json to end user
        """
        background_scrap.delay()
        logging.info("Successfully the run the application")
        return Response({'status': 'pass', 'msg': 'Scrapping InProgress '}, status=status.HTTP_200_OK)

class MovieRecommendation(ListAPIView):
    """
    Field lookups in django orm it provide us check particular data into the database
    we can use many function like startswith, endswith, extract, gt, gte,lt,lte, etc....
    """
    serializer_class = ComplexImdbSerializers

    def get_queryset(self):
        # queryset = IMDbScrapping.objects.filter(name__startswith='Top Gun: Maverick')
        # queryset = IMDbScrapping.objects.filter(vote__gt=90000)
        # queryset = IMDbScrapping.objects.filter(runtime__lte=140)
        queryset = IMDbScrapping.objects.filter(runtime__gte=90)
        logger.info('successfully run the movie recommendation')
        # queryset = IMDbScrapping.objects.filter(name__endswith='Top Gun: Maverick')
        return queryset

class MovieSearch(ListAPIView):
    """
    In Django orm it provides us complex lookups with Q. Where we can or condition in the filter for the data,
    take out the that data from the database. As you can see below exg in which we have applied the Q for OR Condition.
    """
    serializer_class = ComplexImdbSerializers

    def get_queryset(self):
        queryset = IMDbScrapping.objects.filter(Q(rating__gt=8.5) | Q(runtime__lte=110))
        logger.info(" Successfully run the movie search ")
        return queryset


class AggreateRating(APIView):
    """
    Aggregate provide us take out the min, max, avg, count with the database. We can also implement the Aggreate with the using with filtet
    As you show the below examples are given the calculate the different fields
    """
    serializer_class = ComplexImdbSerializers

    def get(self, request):
        # queryset = IMDbScrapping.objects.aggregate(Min('rating'), Max('rating'))
        # queryset = IMDbScrapping.objects.aggregate(Min('vote'), Max('vote'))
        queryset = IMDbScrapping.objects.filter(runtime__lte=120).aggregate(Min('vote'), Max('vote'))
        # queryset = IMDbScrapping.objects.annotate(Count('vote'))
        # s = Complex_IMDb(instance=queryset, many=True)
        logger.info('Successfully run the aggregate rating')
        return Response(queryset)


class LimitRecords(ListAPIView):
    """
    the limit records we are going to show the user sometimes. There lacks of records are available into the our the system,
    but we need show limit numbers of records to the user we can do this using the slicing after query
    In this only positive integer values should given, it will not work for the negative value
    """
    serializer_class = ComplexImdbSerializers
    def get_queryset(self):
        # entry object will not support the negative index , it required only positive integer
        queryset = IMDbScrapping.objects.filter(rating__gt=7.9, runtime__gte=90)[:15]
        logger.info('Run with success the limit records')
        return queryset


class ReturnRecords(APIView):
    """
    Reserving the objects of particular id from the given into the parameter
    """
    serializer_class = ComplexImdbSerializers
    def get(self, request):
        try:
            queryset = IMDbScrapping.objects.get(id=12005)
            serialzier = ComplexImdbSerializers(instance=queryset)
            logger.info('Success return data of particular ID')
            return Response(serialzier.data)
        except:
            logger.error('Sorry, this ID is not present in thr database')
            return Response({'msg': "data not found"}, status=status.HTTP_404_NOT_FOUND)


class DeleteObjects(APIView):
    """
    Deleting the objects by taking the manual id of which object we need remove from our database
    """
    serializer_class = ComplexImdbSerializers
    # queryset = IMDbScrapping.objects.all()
    def delete(self, request):
        try:
            IMDbScrapping.objects.get(id=20309).delete()
            logger.info(
                "Successfully the delete records of the given ID"
            )
            return Response({'msg': "Done"}, status=status.HTTP_204_NO_CONTENT)
        except:
            logger.error("Sorry, this ID is not available into the system")
            return Response({'msg': "data not found"}, status=status.HTTP_404_NOT_FOUND)

class SelectObjects(APIView):
    """
    Select is the query booster in the orm, It will convert multiple query into the single query using the join
    """
    serializer_class = ComplexImdbSerializers
    def get(self,request):
        queryset = IMDbScrapping.objects.select_related().all()
        serializer = ComplexImdbSerializers(instance=queryset, many=True)
        logger.info("Successfully run the select objects in the system ")
        return Response(serializer.data)

class PrefetchObjects(APIView):
    """
    Prefetch is also the query booster in the orm, it basically work on the many-to-many field in forgein key
    """
    serializer_class = ComplexImdbSerializers
    def get(self,request):
        queryset = IMDbScrapping.objects.prefetch_related().all()
        serializer = ComplexImdbSerializers(instance=queryset, many=True)
        logger.info("Successfully run the prefetch objects in the system")
        return Response(serializer.data)

class FieldCompareModels(APIView):
    """
    when we want to compare the different fields of the same database that time we can use this.
    It will compare its running on the Bitwise operators
    """
    serializer_class = ComplexImdbSerializers
    def get(self,request):
        queryset = IMDbScrapping.objects.filter(runtime__gte=F('rating'))
        serializer = ComplexImdbSerializers(instance=queryset, many=True)
        logger.info("Successfully the run the field compare models")
        return Response(serializer.data)

class BulkUpdateView(APIView):
    """
    when we want to update many records in the single sql execution that time we can use the bulk updates
    """
    def put(self,request):
        """
        Data should have given in the form of the list and inside the list it should be dictionary
        :param request:  it sends data which we need to update, it should be correct format otherwise it raise error
        :return: If data is update successfully it will return success msg or if any error is arise error
        """
        data = request.data

        if data:
            if not isinstance(data, list):
                raise ValidationError('Expected list of dict.')

            try:
                id_count = {}
                for i in data:
                    id_count[i['id']] = id_count.get(i['id'], 0) + 1
            except KeyError:
                raise ValidationError('Id not present in data.')

            context = {
                'request': request,
                'id_count': id_count
            }

            serializer = BulkUpdateSerializers(data=data, context=context, many=True)
            if serializer.is_valid():
                serializer.save()
                logger.info("Successfully bulk update into the system...")
                return Response({'msg': "SuccessFully Update into the database"}, status=status.HTTP_201_CREATED)
            logger.warning("some warning has been arise by serializers")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        logger.error("Hey, some error has been arise into the system")
        return Response({'msg': 'No Data to process'}, status=status.HTTP_400_BAD_REQUEST)






