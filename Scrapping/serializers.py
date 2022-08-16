from rest_framework import serializers
from .models import IMDbScrapping


class Complex_IMDb(serializers.ModelSerializer):
    class Meta:
        model = IMDbScrapping
        fields = '__all__'