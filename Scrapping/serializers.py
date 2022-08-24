from rest_framework import serializers
from .models import IMDbScrapping

class Complex_IMDb(serializers.ModelSerializer):

    class Meta:
        model = IMDbScrapping
        fields = '__all__'


class bulk_update(Complex_IMDb):
    id = serializers.IntegerField()

    def validate(self, attrs):
        attrs = super(bulk_update, self).validate(attrs)
        id_count = self.context.get('id_count', None)
        if id_count and id_count[f"{attrs['id']}"] > 1:
            raise serializers.ValidationError({'id': 'Same ids present in data.'})
        return attrs

    def create(self, validated_data):
        instance = IMDbScrapping.objects.get(id=validated_data['id'])
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data['description']
        instance.save()
        return instance
    class Meta:
        model= IMDbScrapping
        fields = ['id', 'description']
        validators = []