from topic.models import Topic, Keyword, TopicUser
from rest_framework import serializers
from rest_framework.response import Response


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

    def update(self, instance, validated_data):
        return ":)"


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'


class TopicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicUser
        fields = '__all__'


