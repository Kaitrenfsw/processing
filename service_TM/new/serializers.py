from .models import New, NewClassification
from rest_framework import serializers


class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = '__all__'


class NewClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewClassification
        fields = '__all__'


class PreprocessedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = ('title', 'url', 'site', 'site_name',
                  'published', 'main_image', 'text')


class NewClassifiedSerializer(serializers.ModelSerializer):
    new_classification = NewClassificationSerializer(many=True)

    class Meta:
        model = New
        fields = '__all__'






