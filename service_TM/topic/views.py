from topic.models import Topic, Keyword, TopicUser
from topic.serializers import TopicSerializer, KeywordSerializer, TopicUserSerializer, TopicKeywordSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


class TopicViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        topics = Topic.objects.all()
        response_array = []
        for topic in topics:
            serialized = TopicKeywordSerializer(topic).data
            response_array.append(serialized)

        return Response(data=response_array, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        new_topic_data = request.data
        new_topic = Topic(topic_number=new_topic_data['topic_number'],
                          corpus_number=new_topic_data['corpus_number'],
                          name=new_topic_data['topic_name'])
        new_topic.save()
        return Response(data={"New Topic added successfully"}, status=status.HTTP_200_OK)

    @staticmethod
    def retrieve(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def update(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def partial_update(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def destroy(request, pk=None):
        return Response(data={":)"})


topic_list = TopicViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
})


class KeywordViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        queryset = KeywordSerializer(Keyword.objects.all(), many=True).data
        return Response(data=queryset, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        return Response(data={":)"})

    @staticmethod
    def retrieve(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def update(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def partial_update(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def destroy(request, pk=None):
        return Response(data={":)"})


keyword_list = KeywordViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
})


class TopicUserViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        usertopics = TopicUser.objects.filter(user_id=1)
        response_array = []
        for topic in usertopics:
            dic_of_topics = {}
            keywords = Keyword.objects.filter(topic_id=topic.pk)
            dic_of_topics['topic'] = TopicUserSerializer(topic).data
            dic_of_topics['topic']['keywords'] = KeywordSerializer(keywords, many=True).data
            response_array.append(dic_of_topics)

        return Response(data=response_array, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        return Response(data={":)"})

    @staticmethod
    def retrieve(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def update(request, pk=None):
        data = request.data
        older_topics = TopicUser.objects.filter(user_id=1).values_list('topic_id', flat=True)
        updated_topics = data["user_topics_id"]

        # adding new topics that didn't exist
        for new_topic_id in updated_topics:
            if new_topic_id not in older_topics:
                topic_instance = Topic.objects.get(id=new_topic_id)
                topic = TopicUser(user_id=data['user_id'], topic_id=topic_instance)
                topic.save()
        # deleting topics
        for old_topic_id in older_topics:
            if old_topic_id not in updated_topics:
                topicuser_instance = TopicUser.objects.get(id=old_topic_id)
                topicuser_instance.delete()

        return Response(data={}, status=status.HTTP_200_OK)

    @staticmethod
    def partial_update(request, pk=None):
        if 'id' in request.data:
            print(":()")
        else:
            print("chan!")
        return Response(data={":)"})

    @staticmethod
    def destroy(request, pk=None):
        return Response(data={":)"})


topicUser_list = TopicUserViewSet.as_view({
    'post': 'list',
    'put': 'update',
    'patch': 'partial_update',
})
