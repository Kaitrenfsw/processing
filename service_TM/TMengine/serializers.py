from TMengine.models import LdaModel
from rest_framework import serializers


class LdaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LdaModel
        fields = ('id', 'filename', 'creation_date', 'newest', 'in_use',)
