from topic.models import Topic, Keyword, TopicUser
from rest_framework import serializers


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('topic_number', 'lda_model', 'name')


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
        fields = ('id', 'topic_number', 'lda_model', 'name', 'keyword_topic')

