""" Import libraries """
from .task import bakcgroung_scrapping
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

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
        return Response({'status': 'pass','msg': 'successfully data scraped'},status=status.HTTP_200_OK)

