from .models import New
from rest_framework import serializers


class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = '__all__'


class PreprocessedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = ('title', 'url', 'site', 'site_name',
                  'published', 'main_image', 'text')


