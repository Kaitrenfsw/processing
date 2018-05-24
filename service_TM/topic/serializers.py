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
        fields = ('id', 'name', 'weight')


class TopicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicUser
        fields = '__all__'


class TopicKeywordSerializer(serializers.ModelSerializer):
    keyword_topic = KeywordSerializer(many=True)

    class Meta:
        model = Topic
        fields = ('id', 'topic_number', 'corpus_number', 'name', 'keyword_topic')

